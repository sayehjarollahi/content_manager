# Generated by Django 3.1.5 on 2023-03-14 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_remove_content_is_private'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='attach_category',
        ),
        migrations.RemoveField(
            model_name='category',
            name='allowed_attach_categories',
        ),
        migrations.DeleteModel(
            name='AttachCategory',
        ),
    ]