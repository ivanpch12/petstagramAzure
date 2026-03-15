from django.conf import settings
from django.db import migrations, models


def assign_superuser_to_pets(apps, schema_editor):
    Pet = apps.get_model('pets', 'Pet')
    User = apps.get_model(settings.AUTH_USER_MODEL)

    user = User.objects.filter(is_superuser=True).first()
    if not user:
        user = User.objects.create_superuser(email='admin@admin.com', password='password123')

    for pet in Pet.objects.all():
        if not pet.user_id:
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
                null=True,
                on_delete=models.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(assign_superuser_to_pets),
        migrations.AlterField(
            model_name='pet',
            name='user',
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]