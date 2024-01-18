from datetime import datetime

from app.utils.extensions import db


class AiModel(db.Model):
    __tablename__ = 'ai'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    image_id = db.Column(db.String(50))
    status = db.Column(db.String(50))
    prediction = db.Column(db.String(50), default="")
    shap_impaint_telea_image_url = db.Column(db.String(200))
    shap_inpaint_ns_image_url = db.Column(db.String(200))
    shap_blur_image_url = db.Column(db.String(200))
    saliency_image_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
