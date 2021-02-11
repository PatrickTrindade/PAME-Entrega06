from ..extensions import db

class Servico(db.Model):
    __tablename__           = 'servico'
    id                      = db.Column(db.Integer, primary_key=True)
    nome                    = db.Column(db.String(63), nullable=False)  # banho / tosa
    horario                 = db.Column(db.String(20), nullable=False)  # timestamp
    pet_id                  = db.Column(db.Integer, db.ForeignKey('pet.id'))
    descricao               = db.Column(db.String(127), default="")
        
    pet                     = db.relationship("Pet", backref="servico")

    def json(self):
        return{
            "nome": self.nome,
            "horario": self.horario,
            "descricao": self.descricao
        }

