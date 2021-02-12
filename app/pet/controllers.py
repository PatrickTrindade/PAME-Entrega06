from flask import request, Blueprint, jsonify
from flask.views import MethodView
#from flask_jwt_extended import jwt_required, get_jwt_identity


from app.pet.model import Pet
from app.extensions import db


class PetDetails(MethodView):       #/pet
    def get(self):
        pets = Pet.query.all()   # pega todos os pets

        return jsonify([pet.json() for pet in pets]), 200

    def post(self):

        #decorators = [jwt_required]     # ele precisa estar logado para adicionar um pet

        print("g:", get_jwt_identity())

        dados = request.json
        
        nome = dados.get('nome', "")
        raca = dados.get('raca')
        porte = dados.get('porte')
        data_nascimento = dados.get('data_nascimento')
        #user_id = get_jwt_identity() #-> o objetivo era pegar o id do usuario logado

        if (raca is None or porte is None or data_nascimento is None):
            return {'erro' : 'Falta um campo obrigatorio raca, porte ou nascimento'}, 400

        if(not isinstance(nome, str) or not isinstance(raca, str) or not isinstance(porte, str) or not isinstance(data_nascimento, str)):
            return {'erro' : 'nome, raca, porte, ou data de nascimento inválidos'}, 400
        
        pet = Pet(nome = nome, raca = raca, porte = porte, data_nascimento = data_nascimento, user_id=user_id)
        
        db.session.add(pet) # não salva ainda, apenas 'coloca na fila' para ser salvo

        db.session.commit() # salva no banco oq foi add na 'fila'

        return pet.json(), 200

class PetPagina(MethodView):        #/pet/<int:id>
    def get(self, id):
        pet = Pet.query.get_or_404(id) #se existir o pet retorna os dados, caso contrário sai da função retornando 404

        return pet.json(), 200


    def patch(self, id):
        pet = Pet.query.get_or_404(id) #se existir o pet retorna os dados, caso contrário sai da função retornando 404

        dados = request.json

        nome = dados.get('nome', pet.nome)
        raca = dados.get('raca', pet.raca)
        porte = dados.get('porte', pet.porte)
        data_nascimento = dados.get('data_nascimento', pet.data_nascimento)

        if(not isinstance(nome, str) or not isinstance(raca, str) or not isinstance(porte, str) or not isinstance(data_nascimento,str) 
        or len(nome) > 63 or len(raca) > 63 or len(porte) > 63 or len(data_nascimento) > 63 ):

            return {"erro" : "nome, raca, porte ou data de nascimento em formato invalido"}

        pet.nome = nome
        pet.raca = raca
        pet.porte = porte
        pet.data_nascimento = data_nascimento

        db.session.add(pet)

        db.session.commit() # executa no banco todas as tarefas que estavam na fila
        return pet.json(), 200

    def delete(self, id):
        #db.session.delete(pet)
        #db.session.commit()

        return {"erro" : "recurso ainda nao disponivel"}

    




'''
#essas func estao sendo subtituidas pela classe acima
@pet_api.route('/pet', methods=['GET', 'POST'])
def index():
    if (request.method == 'GET'):
        pets = Pet.query.all()   # pega todos os pets

        return jsonify([pet.json() for pet in pets]), 200

    if (request.method == 'POST'):
        dados = request.json
        
        nome = dados.get('nome', "")
        raca = dados.get('raca')
        porte = dados.get('porte')
        data_nascimento = dados.get('data_nascimento')

        if (raca is None or porte is None or data_nascimento is None):
            return {'erro' : 'Falta um campo obrigatorio raca, porte ou nascimento'}, 400

        if(not isinstance(nome, str) or not isinstance(raca, str) or not isinstance(porte, str) or not isinstance(data_nascimento, str)):
            return {'erro' : 'nome, raca, porte, ou data de nascimento inválidos'}, 400
        
        pet = Pet(nome = nome, raca = raca, porte = porte, data_nascimento = data_nascimento)
        
        db.session.add(pet) # não salva ainda, apenas 'coloca na fila' para ser salvo

        db.session.commit() # salva no banco oq foi add na 'fila'

        return pet.json(), 200


@pet_api.route('/pet/<int:id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def pagina_pet(id):
    pet = Pet.query.get_or_404(id) #se existir o pet retorna os dados, caso contrário sai da função retornando 404

    if (request.method == 'GET'):
        return pet.json(), 200

    if (request.method == 'PATCH' or 'PUT'):
        dados = request.json

        nome = dados.get('nome', pet.nome)
        raca = dados.get('raca', pet.raca)
        porte = dados.get('porte', pet.porte)
        data_nascimento = dados.get('data_nascimento', pet.data_nascimento)

        if(not isinstance(nome, str) or not isinstance(raca, str) or not isinstance(porte, str) or not isinstance(data_nascimento,str) 
        or len(nome) > 63 or len(raca) > 63 or len(porte) > 63 or len(data_nascimento) > 63 ):

            return {"erro" : "nome, raca, porte ou data de nascimento em formato invalido"}

        pet.nome = nome
        pet.raca = raca
        pet.porte = porte
        pet.data_nascimento = data_nascimento

        db.session.add(pet)

    if (request.method == 'DELETE'):
        #db.session.delete(pet)
        return {"erro" : "recurso ainda nao disponivel"}

    db.session.commit() # executa no banco todas as tarefas que estavam na fila
    return pet.json(), 200
'''