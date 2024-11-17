from datetime import datetime, timedelta
import random
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import User, Post
from app import db

app = create_app()

# Example user personalities with their typical posting styles
USERS = [
    {
        "username": "techie_sarah",
        "password": "Tech123!",
        "email": "sarah@example.com",
        "bio": "Software engineer by day, indie game dev by night. Always learning!",
        "posts": [
            "Just deployed my first Kubernetes cluster! The learning curve was worth it.",
            "Working on a new pixel art game. Here's a sneak peek of the mechanics I'm building!",
            "TIL about Python's walrus operator. Mind = blown! ",
            "Who else is excited about the new Rust features?",
            "Coffee + Code = Perfect Sunday ",
            "Debugging this recursive algorithm for 3 hours. The solution was so simple! ",
            "Started contributing to open source today. Small PR but feeling accomplished! "
        ]
    },
    {
        "username": "fitness_mike",
        "password": "Fit2024!",
        "email": "mike@example.com",
        "bio": "Personal trainer Helping you achieve your fitness goals! ",
        "posts": [
            "Morning workout complete! 5-mile run and HIIT session. Who's with me? ",
            "Pro tip: Don't forget to stretch after your workouts! Flexibility is key ",
            "New PR on deadlifts today! 315lbs x 5 ",
            "Meal prep Sunday! Chicken, sweet potatoes, and lots of veggies ",
            "Rest days are as important as workout days. Listen to your body! ",
            "Quick 20-min home workout: 50 pushups, 50 squats, 30 burpees. Try it! "
        ]
    },
    {
        "username": "foodie_lisa",
        "password": "Yummy2024!",
        "email": "lisa@example.com",
        "bio": "Food blogger Recipe developer Living life one bite at a time!",
        "posts": [
            "Made the perfect croissants today! Third time's the charm ",
            "Testing a new ramen recipe. The secret is in the broth! ",
            "Found the cutest little farmers market! Fresh ingredients incoming ",
            "Who wants the recipe for my famous chocolate chip cookies? ",
            "Food photography tip: Natural light is your best friend! ",
            "Pizza night! Made the dough from scratch "
        ]
    },
    {
        "username": "travel_tom",
        "password": "Wanderlust24!",
        "email": "tom@example.com",
        "bio": "Digital nomad Currently in: Bali Next stop: Japan ",
        "posts": [
            "Sunrise at Mount Batur. Worth the 3am wake-up call! ",
            "Found this hidden waterfall on today's hike. Bali never ceases to amaze! ",
            "Local street food tour in Ubud. My taste buds are dancing! ",
            "Working from a beach cafe today. Living the dream! ",
            "Booked my tickets to Japan! Cherry blossom season, here I come! ",
            "Pro tip: Always carry a portable charger when traveling! Saved me today "
        ]
    },
    {
        "username": "artist_emma",
        "password": "Create2024!",
        "email": "emma@example.com",
        "bio": "Digital artist Commission slots open! Living in colors",
        "posts": [
            "Just finished this commission piece! Love how the colors turned out ",
            "Working on a new character design. Sketching phase is my favorite! ",
            "Art supply haul! Can't wait to try these new brushes ",
            "Time-lapse of today's painting coming soon! ",
            "Sometimes the best art comes from mistakes. Embrace the imperfections! ",
            "Started learning 3D modeling. This is harder than I thought! "
        ]
    },
    {
        "username": "gamer_alex",
        "password": "Player2024!",
        "email": "alex@example.com",
        "bio": "Pro gamer Twitch streamer Always in game",
        "posts": [
            "Epic win in today's tournament! GG everyone! ",
            "New gaming setup complete! RGB everything! ",
            "12-hour stream starting in 30 minutes! Come hang out ",
            "That new game update though! Time to grind some levels ",
            "Anyone up for some multiplayer? Drop your username! ",
            "Just hit Diamond rank! The grind was worth it! "
        ]
    },
    {
        "username": "chef_david",
        "password": "Cook2024!",
        "email": "david@example.com",
        "bio": "Professional chef Food is love Recipe developer",
        "posts": [
            "New menu testing day at the restaurant! So many flavors ",
            "The secret to perfect pasta? It's all in the sauce! ",
            "Kitchen hack: Keep your knives sharp! A dull knife is dangerous ",
            "Today's special: Truffle risotto with wild mushrooms ",
            "Behind the scenes of a professional kitchen. Chaos and creativity! ",
            "Teaching a cooking class tonight! Excited to share some techniques "
        ]
    },
    {
        "username": "bookworm_nina",
        "password": "Read2024!",
        "email": "nina@example.com",
        "bio": "Book reviewer Fantasy lover Lost in pages",
        "posts": [
            "Just finished this amazing fantasy novel! No spoilers but WOW! ",
            "Current reading spot: cozy corner + rain + tea = perfect! ",
            "Monthly TBR pile ready! Which one should I start with? ",
            "Book mail day is the best day! ",
            "That plot twist though! Still processing... ",
            "Starting a virtual book club! Who wants to join? "
        ]
    },
    {
        "username": "music_ray",
        "password": "Beats2024!",
        "email": "ray@example.com",
        "bio": "Music producer Guitar teacher Living in rhythm",
        "posts": [
            "New track dropping next week! Can't wait to share it! ",
            "Studio session was fire today! The beat is coming together ",
            "Teaching my students about jazz theory. Music is math! ",
            "New guitar day! This tone is everything ",
            "Collaborating with some amazing artists. Stay tuned! ",
            "Live performance this weekend! Come through! "
        ]
    },
    {
        "username": "nature_pat",
        "password": "Earth2024!",
        "email": "pat@example.com",
        "bio": "Wildlife photographer Nature lover Conservation advocate",
        "posts": [
            "Captured this stunning sunset in the mountains today ",
            "Spotted a rare bird species! Nature never ceases to amaze ",
            "Remember: Take only pictures, leave only footprints ",
            "Early morning hike = best way to start the day ",
            "Working on a photo series about local wildlife ",
            "Found some beautiful wildflowers on today's nature walk "
        ]
    }
]

def create_test_data():
    print("Creating test users and posts...")
    
    # Clear existing data
    Post.query.delete()
    User.query.delete()
    
    for user_data in USERS:
        # Create user
        user = User(
            username=user_data["username"],
            email=user_data["email"],
            bio=user_data["bio"]
        )
        user.set_password(user_data["password"])
        db.session.add(user)
        db.session.commit()
        
        # Create posts for user
        available_posts = len(user_data["posts"])
        num_posts = min(random.randint(5, 10), available_posts)
        posts = random.sample(user_data["posts"], num_posts)
        
        # Generate random timestamps within the last week
        now = datetime.utcnow()
        for post_content in posts:
            random_hours = random.randint(0, 168)  # Within last week (7 * 24 = 168 hours)
            timestamp = now - timedelta(hours=random_hours)
            
            post = Post(
                body=post_content,
                timestamp=timestamp,
                user_id=user.id
            )
            db.session.add(post)
        
        # Make users follow each other randomly
        other_users = User.query.filter(User.id != user.id).all()
        for other_user in other_users:
            if random.random() < 0.7:  # 70% chance to follow
                user.follow(other_user)
    
    db.session.commit()
    print("Test data created successfully!")
    print("\nExample Users:")
    for user in USERS:
        print(f"Username: {user['username']}")
        print(f"Password: {user['password']}")
        print("---")

if __name__ == "__main__":
    with app.app_context():
        create_test_data()
