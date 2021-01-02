# Generated by Django 3.1.4 on 2021-01-01 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='GroupSvg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(help_text='dfgdfg', max_length=255, verbose_name='key')),
                ('collection', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='snowebsvg.collection')),
            ],
        ),
        migrations.CreateModel(
            name='Svg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255, verbose_name='title')),
                ('group', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='snowebsvg.groupsvg')),
            ],
        ),
    ]
