# Generated by Django 5.0.3 on 2025-04-13 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailApp', '0007_alter_subscribedcategory_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='verificationtoken',
            name='action',
            field=models.CharField(default='subscribe', max_length=20),
        ),
    ]
