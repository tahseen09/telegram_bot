# Generated by Django 4.0.5 on 2023-07-03 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hadith', '0002_alter_chat_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
