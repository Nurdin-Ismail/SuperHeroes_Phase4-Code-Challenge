#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource


from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

@app.route('/')
def home():
    response = {
        "Message":"Heroes and Powers API.",
        "Heroes_Endpoint": '/heroes',
        "Powers_Endpoint": '/powers',
        }
    return make_response(response, 200)


class Heroes(Resource):
    # Queries for all records for restaurants
    def get(self):
        heroes = []
        for hero in Hero.query.all():
            hero_dict = {
                'id' : hero.id,
                'name' : hero.name,
                'super_name' : hero.super_name
                
            }
            
            heroes.append(hero_dict)
        return make_response(jsonify(heroes), 200)

api.add_resource(Heroes, '/heroes')

class HerobyID(Resource):
    # Queries for specific restaurant and either gets them or deletes them based o the HTTP verb
    def get(self, id):
        hero = Hero.query.filter_by(id=id).first()
        if hero:
             hero_dict =hero.to_dict()
             return make_response(jsonify(hero_dict), 200)
        else:
            response = { "error": "hero you are trying to get DOES NOT EXIST" }
            return make_response(response,404)
        
        
    
    def delete(self,id):
        # Queries for specified restaurant
        hero = Hero.query.filter_by(id=id).first()
        # Queries for all records with specified restaurant id
        hero_powers = HeroPower.query.filter_by(hero_id = hero.id).all()
        if hero_powers:
            
            # Deletes all records containing the restaurant's id
            for n in hero_powers:
                
                db.session.delete(n)
                db.session.commit()
        
        # Checks if restaurant is real and if it is, then it 
        # Deletes the restaurant and returns successful response
        if hero:
            db.session.delete(hero)
            db.session.commit()
            hero = Hero.query.filter_by(id=id).first()
            
            if not hero:
                responso = {
                "delete-successful":True,
                "message": "hero deleted"
            }
                return make_response(jsonify(responso))

            
        
        else:
            response = { "error": "hero you are trying to delete DOES NOT EXIST" }
            return make_response(response,404)


api.add_resource(HerobyID, '/heroes/<int:id>')

class Powers(Resource):
    # Queries for all power records and returns them as a response
    def get(self):
        powers = []
        for power in Power.query.all():
            power_dict = {
                'id' : power.id,
                'name' : power.name,
                'description' : power.description
            }
            
            powers.append(power_dict)
        return make_response(jsonify(powers), 200)
    
api.add_resource(Powers, '/powers')


class PowerByID(Resource):
    def get(self, id):
        power = Power.query.filter_by(id=id).first()
        if power:
             power_dict =power.to_dict()
             return make_response(jsonify(power_dict), 200)
        else:
            response = { "error": "power you are trying to get DOES NOT EXIST" }
            return make_response(response,404)
     
    def patch(self, id):
        record = Power.query.filter_by(id=id).first()
        for attr in request.form:
            setattr(record, attr, request.form[attr])

        db.session.add(record)
        db.session.commit()

        response_dict = record.to_dict()

        response = make_response(
            jsonify(response_dict),
            200
        ) 
        
        return response  
    

api.add_resource(PowerByID, '/powers/<int:id>')

class HeroPowers(Resource):
    
    def post(self):
        hero_power = HeroPower(
            
            power_id= request.form.get('power_id'),
            hero_id=request.form.get('hero_id'),
            strength =request.form.get('strength'),
        
        )
        
        
        db.session.add(hero_power)
        db.session.commit()

        # Turns record data into a dictionary
        
        if hero_power:
            hp_dict = hero_power.to_dict()
            # send back a response with the data related to the hero
            return make_response(hp_dict['hero'],201)
        else:
            response ={"errors": ["validation errors"] }
            return make_response(hero_power, 404)
    
api.add_resource(HeroPowers, '/hero_powers')


if __name__ == '__main__':
    app.run(port=5555)
