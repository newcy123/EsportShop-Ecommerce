# Generated by Django 3.2 on 2021-06-28 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20210629_0506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='charge',
            field=models.IntegerField(default=0),
        ),
    ]