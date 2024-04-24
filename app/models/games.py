from .db import db


class Game(db.Model):
    __tablename__ = "game"

    game_store_association = db.Table(
        'game_store',
        db.Column('game_id', db.Integer, db.ForeignKey(
            'game.id'), primary_key=True),
        db.Column('store_id', db.Integer, db.ForeignKey(
            'store.id'), primary_key=True)
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    release_date = db.Column(db.Date, nullable=True)
    stores = db.relationship('Store', secondary=game_store_association,
                             backref=db.backref('games', lazy='dynamic'))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "genre": self.genre,
            "price": self.price,
            "release_date": self.release_date,
        }
