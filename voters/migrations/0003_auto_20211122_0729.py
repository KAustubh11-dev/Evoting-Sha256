# Generated by Django 3.2.7 on 2021-11-22 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voters', '0002_auto_20211121_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='adhar_photo',
            field=models.ImageField(upload_to='media/images/adhar'),
        ),
        migrations.AlterField(
            model_name='voter',
            name='profile_photo',
            field=models.ImageField(upload_to='media/images/profile'),
        ),
    ]