# Generated by Django 2.1.1 on 2018-09-06 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20180905_1721'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('order', models.IntegerField(default=0)),
                ('total_questions', models.IntegerField(default=4)),
                ('course', models.ForeignKey(on_delete='models.CASCADE', to='courses.Course')),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
        ),
    ]
