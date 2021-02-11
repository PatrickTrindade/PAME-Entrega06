from flask import Blueprint

from .controllers import (PetDetails, PetPagina)

pet_api = Blueprint('pet_api', __name__) # armazena as rotas

pet_api.add_url_rule(
    '/pet/', view_func=PetDetails.as_view('pet_details'), methods=['GET', 'POST']
)

pet_api.add_url_rule(
    '/pet/<int:id>', view_func=PetPagina.as_view('pet_pagina'), methods=['GET', 'PUT', 'PATCH', 'DELETE']
)