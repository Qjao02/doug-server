# Generated by Django 2.1.5 on 2019-08-14 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doug_server_app', '0016_eventos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=30, null=True)),
                ('assunto', models.TextField()),
                ('data_criado', models.DateTimeField(editable=False)),
                ('data_evento', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Eventos',
        ),
    ]
