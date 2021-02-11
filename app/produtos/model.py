from ..extensions import db

class Produto(db.Model):
    __tablename__           = 'produto'
    id                      = db.Column(db.Integer, primary_key=True)
    nome                    = db.Column(db.String(63), nullable=False)
    preco                   = db.Column(db.Float, nullable=False)
    qnt_estoque             = db.Column(db.Integer, default=0)
    descricao               = db.Column(db.String(127), default="")
    
    def json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'preco' : self.preco,
            'descricao': self.descricao,
            'qnt_estoque': self.qnt_estoque
        }