from django.db import migrations
from django.contrib.auth import get_user_model
from django.utils.text import slugify # Added slugify import


from django.db import migrations
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.utils.text import slugify


def create_sample_data(apps, schema_editor):
    User = apps.get_model(settings.AUTH_USER_MODEL)
    Pet = apps.get_model('pets', 'Pet')
    Photo = apps.get_model('photos', 'Photo')
    Comment = apps.get_model('common', 'Comment')
    Like = apps.get_model('common', 'Like')

    user1, created = User.objects.get_or_create(
        email='testuser1@example.com',
        defaults={'password': make_password('password123')}
    )

    user2, created = User.objects.get_or_create(
        email='testuser2@example.com',
        defaults={'password': make_password('password123')}
    )

    # Create Pets
    pet1, created = Pet.objects.get_or_create(
        name='Buddy',
        personal_photo='https://i.natgeofe.com/n/4f5aaece-3300-41a4-b8a5-adfdcdbea36d/domestic-cat_thumb_3x2.jpg',
        date_of_birth='2020-05-15',
        slug=slugify('Buddy') # Explicitly set slug
    )
    pet2, created = Pet.objects.get_or_create(
        name='Whiskers',
        personal_photo='https://www.humanesociety.org/sites/default/files/styles/1240x698/public/2022-07/kitten-paws-getty-1246143529.jpg',
        date_of_birth='2019-11-20',
        slug=slugify('Whiskers') # Explicitly set slug
    )
    pet3, created = Pet.objects.get_or_create(
        name='Rocky',
        personal_photo='https://g.petango.com/photos/1090/13271871-1-pb.jpg',
        date_of_birth='2021-01-01',
        slug=slugify('Rocky') # Explicitly set slug
    )

    # Create Photos
    photo1, created = Photo.objects.get_or_create(
        photo='photos/dog_park.jpg', # Dummy file path
        description='A happy dog playing in the park.',
        location='Central Park'
    )
    if created:
        photo1.tagged_pets.add(pet1)
    photo2, created = Photo.objects.get_or_create(
        photo='photos/cat_couch.jpg', # Dummy file path
        description='Cute cat napping on the couch.',
        location='Home'
    )
    if created:
        photo2.tagged_pets.add(pet2)
    photo3, created = Photo.objects.get_or_create(
        photo='photos/rocky_walk.jpg', # Dummy file path
        description='Rocky enjoying his morning walk.',
        location='Mountain Trail'
    )
    if created:
        photo3.tagged_pets.add(pet3)

    # Create Comments
    comment1, created = Comment.objects.get_or_create(
        text='What a lovely dog!',
        to_photo=photo1
    )
    comment2, created = Comment.objects.get_or_create(
        text='So sleepy and cute!',
        to_photo=photo2
    )

    # Create Likes
    like1, created = Like.objects.get_or_create(to_photo=photo1)
    like2, created = Like.objects.get_or_create(to_photo=photo2)


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0001_initial'),
        ('photos', '0001_initial'), # Add dependency for photos app
        ('common', '0001_initial'), # Add dependency for common app
    ]

    operations = [
        migrations.RunPython(create_sample_data),
    ]
