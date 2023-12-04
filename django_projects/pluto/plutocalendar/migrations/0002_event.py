# Generated by Django 4.2.7 on 2023-12-02 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plutocalendar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(help_text='Summary of event', max_length=250)),
                ('date', models.DateField()),
            ],
        ),
    ]
