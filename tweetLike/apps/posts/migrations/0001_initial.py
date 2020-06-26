# Generated by Django 2.2.2 on 2020-06-25 23:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('title', models.CharField(db_index=True, max_length=255)),
                ('contentType', models.CharField(choices=[('text/plain', 'Plain Text'), ('text/markdown', 'Markdown'), ('image/png', 'Image with PNG format'), ('image/jpeg', 'Image with JPEG format'), ('application/base64', 'Application')], default='text/plain', max_length=48)),
                ('description', models.TextField()),
                ('content', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='profiles.Profile')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
                'abstract': False,
            },
        ),
    ]