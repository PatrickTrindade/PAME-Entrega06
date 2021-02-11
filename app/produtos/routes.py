from flask import Blueprint

from .controllers import (ProdutoDetails, ProdutoPagina)

produto_api = Blueprint('produto_api', __name__) # armazena as rotas

produto_api.add_url_rule(
    '/produto/', view_func=ProdutoDetails.as_view('produto_details'), methods=['GET', 'POST']
)

produto_api.add_url_rule(
    '/produto/<int:id>', view_func=ProdutoPagina.as_view('produto_pagina'), methods=['GET', 'PATCH', 'DELETE']
)