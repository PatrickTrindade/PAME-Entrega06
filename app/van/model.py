from ..extensions import db

class Van(db.Model):    
    __tablename__           = 'van'
    id                      = db.Column(db.Integer, primary_key=True)
    horario                 = db.Column(db.String(20), nullable=False)   # timestamp / add unique
    id_pet                  = db.Column(db.Integer, db.ForeignKey('pet.id'))
    descricao               = db.Column(db.String(127), default="")

    pet                     = db.relationship('Pet', backref='van')

    def json(self):
        return {
            'id': self.id,
            'horario': self.horario,
            'id_pet': self.id_pet,
            'descricao': self.descricao
        }
