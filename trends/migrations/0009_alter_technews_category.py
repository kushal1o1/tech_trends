# Generated by Django 5.0.3 on 2025-03-29 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trends', '0008_alter_technews_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='technews',
            name='category',
            field=models.CharField(choices=[('nepali', 'Nepali Tech News'), ('global', 'Global Tech News (Nepali)'), ('trending', 'Trending  News(Nepali)'), ('ronb', 'Routine Of Nepal Banda'), ('bbc', 'Tech BBC News'), ('newsapinewsapiorg', 'News API')], max_length=20),
        ),
    ]
