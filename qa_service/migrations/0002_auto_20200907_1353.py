# Generated by Django 3.1 on 2020-09-07 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa_service', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
