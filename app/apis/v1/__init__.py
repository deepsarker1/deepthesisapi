from flask import Blueprint
from flask_restx import Api
from app.apis.v1.ai.route import api as api_ai
from app.utils.utils import api as api_utils

blueprint_v1 = Blueprint("api_v1", __name__, url_prefix="/v1")

api_v1 = Api(
    blueprint_v1,
    title="Thesis API",
    version="1.0",
    doc="/docs"
)
api_v1.add_namespace(api_utils)
api_v1.add_namespace(api_ai)

