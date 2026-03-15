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

    user = User.objects.filter(is_superuser=True).first()
    if not user:
        user = User.objects.create(
            email='testuser1@example.com',
            password=make_password('password123'),
            is_superuser=True
        )

    pet1, _ = Pet.objects.get_or_create(
        name='Buddy',
        personal_photo='https://i.natgeofe.com/n/4f5aaece-3300-41a4-b8a5-adfdcdbea36d/domestic-cat_thumb_3x2.jpg',
        date_of_birth='2020-05-15',
        slug=slugify('Buddy')
    )
    pet2, _ = Pet.objects.get_or_create(
        name='Whiskers',
        personal_photo='https://www.humanesociety.org/sites/default/files/styles/1240x698/public/2022-07/kitten-paws-getty-1246143529.jpg',
        date_of_birth='2019-11-20',
        slug=slugify('Whiskers')
    )
    pet3, _ = Pet.objects.get_or_create(
        name='Rocky',
        personal_photo='https://g.petango.com/photos/1090/13271871-1-pb.jpg',
        date_of_birth='2021-01-01',
        slug=slugify('Rocky')
    )

    photo1, _ = Photo.objects.get_or_create(
        photo='photos/dog_park.jpg',
        description='A happy dog playing in the park.',
        location='Central Park'
    )
    photo1.tagged_pets.add(pet1)

    photo2, _ = Photo.objects.get_or_create(
        photo='photos/cat_couch.jpg',
        description='Cute cat napping on the couch.',
        location='Home'
    )
    photo2.tagged_pets.add(pet2)

    photo3, _ = Photo.objects.get_or_create(
        photo='photos/rocky_walk.jpg',
        description='Rocky enjoying his morning walk.',
        location='Mountain Trail'
    )
    photo3.tagged_pets.add(pet3)

    Comment.objects.get_or_create(
        text='What a lovely dog!',
        to_photo=photo1,
        user=user
    )
    Comment.objects.get_or_create(
        text='So sleepy and cute!',
        to_photo=photo2,
        user=user
    )

    Like.objects.get_or_create(to_photo=photo1, user=user)
    Like.objects.get_or_create(to_photo=photo2, user=user)


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0001_initial'),
        ('photos', '0001_initial'),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_sample_data),
    ]