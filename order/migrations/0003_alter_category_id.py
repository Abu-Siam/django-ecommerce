# Generated by Django 4.1 on 2022-09-27 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_blog_category_rename_userid_order_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
