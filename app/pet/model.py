from ..extensions import db

class Pet(db.Model):
    __tablename__           = 'pet'
    id                      = db.Column(db.Integer, primary_key=True)
    nome                    = db.Column(db.String(63), nullable=True) # so será utilizada se o cliente for cadastrado

    raca                    = db.Column(db.String(63), nullable=False)
    porte                   = db.Column(db.String(63), nullable=False) # pequeno / medio / grande
    data_nascimento         = db.Column(db.String(63), nullable=False) # para saber a idade do pet

    user_id                 = db.Column(db.String, db.ForeignKey('usuario.id'))


    #usuario                 = db.relationship("Usuario", backref="pets")   -> tava dando erro
    #servico                 = db.relationship("Servico", backref="pet")     -> tava dando erro


    def json(self):
        return{
            "nome": self.nome,
            "raca": self.raca,
            "porte": self.porte,
            "data_nascimento": self.data_nascimento,
            "user_id": self.user_id
        }
