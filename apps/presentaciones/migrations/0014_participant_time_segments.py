# Generated migration for adding time_segments field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presentaciones', '0013_presentation_cloudinary_public_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='time_segments',
            field=models.JSONField(blank=True, default=list, help_text="Intervalos de tiempo donde aparece (formato: [{'start': 10.5, 'end': 25.3}, ...])", verbose_name='Segmentos de tiempo'),
        ),
    ]
