# Generated by Django 4.2 on 2023-04-14 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NewsApp', '0010_remove_category_name_en_remove_category_name_ru_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='news',
            old_name='author',
            new_name='user',
        ),
    ]
