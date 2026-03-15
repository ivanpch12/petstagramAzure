import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def set_user_for_existing_photos(apps, schema_editor):
    User = apps.get_model(settings.AUTH_USER_MODEL)
    Photo = apps.get_model('photos', 'Photo')

    user = User.objects.filter(is_superuser=True).first()
    if not user:
        user = User.objects.create_superuser(
            email='admin@admin.com',
            password='admin123'
        )

    for photo in Photo.objects.all():
        photo.user = user
        photo.save()


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0003_alter_photo_photo'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='user',
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL,
                on_delete=django.db.models.deletion.CASCADE,
                null=True,
                blank=True,
            ),
        ),
        migrations.RunPython(set_user_for_existing_photos),
        migrations.AlterField(
            model_name='photo',
            name='user',
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL,
                on_delete=django.db.models.deletion.CASCADE,
            ),
        ),
    ]