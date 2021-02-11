from flask import Blueprint

from .controllers import (VanDetails, VanPagina)

van_api = Blueprint('van_api', __name__) # armazena as rotas

van_api.add_url_rule(
    '/van/', view_func=VanDetails.as_view('van_details'), methods=['GET', 'POST']
)

van_api.add_url_rule(
    '/van/<int:id>', view_func=VanPagina.as_view('van_pagina'), methods=['GET', 'PATCH', 'DELETE']
)