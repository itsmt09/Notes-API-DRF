# Generated by Django 4.2.3 on 2023-07-19 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_rename_note_page'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Page',
            new_name='Note',
        ),
    ]
