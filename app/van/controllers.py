from flask import request, Blueprint, jsonify
from app.van.model import Van
from app.extensions import db

van_api = Blueprint('van_api', __name__) # armazena as rotas

@van_api.route('/van', methods=['GET', 'POST'])
def index():
    if (request.method == 'GET'):
        vans = Van.query.all()   # pega todos os vans

        return jsonify([van.json() for van in vans]), 200

    if (request.method == 'POST'):
        dados = request.json
        
        horario = dados.get('horario')
        id_pet = dados.get('id_pet', 0)
        descricao = dados.get('descricao', "")

        if (horario is None):
            return {'erro' : 'O campo de horario é obrigatório'}, 400

        if(not isinstance(horario, str) or not isinstance(id_pet, int) or not isinstance(descricao, str) 
        or len(horario) > 20 or len(descricao) > 127):

            return {'erro' : 'horario, id_pet, ou descricao inválidos'}, 400
        
        van = Van(horario = horario, id_pet = id_pet, descricao = descricao)
        
        db.session.add(van) # não salva ainda, apenas 'coloca na fila' para ser salvo

        db.session.commit() # salva no banco oq foi add na 'fila'

        return van.json(), 200


@van_api.route('/van/<int:id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def pagina_van(id):
    van = Van.query.get_or_404(id) #se existir o van retorna os dados, caso contrário sai da função retornando 404

    if (request.method == 'GET'):
        return van.json(), 200

    if (request.method == 'PATCH' or 'PUT'):
        dados = request.json

        horario = dados.get('horario', van.horario)
        id_pet = dados.get('id_pet', van.id_pet)
        descricao = dados.get('descricao', van.descricao)

        if(not isinstance(horario, str) or not isinstance(id_pet, int) or not isinstance(descricao, str)
        or len(horario) > 20 or len(descricao) > 127):
        
            return {'erro' : 'horario, id_pet, ou descricao inválidos'}, 400

        van.horario = horario
        van.id_pet = id_pet
        van.descricao = descricao

        db.session.add(van)

    if (request.method == 'DELETE'):
        #db.session.delete(van)
        return {"erro" : "recurso ainda nao disponivel"}

    db.session.commit() # executa no banco todas as tarefas que estavam na fila
    return van.json(), 200
