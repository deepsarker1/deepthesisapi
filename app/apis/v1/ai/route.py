from flask import request
from flask_restx import Namespace, Resource, fields
from werkzeug.datastructures import FileStorage
from app.utils.utils import err_resp, error_response_model
from .handler import predict_image, get_prediction_process_status

api = Namespace(
    name="ai",
    path="/ai",
    description="AI Tool"
)

parser = api.parser()

predict_image_response = api.model("Predict Image", {
    "status": fields.Boolean,
    "message": fields.String,
    "uuid": fields.String
})

prediction_response = api.model("Prediction Response", {
    "message": fields.Boolean,
})


@api.route("/predict")
class PredictImage(Resource):
    parser.add_argument('file', location='files', type=FileStorage, required=True)

    @api.doc(
        "Get Predict Image",
        responses={
            200: ("Success", predict_image_response),
            400: ("Bad Request", error_response_model)
        }
    )
    @api.expect(parser)
    def post(self):
        args = parser.parse_args()
        uploaded_file = args['file']
        if uploaded_file is None:
            return err_resp("Image Not Found", "bad_request", 400)

        return predict_image(uploaded_file)


@api.route("/prediction-status/<string:uuid>")
class PredictionStatus(Resource):
    @api.doc(
        "Get Prediction Responses",
        responses={
            200: ("Success", prediction_response)
        }
    )
    def get(self, uuid):
        return get_prediction_process_status(uuid)
