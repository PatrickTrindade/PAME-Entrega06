from flask import Blueprint

from .controllers import (ServicoDetails, ServicoPagina)

servico_api = Blueprint('servico_api', __name__) # armazena as rotas

servico_api.add_url_rule(
    '/servico/', view_func=ServicoDetails.as_view('servico_details'), methods=['GET', 'POST']
)

servico_api.add_url_rule(
    '/servico/<int:id>', view_func=ServicoPagina.as_view('servico_pagina'), methods=['GET', 'PATCH', 'DELETE']
)