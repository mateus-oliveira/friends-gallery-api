# Generated by Django 3.1.5 on 2021-07-04 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20210702_0106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'married'), (2, 'friend'), (3, 'admin')], verbose_name='User role'),
        ),
    ]
