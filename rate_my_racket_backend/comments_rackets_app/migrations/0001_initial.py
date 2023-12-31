# Generated by Django 4.0.4 on 2022-04-19 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Brand Name', max_length=256)),
                ('image', models.ImageField(blank=True, null=True, upload_to='brands/')),
            ],
        ),
        migrations.CreateModel(
            name='Racket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Brand Name', max_length=256)),
                ('image', models.ImageField(blank=True, null=True, upload_to='brands/')),
                ('head_size', models.FloatField(default=0.0)),
                ('length', models.FloatField(default=0.0)),
                ('weight_strung', models.FloatField(default=0.0)),
                ('weight_unstrung', models.FloatField(default=0.0)),
                ('composition', models.CharField(default='Graphite', max_length=256)),
                ('stiffness', models.FloatField(default=0.0)),
                ('average_cost', models.FloatField(default=0.0)),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='comments_rackets_app.brand')),
            ],
        ),
    ]
