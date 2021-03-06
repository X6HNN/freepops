# Generated by Django 3.0.4 on 2020-03-05 12:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_group', models.CharField(max_length=10)),
                ('date_post', models.DateTimeField()),
                ('url_post', models.TextField()),
                ('url_img', models.TextField()),
                ('text_post', models.TextField()),
                ('c_like', models.IntegerField(max_length=10)),
                ('c_comments', models.IntegerField(max_length=10)),
                ('c_views', models.IntegerField(max_length=10)),
                ('c_reposts', models.IntegerField(max_length=10)),
                ('id_posts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
