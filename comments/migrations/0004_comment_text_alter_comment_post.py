# Generated by Django 5.0.4 on 2024-06-17 13:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
        ('comments', '0003_alter_comment_options_comment_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='text',
            field=models.TextField(default='No comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post'),
        ),
    ]
