# Generated by Django 5.1.3 on 2025-01-21 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FiloArtsPlus', '0003_drawing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drawing',
            name='drawing_img',
            field=models.ImageField(upload_to=''),
        ),
    ]
