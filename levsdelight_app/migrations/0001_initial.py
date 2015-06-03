# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('postText', models.CharField(max_length=10000)),
                ('title', models.CharField(max_length=2000)),
                ('images_id', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author_id', models.ForeignKey(default=1, to='levsdelight_app.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('commenter_name', models.CharField(max_length=50)),
                ('comment', models.CharField(max_length=7000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(to='levsdelight_app.BlogPost')),
            ],
        ),
        migrations.CreateModel(
            name='MonthMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slideshow_id', models.IntegerField()),
                ('month', models.CharField(max_length=20)),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PendingComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('commenter_name', models.CharField(max_length=50)),
                ('comment', models.CharField(max_length=7000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(to='levsdelight_app.BlogPost')),
            ],
        ),
        migrations.CreateModel(
            name='Slideshow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=1000)),
                ('desc', models.CharField(max_length=2000)),
                ('pictureLocation', models.CharField(max_length=200)),
                ('isActive', models.BooleanField()),
                ('slideshow_id', models.IntegerField()),
                ('order_id', models.IntegerField()),
                ('pub_date', models.DateTimeField(verbose_name=b'date_pubished')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='author',
            unique_together=set([('first_name', 'last_name')]),
        ),
    ]
