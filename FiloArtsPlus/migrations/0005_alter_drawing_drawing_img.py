# Generated by Django 5.1.3 on 2025-01-21 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FiloArtsPlus', '0004_alter_drawing_drawing_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drawing',
            name='drawing_img',
            field=models.ImageField(upload_to='drawings/'),
        ),
    ]
