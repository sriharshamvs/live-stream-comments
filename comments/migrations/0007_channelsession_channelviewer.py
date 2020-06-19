# Generated by Django 3.0.6 on 2020-06-05 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0006_channelmod'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChannelViewer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2000)),
                ('phone_number', models.CharField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='ChannelSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('online', models.BooleanField()),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comments.Channel')),
                ('viewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comments.ChannelViewer')),
            ],
        ),
    ]