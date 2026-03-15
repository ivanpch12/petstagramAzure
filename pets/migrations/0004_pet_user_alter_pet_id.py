import django.db.models.deletion
from django.db import migrations, models


def set_user_for_existing_pets(apps, schema_editor):
    User = apps.get_model('accounts', 'AppUser')  # Точно app label + Model
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
        migrations.swappable_dependency('accounts.AppUser'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.AppUser'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pet',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.RunPython(set_user_for_existing_pets),
    ]