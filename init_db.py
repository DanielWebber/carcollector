from app import create_app, db
from app.models import Car, User, Inventory


def seed():
    cars = [
        ('1967 Ford Mustang', 'rare', 1000, 50, 12, 220),
        ('1994 Toyota Supra', 'uncommon', 600, 30, 8, 200),
        ('2020 Tesla Model S', 'common', 300, 15, 6, 155),
        ('1957 Chevrolet Bel Air', 'rare', 900, 45, 12, 180),
        ('2010 Nissan GT-R', 'uncommon', 700, 35, 10, 210),
    ]
    for name, rarity, price, rate, duration, top_speed in cars:
        if not Car.query.filter_by(name=name).first():
            db.session.add(Car(name=name, rarity=rarity, price=price, earning_rate=rate, earning_duration_hours=duration, top_speed=top_speed))
    # create a demo user if none
    if not User.query.filter_by(username='demo').first():
        u = User(username='demo')
        u.set_password('demo123')
        u.balance = 5000000  # 5 million for modding
        db.session.add(u)
        db.session.flush()
        # seed some parts to inventory
        starter_parts = [
            ('engines', 'Stock Engine', 3),
            ('tires', 'Stock Tires', 2),
            ('turbos', 'No Turbo', 2),
            ('exhausts', 'Stock Exhaust', 1),
        ]
        for cat, part, qty in starter_parts:
            inv = Inventory(user_id=u.id, part_category=cat, part_name=part, quantity=qty)
            db.session.add(inv)
    db.session.commit()


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        seed()
        print('Initialized database and seeded cars + demo user')
