from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

def set_user_for_existing_pets(apps, schema_editor):
    User = apps.get_model(settings.AUTH_USER_MODEL.split('.')[-1].capitalize(), settings.AUTH_USER_MODEL.split('.')[0])
    Pet = apps.get_model('pets', 'Pet')
    superuser = User.objects.filter(is_superuser=True).first()
    if superuser:
        for pet in Pet.objects.all():
            pet.user = superuser
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
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunPython(set_user_for_existing_pets),
        migrations.AlterField(
            model_name='pet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]