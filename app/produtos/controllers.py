from flask import request, Blueprint, jsonify
from app.produtos.model import Produto
from app.extensions import db

produto_api = Blueprint('produto_api', __name__) # armazena as rotas

@produto_api.route('/produto', methods=['GET', 'POST'])
def index():
    if (request.method == 'GET'):
        produtos = Produto.query.all()   # pega todos os produtos

        return jsonify([produto.json() for produto in produtos]), 200

    if (request.method == 'POST'):
        dados = request.json
        
        nome = dados.get('nome')
        descricao = dados.get('descricao', "")
        qnt_estoque = dados.get('qnt_estoque', 0)

        if (nome is None):
            return {'erro' : 'O produto exige um nome'}, 400

        if(not isinstance(nome, str) or not isinstance(descricao, str) or not isinstance(qnt_estoque, int)
        or len(nome) > 63 or len(descricao) > 127):
            return {'erro' : 'nome, descricao, ou qnt_estoque inválidos'}, 400
        
        produto = Produto(nome = nome, descricao = descricao, qnt_estoque = qnt_estoque)
        
        db.session.add(produto) # não salva ainda, apenas 'coloca na fila' para ser salvo

        db.session.commit() # salva no banco oq foi add na 'fila'

        return produto.json(), 200


@produto_api.route('/produto/<int:id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def pagina_produto(id):
    produto = Produto.query.get_or_404(id) #se existir o produto retorna os dados, caso contrário sai da função retornando 404

    if (request.method == 'GET'):
        return produto.json(), 200

    if (request.method == 'PATCH' or 'PUT'):
        dados = request.json

        nome = dados.get('nome', produto.nome)
        descricao = dados.get('descricao', produto.descricao)
        qnt_estoque = dados.get('qnt_estoque', produto.qnt_estoque)

        if(not isinstance(nome, str) or not isinstance(descricao, str) or not isinstance(qnt_estoque, int) 
        or len(nome) > 63 or len(descricao) > 127):

            return {"erro" : "nome, raca, porte ou data de nascimento em formato invalido"}

        produto.nome = nome
        produto.descricao = descricao
        produto.qnt_estoque = qnt_estoque

        db.session.add(produto)

    if (request.method == 'DELETE'):
        #db.session.delete(produto)
        return {"erro" : "recurso ainda nao disponivel"}

    db.session.commit() # executa no banco todas as tarefas que estavam na fila
    return produto.json(), 200
