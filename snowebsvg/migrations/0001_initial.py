# Generated by Django 3.1.4 on 2021-02-08 11:18

from django.db import migrations, models
import django.db.models.deletion
from snowebsvg import settings

if settings.WAGTAIL_INSTALL:
    import wagtail.search.index
    bases_svg = (wagtail.search.index.Indexed, models.Model)
else:
    bases_svg = (models.Model,)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255, verbose_name='Key')),
            ],
            options={
                'ordering': ('key',),
            },
        ),
        migrations.CreateModel(
            name='GroupSvg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255, verbose_name='Key')),
                ('collection', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='snowebsvg.collection')),
            ],
            options={
                'ordering': ('key',),
            },
        ),
        migrations.CreateModel(
            name='Svg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255, verbose_name='Key')),
                ('group', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='snowebsvg.groupsvg')),
            ],
            options={
                'ordering': ('key',),
            },
            bases=bases_svg,
        ),
    ]
