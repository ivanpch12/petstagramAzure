import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def set_user_for_existing_pets(apps, schema_editor):
    User = apps.get_model(settings.AUTH_USER_MODEL)
    Pet = apps.get_model('pets', 'Pet')

    user = User.objects.filter(is_superuser=True).first()
    if not user:
        user = User.objects.create_superuser(
            email='admin@admin.com',
            password='admin123'
        )

    for pet in Pet.objects.all():
        pet.user = user
        pet.save()


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0003_populate_pet_model'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='user',
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL,
                on_delete=django.db.models.deletion.CASCADE,
                null=True,
                blank=True,
            ),
        ),
        migrations.RunPython(set_user_for_existing_pets),
        migrations.AlterField(
            model_name='pet',
            name='user',
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL,
                on_delete=django.db.models.deletion.CASCADE,
            ),
        ),
    ]