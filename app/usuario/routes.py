from flask import Blueprint

from .controllers import (UsuarioDetails, UsuarioPagina, UsuarioLogin)

usuario_api = Blueprint('usuario_api', __name__) # armazena as rotas


usuario_api.add_url_rule(
    '/usuario/', view_func=UsuarioDetails.as_view('usuario_details'), methods=['GET', 'POST']
)

usuario_api.add_url_rule(
    '/usuario/<int:id>', view_func=UsuarioPagina.as_view('pagina_usuario'), methods=['GET', 'PATCH']
)

usuario_api.add_url_rule(
    '/login', view_func=UsuarioLogin.as_view('usuario_login'), methods=['POST']
)

