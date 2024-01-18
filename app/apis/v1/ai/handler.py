from uuid import uuid4
from app.utils.utils import message
from app.utils.utils import send_rmq_message_with_pika
from app.utils.extensions import db
import tensorflow as tf
import numpy as np
import cv2
import os
import shap
from matplotlib import pyplot as plt
from imagekitio import ImageKit
from .models import AiModel

imagekit = ImageKit(
    private_key='private_H3sT1y8NIBTJkMQsw1rvKtbD5mM=',
    public_key='public_2YXuApzLJHgRqCM53bJ/DLbM/ec=',
    url_endpoint='https://ik.imagekit.io/deepthesis'
)


def update_model_status(str_uuid, status, prediction="", inpaint_telea="", inpaint_ns="", blur="", saliency=""):
    ai_model_query = AiModel.query.filter_by(
        image_id=str_uuid
    ).first()
    ai_model_query.status = status
    if prediction != "":
        ai_model_query.prediction = prediction
    if inpaint_telea != "":
        ai_model_query.shap_impaint_telea_image_url = inpaint_telea
    if inpaint_ns != "":
        ai_model_query.shap_inpaint_ns_image_url = inpaint_ns
    if blur != "":
        ai_model_query.shap_blur_image_url = blur
    if saliency != "":
        ai_model_query.saliency_image_url = saliency

    db.session.commit()


def upload_image(str_uuid, file_name):
    result = imagekit.upload_file(
        file=open(f"images/{file_name}", "rb"),
        file_name=file_name,
    )
    main_data = result.response_metadata
    raw_data = main_data.raw
    if main_data.http_status_code == 200:
        url = raw_data["url"]
        if "inpaint_telea" in file_name:
            update_model_status(str_uuid=str_uuid, status="UPLOADING_INPAINT_TELEA", inpaint_telea=url)
        elif "inpaint_ns" in file_name:
            update_model_status(str_uuid=str_uuid, status="UPLOADING_INPAINT_NS", inpaint_ns=url)
        elif "blur" in file_name:
            update_model_status(str_uuid=str_uuid, status="UPLOADING_BLUR", blur=url)
        elif "saliency" in file_name:
            update_model_status(str_uuid=str_uuid, status="UPLOADING_SALIENCY", saliency=url)


def delete_image(file_name):
    os.remove(f"images/{file_name}")


def predict_image(file):
    str_uuid = str(uuid4())
    resp = message(True, "Get prediction id success")
    resp["uuid"] = str_uuid
    file.save(f"images/{str_uuid}.png")
    ai_model_query = AiModel(
        image_id=str_uuid,
        status="STARTED"
    )
    db.session.add(ai_model_query)
    db.session.commit()
    payload = {
        "type": "start_prediction",
        "data": {
            "uuid": str_uuid
        }
    }
    send_rmq_message_with_pika(payload)
    return resp, 200


def map_index(index):
    return {0: 'Fractured', 1: 'Not Fractured'}.get(index)


def get_prediction_class(model, image):
    prediction = model.predict(image)
    prediction_index = np.argmax(prediction, axis=1)[0]
    return map_index(prediction_index)


def start_plot_shap(str_uuid, model, main_image, processed_image):
    class_names = ['Fractured', 'Not Fractured']
    mask_list = ["inpaint_telea", "inpaint_ns", "blur(28,28)"]
    for mask in mask_list:
        masker = shap.maskers.Image(mask, main_image.shape)
        explainer = shap.Explainer(model, masker, output_names=class_names)
        shap_values = explainer(processed_image, outputs=shap.Explanation.argsort.flip[:5])
        shap.image_plot(shap_values)
        file_name = f"{str_uuid}_{mask}.png"
        plt.savefig(f"images/{file_name}")
        upload_image(str_uuid, file_name)
        delete_image(file_name)
        update_model_status(str_uuid, f"SHAP_{mask.upper()}_UPLOADED")


def input_img_for_saliency(image):
    image = tf.expand_dims(image, axis=0)
    image = tf.cast(image, tf.float32)
    image = tf.image.resize(image, [224, 224])
    return image


def normalize_image(img):
    grads_norm = img[:, :, 0] + img[:, :, 1] + img[:, :, 2]
    grads_norm = (grads_norm - tf.reduce_min(grads_norm)) / (tf.reduce_max(grads_norm) -
                                                             tf.reduce_min(grads_norm))
    return grads_norm


def plot_maps(str_uuid, img1, img2, vmin=0.3, vmax=0.7, mix_val=2):
    f = plt.figure(figsize=(45, 15))
    plt.subplot(1, 3, 1)
    plt.imshow(img1, vmin=vmin, vmax=vmax, cmap="ocean")
    plt.axis("off")
    plt.subplot(1, 3, 2)
    plt.imshow(img2, cmap="ocean")
    plt.axis("off")
    plt.subplot(1, 3, 3)
    plt.imshow(img1 * mix_val + img2 / mix_val, cmap="ocean")
    plt.axis("off")
    file_name = f"{str_uuid}_saliency.png"
    plt.savefig(f'images/{file_name}')
    upload_image(str_uuid, file_name)
    delete_image(file_name)
    update_model_status(str_uuid, "SALIENCY_IMAGE_UPLOADED")


def save_saliency_image(str_uuid, model, main_image):
    input_img = input_img_for_saliency(main_image)
    result = model(input_img)
    max_idx = tf.argmax(result, axis=1)
    with tf.GradientTape() as tape:
        tape.watch(input_img)
        result = model(input_img)
        max_score = result[0, max_idx[0]]
    grads = tape.gradient(max_score, input_img)
    plot_maps(str_uuid, normalize_image(grads[0]), normalize_image(input_img[0]))


def run_model_and_predict(str_uuid):
    update_model_status(str_uuid, "MODEL_INITIALIZING")
    model = tf.keras.models.load_model('models/densenet121')

    update_model_status(str_uuid, "MODEL_INITIALIZED")

    image_cv2 = cv2.imread(f"images/{str_uuid}.png")
    resize_image = cv2.resize(image_cv2, (224, 224))
    img = np.expand_dims(resize_image, axis=0)
    update_model_status(str_uuid, "IMAGE_PROCESSED")
    prediction = get_prediction_class(model, img)
    update_model_status(str_uuid, "IMAGE_PREDICTED", prediction=prediction)
    start_plot_shap(str_uuid, model, resize_image, img)
    save_saliency_image(str_uuid, model, resize_image)
    update_model_status(str_uuid, "COMPLETED")
    delete_image(str_uuid + ".png")


def get_prediction_process_status(str_uuid):
    ai_model = AiModel.query.filter_by(image_id=str_uuid).first()
    resp = message(True, "Get Prediction process status success", )
    resp["pred_status"] = ai_model.status
    resp["prediction"] = ai_model.prediction
    resp["images"] = [
        ai_model.shap_impaint_telea_image_url,
        ai_model.shap_inpaint_ns_image_url,
        ai_model.shap_blur_image_url,
        ai_model.saliency_image_url
    ]
    return resp, 200
