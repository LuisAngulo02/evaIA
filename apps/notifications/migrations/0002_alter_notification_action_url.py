# Generated manually to fix action_url field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='action_url',
            field=models.URLField(blank=True, null=True, verbose_name='URL de acción'),
        ),
    ]