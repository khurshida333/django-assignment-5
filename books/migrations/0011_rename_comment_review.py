# Generated by Django 5.0.6 on 2024-09-06 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0010_book_is_borrowed'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comment',
            new_name='Review',
        ),
    ]
