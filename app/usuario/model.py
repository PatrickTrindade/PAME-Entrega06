from ..extensions import db

class Usuario(db.Model):
    __tablename__           = 'usuario'
    id                      = db.Column(db.Integer, primary_key=True)
    username                = db.Column(db.String(63), nullable=False, unique=True)
    senha                   = db.Column(db.String(63), nullable=False) # mudar para salvar um hash e não a senha de fato
    nome                    = db.Column(db.String(63), nullable=False)
    endereco                = db.Column(db.String(127), nullable=False)
    email                   = db.Column(db.String(63), nullable=False, unique=True) # unique -> true

    pets                    = db.relationship("Pet", backref="usuario")

    def json(self):
        return{
            "username": self.username,
            "nome": self.nome,
            "endereco": self.endereco,
            "email": self.email
        } # nao retorna senha propositalmente