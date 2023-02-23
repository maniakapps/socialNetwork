from django.contrib.auth.models import User
from faker import Faker

from myapp.models import Post, Comment

fake = Faker()

# Create a new user with a fake name, email, and password
user = User.objects.create_user(
    username=fake.user_name(),
    email=fake.email(),
    password=fake.password()
)

# Create a new post with fake content, image, and date
post = Post.objects.create(
    user=user,
    content=fake.paragraph(),
    image=fake.image_url(),
    created_at=fake.date_time_this_month()
)

# Create a new comment with fake content and date
comment = Comment.objects.create(
    user=user,
    post=post,
    content=fake.sentence(),
    created_at=fake.date_time_this_month()
)
