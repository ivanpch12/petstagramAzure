import django.db.models.deletion
from django.db import migrations, models
from django.conf import settings


def set_user_for_existing_pets(apps, schema_editor):
    User = apps.get_model('accounts', 'AppUser')
    Pet = apps.get_model('pets', 'Pet')

    superuser = User.objects.filter(is_superuser=True).first()
    if not superuser:
        superuser = User.objects.create(
            email='admin@admin.com',
            password='!',
            is_superuser=True
        )

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
        migrations.AlterField(
            model_name='pet',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]