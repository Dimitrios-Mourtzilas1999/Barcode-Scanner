from flask import Blueprint

productbp = Blueprint(
    "product",
    __name__,
    url_prefix="/product",
    static_folder="static",
    template_folder="templates",
)

from . import routes
