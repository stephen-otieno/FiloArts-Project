# Generated by Django 5.1.3 on 2025-03-19 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FiloArtsPlus', '0011_alter_blog_post_date_alter_comment_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='author',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='blog',
            name='post_date',
            field=models.DateField(),
        ),
    ]
