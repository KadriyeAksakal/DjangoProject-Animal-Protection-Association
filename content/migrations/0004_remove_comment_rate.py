# Generated by Django 3.0.4 on 2020-05-10 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_auto_20200510_1638'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='rate',
        ),
    ]
