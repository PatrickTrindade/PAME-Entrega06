from ..extensions import db

class Servico(db.Model):
    __tablename__           = 'servico'
    id                      = db.Column(db.Integer, primary_key=True)
    horario                 = db.Column(db.String(20), nullable=False)  # timestamp
    pet_id                  = db.Column(db.Integer, db.ForeignKey('pet.id'))
    banho                   = db.Column(db.Boolean, default=False)
    tosa                    = db.Column(db.Boolean, default=False)
    descricao               = db.Column(db.String(127), default="")
        
    pet                     = db.relationship("Pet", backref="servico")

    def json(self):
        return{
            "horario": self.horario,
            "pet_id": self.pet_id,
            "banho": self.banho,
            "tosa": self.tosa,
            "descricao": self.descricao
        }

