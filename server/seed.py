from app import app
from models import Blogpost, User, User_blogposts, db
from faker import Faker
import random

# Create a Faker instance
fake = Faker()

with app.app_context():
    # Clear existing data
    User_blogposts.query.delete()
    User.query.delete()
    Blogpost.query.delete()

    print("🦸‍♀️ Seeding blogposts...")

    blogposts_data = [
        {"name": "la fashion", "description": "gives French vibes"},
        {"name": "Bleeding ink", "description": "bringing your stories to life"},
        {"name": "The Blog Business", "description": "keeping you updated on the business world"},
        {"name": "Glam up", "description": "here to assert drip is for life"},
        {"name": "NatureScribblings", "description": "Nature is beautiful"},
        {"name": "Sage's corner", "description": "a look into Sage's fabulous lifestyle"},
        {"name": "Beauty secrets", "description": "Open a door to vast knowledge in skincare"},
        {"name": "Hiking Diary", "description": "Discover the world's best hiking grounds"},
        {"name": "Analog blog", "description": "Travel back to reminisce ancient cultures"},
        {"name": "Chocolate Fanatic", "description": "chocolate discovery "},
        {"name": "Seaman tales", "description": "underwater chronicles"},
        {"name": "City food", "description": "a plug to your go-to food places"},
        {"name": "Basqueparfum", "description": "let your scent tell your story"},
    ]

    for data in blogposts_data:
        blogpost = Blogpost(**data)
        db.session.add(blogpost)

    db.session.commit()

    print("🦸‍♀️ Adding users...")

    # Generate and add fake users
    for _ in range(12):  
        username = fake.user_name()
        email = fake.email()
        user = User(username=username, email=email)
        db.session.add(user)

    db.session.commit()

    print("🦸‍♀️ Adding blogposts to users...")

    ratings = ["Good", "Awesome", "Fantastic"]

    users = User.query.all()
    blogposts = Blogpost.query.all()

    for user in users:
        for _ in range(random.randint(1, 3)):
            blogpost = random.choice(blogposts)
            rating = random.choice(ratings)

            user_blogpost = User_blogposts(user_id=user.id, blogpost_id=blogpost.id, rating=rating)
            db.session.add(user_blogpost)

    db.session.commit()

    print("🦸‍♀️ Done seeding!")
