from flask import request, Blueprint, jsonify
from app.servico.model import Servico
from app.extensions import db

servico_api = Blueprint('servico_api', __name__) # armazena as rotas

@servico_api.route('/servico', methods=['GET', 'POST'])
def index():
    if (request.method == 'GET'):
        servicos = Servico.query.all()   # pega todos os servicos

        return jsonify([servico.json() for servico in servicos]), 200

    if (request.method == 'POST'):
        dados = request.json
        
        nome = dados.get('nome')
        horario = dados.get('horario')
        pet_id = dados.get('pet_id', 0)
        descricao = dados.get('descricao', "")

        if (nome is None or horario is None or pet_id is None or descricao is None):
            return {'erro' : 'Falta um campo obrigatorio: nome ou horario'}, 400

        if(not isinstance(nome, str) or not isinstance(horario, str) or not isinstance(pet_id, int) or not isinstance(descricao,str) 
        or len(nome) > 63 or len(horario) > 20 or len(descricao) > 127 ):

            return {"erro" : "nome, horario, pet_id ou descricao em formato invalido"}, 400
        
        servico = Servico(nome = nome, horario = horario, pet_id = pet_id, descricao = descricao)
        
        db.session.add(servico) # não salva ainda, apenas 'coloca na fila' para ser salvo

        db.session.commit() # salva no banco oq foi add na 'fila'

        return servico.json(), 200


@servico_api.route('/servico/<int:id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def pagina_servico(id):
    servico = Servico.query.get_or_404(id) #se existir o servico retorna os dados, caso contrário sai da função retornando 404

    if (request.method == 'GET'):
        return servico.json(), 200

    if (request.method == 'PATCH' or 'PUT'):
        dados = request.json

        nome = dados.get('nome', servico.nome)
        horario = dados.get('horario', servico.horario)
        pet_id = dados.get('pet_id', servico.pet_id)
        descricao = dados.get('descricao', servico.descricao)

        if(not isinstance(nome, str) or not isinstance(horario, str) or not isinstance(pet_id, int) or not isinstance(descricao,str) 
        or len(nome) > 63 or len(horario) > 20 or len(descricao) > 127 ):

            return {"erro" : "nome, horario, pet_id ou descricao em formato invalido"}, 400

        servico.nome = nome
        servico.horario = horario
        servico.pet_id = pet_id
        servico.descricao = descricao

        db.session.add(servico)

    if (request.method == 'DELETE'):
        #db.session.delete(servico)
        return {"erro" : "recurso ainda nao disponivel"}

    db.session.commit() # executa no banco todas as tarefas que estavam na fila
    return servico.json(), 200
