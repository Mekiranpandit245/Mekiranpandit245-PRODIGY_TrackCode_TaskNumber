import datetime

class User:
    def __init__(self, user_id, username, profile_picture=None):
        self.user_id = user_id
        self.username = username
        self.profile_picture = profile_picture
        self.posts = []
        self.followers = []
        self.following = []

    def create_post(self, content, media=None, tags=None):
        post = Post(len(self.posts) + 1, self, content, media, tags)
        self.posts.append(post)
        return post

    def follow(self, other_user):
        if other_user != self and other_user not in self.following:
            self.following.append(other_user)
            other_user.followers.append(self)

    def unfollow(self, other_user):
        if other_user in self.following:
            self.following.remove(other_user)
            other_user.followers.remove(self)

    def __str__(self):
        return f"User(id={self.user_id}, username='{self.username}')"

class Post:
    def __init__(self, post_id, author, content, media=None, tags=None):
        self.post_id = post_id
        self.author = author
        self.content = content
        self.media = media  # Image/video file path or URL
        self.tags = tags or []  # List of tagged users
        self.likes = []
        self.comments = []
        self.timestamp = datetime.datetime.now()

    def like(self, user):
        if user not in self.likes:
            self.likes.append(user)

    def unlike(self, user):
        if user in self.likes:
            self.likes.remove(user)

    def add_comment(self, user, text):
        comment = Comment(user, text)
        self.comments.append(comment)
        return comment

    def __str__(self):
        return f"Post(id={self.post_id}, author={self.author.username}, content='{self.content[:20]}...', likes={len(self.likes)}, comments={len(self.comments)})"

class Comment:
    def __init__(self, user, text):
        self.user = user
        self.text = text
        self.timestamp = datetime.datetime.now()

    def __str__(self):
        return f"Comment(user={self.user.username}, text='{self.text}')"

class SocialMediaApp:
    def __init__(self):
        self.users = {}
        self.posts = []

    def create_user(self, user_id, username, profile_picture=None):
        if user_id not in self.users:
            user = User(user_id, username, profile_picture)
            self.users[user_id] = user
            return user
        else:
            return None

    def get_user(self, user_id):
        return self.users.get(user_id)

    def add_post(self, post):
        self.posts.append(post)

    def get_all_posts(self):
        return sorted(self.posts, key=lambda post: post.timestamp, reverse=True)

    def get_user_posts(self, user_id):
        user = self.get_user(user_id)
        if user:
            return sorted(user.posts, key=lambda post: post.timestamp, reverse=True)
        else:
            return []

    def get_trending_posts(self):
        # Simple trending based on like and comment count (can be improved)
        return sorted(self.posts, key=lambda post: len(post.likes) + len(post.comments), reverse=True)[:10] #top 10 trending.

# Example Usage
app = SocialMediaApp()

user1 = app.create_user(1, "Alice", "alice.jpg")
user2 = app.create_user(2, "Bob", "bob.png")
user3 = app.create_user(3, "Charlie", "charlie.jpeg")

post1 = user1.create_post("Hello, world!", "image.jpg", [user2])
post2 = user2.create_post("Python is fun!", "video.mp4")
post3 = user3.create_post("Just had amazing coffee.")

app.add_post(post1)
app.add_post(post2)
app.add_post(post3)

post1.like(user2)
post1.add_comment(user3, "Nice post!")
post2.like(user1)

user1.follow(user2)
user2.follow(user3)

print("All Posts:")
for post in app.get_all_posts():
    print(post)

print("\nAlice's Posts:")
for post in app.get_user_posts(1):
    print(post)

print("\nTrending Posts:")
for post in app.get_trending_posts():
    print(post)

print(f"\n{user2.username}'s Followers: {[follower.username for follower in user2.followers]}")
print(f"{user1.username}'s Following: {[following.username for following in user1.following]}")