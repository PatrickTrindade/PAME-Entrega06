from flask import request, jsonify, render_template #, Blueprint tirado durante a cap 10/02
from app.usuario.model import Usuario
from app.extensions import db
import bcrypt
from flask_mail import Message
from flask_jwt_extended import create_acess_token

usuario_api = Blueprint('usuario_api', __name__) # armazena as rotas


class UsuarioDetails(MethodView):        #usuario/

    def get(self):
        usuarios = Usuario.query.all()   # pega todos os usuarios

        return jsonify([usuario.json() for usuario in usuarios]), 200

    def post(self):
        dados = request.json
        
        username = dados.get('username')
        senha = dados.get('senha')
        nome = dados.get('nome')
        endereco = dados.get('endereco')
        email = dados.get('email')

        if (username  is None or senha is None or nome is None or endereco is None or email is None):
            return {'erro' : 'Falta um campo obrigatorio'}, 400

        if(not isinstance(username, str) or not isinstance(senha, str) or not isinstance(nome, str) or not isinstance(endereco, str) or not isinstance(email, str)
        or len(username) > 63 or len(senha) > 63 or len(nome) > 63 or len(endereco) > 63 or len(email) > 63):

            return {'erro' : 'username, senha, nome, endereco ou email inválidos'}, 400
        

        senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
        #para verificar -> bcrypt.checkpw(senha, hash(?))


        usuario = Usuario(username = username, senha = senha_hash, nome = nome, endereco = endereco, email = email)
        
        db.session.add(usuario) # não salva ainda, apenas 'coloca na fila' para ser salvo

        db.session.commit() # salva no banco oq foi add na 'fila'

        msg = Message(sender='email@quemvaienviar.com',
                    recipients=[email],
                    subject="Bem-vindo!",
                    html=render_template('email01.html', nome=nome') 
                    )

        mail.send(msg)

        return usuario.json(), 200


class PaginaUsuario(MethodView):    #usuario/<int:id>

    decorators = [jwt_required]

    def get(self, id):
        if(get_jwt_identity() != id):
            return {'erro' : "usuário não permitido"}, 400

        usuario = Usuario.query.get_or_404(id)

        return usuario.json(), 200

    def patch(self, id):
        usuario = Usuario.query.get_or_404(id)

        dados = request.json

        username = dados.get('username', usuario.username)
        senha = dados.get('senha', usuario.senha)
        nome = dados.get('nome', usuario.nome)
        endereco = dados.get('endereco', usuario.endereco)
        email = dados.get('email', usuario.email)

        if(not isinstance(username, str) or not isinstance(senha, str) or not isinstance(nome, str) or not isinstance(endereco, str) or not isinstance(email, str)
        or len(username) > 63 or len(senha) > 63 or len(nome) > 63 or len(endereco) > 63 or len(email) > 63):

            return {'erro' : 'username, senha, nome, endereco ou email inválidos'}, 400

        usuario.username = username
        usuario.senha = senha
        usuario.nome = nome
        usuario.endereco = endereco
        usuario.email = email

        db.session.add(usuario)


class UsuarioLogin(MethodView): #/login
    def post(self):
        dados = request.json

        senha = str(dados.get('password'))
        email = dados.get('email')

        usuario = Usuario.query.filter_by(email=email).first()

        if (not usuario or not bcrypt.checkpw(senha.encode(), usuario.senha)):
            return ("erro": "Usuário não encontrado"), 400

        token = create_acess_token(identity=usuario.id)

        return {"token": token}, 400



'''
@usuario_api.route('/usuario', methods=['GET', 'POST'])
def index():
    if (request.method == 'GET'):
        usuarios = Usuario.query.all()   # pega todos os usuarios

        return jsonify([usuario.json() for usuario in usuarios]), 200

    if (request.method == 'POST'):
        dados = request.json
        
        username = dados.get('username')
        senha = dados.get('senha')
        nome = dados.get('nome')
        endereco = dados.get('endereco')
        email = dados.get('email')

        if (username  is None or senha is None or nome is None or endereco is None or email is None):
            return {'erro' : 'Falta um campo obrigatorio'}, 400

        if(not isinstance(username, str) or not isinstance(senha, str) or not isinstance(nome, str) or not isinstance(endereco, str) or not isinstance(email, str)
        or len(username) > 63 or len(senha) > 63 or len(nome) > 63 or len(endereco) > 63 or len(email) > 63):

            return {'erro' : 'username, senha, nome, endereco ou email inválidos'}, 400
        

        senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
        #para verificar -> bcrypt.checkpw(senha, hash(?))


        usuario = Usuario(username = username, senha = senha_hash, nome = nome, endereco = endereco, email = email)
        
        db.session.add(usuario) # não salva ainda, apenas 'coloca na fila' para ser salvo

        db.session.commit() # salva no banco oq foi add na 'fila'

        msg = Message(sender='email@quevaienviar.com',
                    recipients=[email],
                    subject="Bem-vindo!",
                    html=render_template('email01.html', nome=nome')
                    )

        mail.send(msg)

        return usuario.json(), 200


@usuario_api.route('/usuario/<int:id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def pagina_usuario(id):
    usuario = Usuario.query.get_or_404(id) #se existir o usuario retorna os dados, caso contrário sai da função retornando 404

    if (request.method == 'GET'):
        return usuario.json(), 200

    if (request.method == 'PATCH' or 'PUT'):
        dados = request.json

        username = dados.get('username', usuario.username)
        senha = dados.get('senha', usuario.senha)
        nome = dados.get('nome', usuario.nome)
        endereco = dados.get('endereco', usuario.endereco)
        email = dados.get('email', usuario.email)

        if(not isinstance(username, str) or not isinstance(senha, str) or not isinstance(nome, str) or not isinstance(endereco, str) or not isinstance(email, str)
        or len(username) > 63 or len(senha) > 63 or len(nome) > 63 or len(endereco) > 63 or len(email) > 63):

            return {'erro' : 'username, senha, nome, endereco ou email inválidos'}, 400

        usuario.username = username
        usuario.senha = senha
        usuario.nome = nome
        usuario.endereco = endereco
        usuario.email = email

        db.session.add(usuario)

    if (request.method == 'DELETE'):
        #db.session.delete(usuario)
        return {"erro" : "recurso ainda nao disponivel"}

    db.session.commit() # executa no banco todas as tarefas que estavam na fila
    return usuario.json(), 200
'''