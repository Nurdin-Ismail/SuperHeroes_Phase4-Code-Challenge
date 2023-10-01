from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'
     
    serialize_rules= ('-created_at', '-updated_at','-powers.heroes', '-hero_power')
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String)
    super_name = db.Column(db.String, unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    hero_power = db.relationship("HeroPower", backref='hero')

    powers = db.relationship('Power', secondary = 'hero_powers', back_populates='heroes')
    
    
    def __repr__(self):
        return f'(id={self.id}, name={self.name} super_name={self.super_name})'
    
class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'
    
    
    serialize_rules= ('-created_at', '-updated_at','-heroes.powers' )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    heroes = db.relationship('Hero', secondary = 'hero_powers', back_populates='powers')
    
    
    
    def __repr__(self):
        return f'(id={self.id}, name={self.name} description={self.description})'

    @validates('description')
    def checks_description(self, key, description):
        if len(description) < 20:
            raise ValueError("Description must be longer than 20 chars")
        else:
            return description


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'
    
    serialize_rules= ('-created_at', '-updated_at', '-hero.hero_power')

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    hero_id = db.Column(db.String, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.String, db.ForeignKey('powers.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    

    def __repr__(self):
        return f'(id={self.id}, heroID={self.hero_id} strength={self.strength}) powerID={self.power_id}'

    @validates('strength')
    def checks_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be a value either 'Strong', 'Weak' or 'Average'")
        else:
            return strength
# add any models you may need. 