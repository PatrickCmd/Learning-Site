# Generated by Django 2.1.1 on 2018-09-10 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_auto_20180910_0912'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]
