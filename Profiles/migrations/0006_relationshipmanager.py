# Generated by Django 3.2.4 on 2021-06-16 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profiles', '0005_delete_relationshipmanager'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelationshipManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
