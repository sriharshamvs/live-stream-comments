# Generated by Django 3.0.6 on 2020-05-06 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChannelMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_name', models.CharField(max_length=2000)),
                ('user_id', models.CharField(max_length=2000)),
                ('user_name', models.CharField(max_length=2000)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('votes', models.IntegerField()),
            ],
        ),
    ]