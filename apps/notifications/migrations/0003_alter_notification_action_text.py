# Generated manually to fix action_text field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_alter_notification_action_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='action_text',
            field=models.CharField(blank=True, null=True, max_length=100, verbose_name='Texto del botón'),
        ),
    ]