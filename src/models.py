from gino.ext.sanic import Gino

db = Gino()

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)

    def __repr__(self):
        return f'<Event: {self.name}>'


class Participant(db.Model):
    __tablename__ = 'participants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)
    email = db.Column(db.Unicode)
    phone_1 = db.Column(db.Unicode)
    phone_2 = db.Column(db.Unicode)
    age = db.Column(db.Integer)
    payment_proof = db.Column(db.Unicode)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    @property
    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'event': self.event_id
        }

    def __repr__(self):
        return f'<Participant: {self.email} - {self.event.name}>'

