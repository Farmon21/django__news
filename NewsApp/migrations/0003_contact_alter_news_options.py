# Generated by Django 4.1.7 on 2023-03-15 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewsApp', '0002_alter_news_managers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('text', models.TextField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ['-publish_time'], 'verbose_name_plural': 'News'},
        ),
    ]
