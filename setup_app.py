import os
import shutil

# Create models.py
models_content = '''from . import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

CAR_PARTS = {
    "engines": {"Stock Engine": {"power": 0, "price": 0, "rarity": "Common"}, "Honda K20A": {"power": 15, "price": 45000, "rarity": "Uncommon"}, "Honda K24A": {"power": 20, "price": 55000, "rarity": "Uncommon"}, "Mitsubishi 4G63T": {"power": 25, "price": 65000, "rarity": "Rare"}, "Toyota 2JZ-GTE": {"power": 40, "price": 180000, "rarity": "Epic"}, "Nissan RB26DETT": {"power": 35, "price": 160000, "rarity": "Epic"}, "BMW S54B32": {"power": 45, "price": 200000, "rarity": "Epic"}, "Mercedes AMG M159": {"power": 80, "price": 800000, "rarity": "Legendary"}, "Ferrari F140 V12": {"power": 100, "price": 1500000, "rarity": "Mythical"}, "Koenigsegg V8 Twin-Turbo": {"power": 200, "price": 10000000, "rarity": "Transcendent"}},
    "engine_blocks": {"Stock Cast Iron Block": {"strength": 0, "weight_reduction": 0, "price": 0, "rarity": "Common"}, "Aluminum Block": {"strength": 8, "weight_reduction": 15, "price": 35000, "rarity": "Uncommon"}, "A356 Aluminum Block": {"strength": 15, "weight_reduction": 20, "price": 65000, "rarity": "Rare"}, "Forged Aluminum Block": {"strength": 22, "weight_reduction": 25, "price": 120000, "rarity": "Epic"}, "Carbon Fiber Block": {"strength": 45, "weight_reduction": 60, "price": 800000, "rarity": "Legendary"}},
    "tires": {"Stock Tires": {"grip": 0, "price": 0, "rarity": "Common"}, "Michelin Pilot Sport 4S": {"grip": 8, "price": 2500, "rarity": "Uncommon"}, "Bridgestone Potenza RE-71R": {"grip": 12, "price": 3500, "rarity": "Rare"}, "Hoosier A7 Racing Slicks": {"grip": 25, "price": 8000, "rarity": "Epic"}, "Michelin Pilot Sport Cup 2 R": {"grip": 40, "price": 15000, "rarity": "Mythical"}},
    "turbos": {"No Turbo": {"boost": 0, "price": 0, "rarity": "Common"}, "Garrett GT2860RS": {"boost": 12, "price": 85000, "rarity": "Uncommon"}, "BorgWarner EFR 7670": {"boost": 25, "price": 180000, "rarity": "Rare"}, "Precision Turbo 6266": {"boost": 40, "price": 350000, "rarity": "Epic"}, "Garrett GT3582R": {"boost": 50, "price": 500000, "rarity": "Legendary"}},
    "nos": {"No NOS": {"nitrous": 0, "price": 0, "rarity": "Common"}, "NOS 50hp Wet Kit": {"nitrous": 50, "price": 45000, "rarity": "Uncommon"}, "ZEX 100hp Wet Kit": {"nitrous": 100, "price": 85000, "rarity": "Rare"}, "Nitrous Express 200hp": {"nitrous": 200, "price": 180000, "rarity": "Epic"}, "ZEX 500hp Professional": {"nitrous": 500, "price": 750000, "rarity": "Mythical"}},
    "exhausts": {"Stock Exhaust": {"sound": 0, "power": 0, "price": 0, "rarity": "Common"}, "Borla ATAK Cat-Back": {"sound": 2, "power": 8, "price": 12000, "rarity": "Uncommon"}, "Akrapovic Evolution": {"sound": 4, "power": 20, "price": 35000, "rarity": "Epic"}, "Fi Exhaust Full System": {"sound": 5, "power": 30, "price": 65000, "rarity": "Legendary"}, "Capristo Carbon Titanium": {"sound": 6, "power": 45, "price": 150000, "rarity": "Mythical"}},
    "suspension": {"Stock Suspension": {"handling": 0, "price": 0, "rarity": "Common"}, "KW V1 Coilovers": {"handling": 12, "price": 25000, "rarity": "Rare"}, "Ohlins Road & Track": {"handling": 22, "price": 55000, "rarity": "Epic"}, "AST 5100 Series": {"handling": 35, "price": 120000, "rarity": "Legendary"}, "Penske Racing Shocks": {"handling": 50, "price": 300000, "rarity": "Mythical"}},
    "engine_internals": {"Stock Internals": {"reliability": 0, "price": 0, "rarity": "Common"}, "Skunk2 Pro Series Cams": {"reliability": 10, "price": 25000, "rarity": "Uncommon"}, "Manley H-Beam Rods": {"reliability": 18, "price": 45000, "rarity": "Rare"}, "JE Pistons Pro Series": {"reliability": 30, "price": 85000, "rarity": "Epic"}, "Cosworth Forged Pistons": {"reliability": 50, "price": 250000, "rarity": "Legendary"}}
}

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    balance = db.Column(db.Integer, default=0)
    bio = db.Column(db.String(500), default="")
    avatar_url = db.Column(db.String(500), default="https://via.placeholder.com/50")
    cars = db.relationship("UserCar", backref="user", lazy=True)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    rarity = db.Column(db.String(20), default="common")
    price = db.Column(db.Integer)
    earning_rate = db.Column(db.Integer, default=0)
    earning_duration_hours = db.Column(db.Integer, default=0)
    top_speed = db.Column(db.Integer, default=0)

class UserCar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey("car.id"), nullable=False)
    car = db.relationship("Car")
    is_touring = db.Column(db.Boolean, default=False)
    tour_start = db.Column(db.DateTime, nullable=True)
    tour_duration_hours = db.Column(db.Integer, nullable=True)
    last_claimed_at = db.Column(db.DateTime, nullable=True)
    engine_mod = db.Column(db.String(120), default="Stock Engine")
    engine_block_mod = db.Column(db.String(120), default="Stock Cast Iron Block")
    tire_mod = db.Column(db.String(120), default="Stock Tires")
    turbo_mod = db.Column(db.String(120), default="No Turbo")
    nos_mod = db.Column(db.String(120), default="No NOS")
    exhaust_mod = db.Column(db.String(120), default="Stock Exhaust")
    suspension_mod = db.Column(db.String(120), default="Stock Suspension")
    engine_internals_mod = db.Column(db.String(120), default="Stock Internals")
    def start_tour(self, hours):
        hours = min(int(hours), 24)
        self.is_touring = True
        self.tour_start = datetime.utcnow()
        self.tour_duration_hours = hours
        self.last_claimed_at = None
    def claim_earnings(self):
        if not self.is_touring or not self.tour_start:
            return 0
        now = datetime.utcnow()
        last = self.last_claimed_at or self.tour_start
        hours_to_claim = (now - last).total_seconds() / 3600
        finish_time = self.tour_start + timedelta(hours=self.tour_duration_hours)
        rate = self.car.earning_rate or 0
        earnings = int(hours_to_claim * rate)
        self.last_claimed_at = now
        if now >= finish_time:
            self.is_touring = False
        return earnings
    def get_total_hp(self):
        total = 0
        part_map = {"engines": (self.engine_mod, "power"), "engine_blocks": (self.engine_block_mod, "strength"), "exhausts": (self.exhaust_mod, "power"), "turbos": (self.turbo_mod, "boost"), "nos": (self.nos_mod, "nitrous"), "engine_internals": (self.engine_internals_mod, "reliability")}
        for cat, (part_name, attr) in part_map.items():
            if part_name in CAR_PARTS.get(cat, {}):
                total += CAR_PARTS[cat][part_name].get(attr, 0)
        return total
    def get_total_torque(self):
        return int(self.get_total_hp() * 0.75)
    def sell_price(self):
        base = int(self.car.price * 0.5)
        mod_bonus = int(self.get_total_hp() * 100)
        return base + mod_bonus

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    username = db.Column(db.String(80), nullable=True)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class Race(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    challenger_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    opponent_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    challenger_car_id = db.Column(db.Integer, db.ForeignKey("car.id"))
    opponent_car_id = db.Column(db.Integer, db.ForeignKey("car.id"), nullable=True)
    status = db.Column(db.String(20), default="open")
    winner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    part_category = db.Column(db.String(80), nullable=False)
    part_name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, default=1)

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
'''

with open('app/models.py', 'w') as f:
    f.write(models_content)

print("Created app/models.py with Inventory model")
