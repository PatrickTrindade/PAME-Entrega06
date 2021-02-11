from flask import request, Blueprint, jsonify
from flask.views import MethodView

from app.servico.model import Servico
from app.extensions import db

class ServicoDetails(MethodView):       #/servico/
    def get(self):
        servicos = Servico.query.all()   # pega todos os servicos

        return jsonify([servico.json() for servico in servicos]), 200

    def post(self):

        dados = request.json
        
        horario = dados.get('horario')
        pet_id = dados.get('pet_id')
        descricao = dados.get('descricao', "")
        banho = dados.get('banho', False)
        tosa = dados.get('tosa', False)

        if (horario is None or pet_id is None):
            return {'erro' : 'É necessário inserir um horário e um pet'}, 400

        if(not isinstance(horario, str) or not isinstance(pet_id, int) or not isinstance(descricao,str) 
        or not isinstance(banho, bool) or not isinstance(tosa, bool) 
        or len(horario) > 20 or len(descricao) > 127 ):

            return {"erro" : "Campo com formato invalido"}, 400
        
        servico = Servico(horario = horario, pet_id = pet_id, descricao = descricao, banho=banho, tosa=tosa)
        
        db.session.add(servico) # não salva ainda, apenas 'coloca na fila' para ser salvo

        db.session.commit() # salva no banco oq foi add na 'fila'

        return servico.json(), 200 


class ServicoPagina(MethodView):        #/servico/<int:id>
    def get(self, id):
        return servico.json(), 200

    def patch(self, id):
        dados = request.json

        horario = dados.get('horario', servico.horario)
        pet_id = dados.get('pet_id', servico.pet_id)
        descricao = dados.get('descricao', servico.descricao)
        banho = dados.get('banho', servico.banho)
        tosa = dados.get('tosa', servico.tosa)

        if(not isinstance(horario, str) or not isinstance(pet_id, int) or not isinstance(descricao,str) 
        or not isinstance(banho, bool) or not isinstance(tosa, bool) 
        or len(horario) > 20 or len(descricao) > 127 ):

            return {"erro" : "horario, pet_id ou descricao em formato invalido"}, 400

        servico.horario = horario
        servico.pet_id = pet_id
        servico.descricao = descricao
        servico.banho = banho
        servico.tosa = tosa

        db.session.add(servico)
        db.session.commit()
        return servico.json(), 200

    def delete(self, id):
        return {"erro" : "recurso ainda nao disponivel"}
        db.session.delete(servico)
        db.session.commit()
        return servico.json(), 200
