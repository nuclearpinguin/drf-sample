# Generated by Django 2.2 on 2019-04-15 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=300)),
                ('director', models.CharField(blank=True, max_length=500, null=True)),
                ('genre', models.CharField(blank=True, max_length=2000, null=True)),
                ('metascore', models.IntegerField(null=True)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('body', models.TextField()),
                ('movie_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='movies.Movie')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]