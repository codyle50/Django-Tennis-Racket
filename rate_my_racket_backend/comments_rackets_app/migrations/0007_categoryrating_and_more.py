# Generated by Django 4.0.4 on 2022-04-20 02:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments_rackets_app', '0006_alter_racket_points'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='overallracketrating',
            name='audience_advanced',
        ),
        migrations.RemoveField(
            model_name='overallracketrating',
            name='audience_beginner',
        ),
        migrations.RemoveField(
            model_name='overallracketrating',
            name='audience_intermediate',
        ),
        migrations.RemoveField(
            model_name='overallracketrating',
            name='comfort_rating',
        ),
        migrations.RemoveField(
            model_name='overallracketrating',
            name='control_rating',
        ),
        migrations.RemoveField(
            model_name='overallracketrating',
            name='flexibility_rating',
        ),
        migrations.RemoveField(
            model_name='overallracketrating',
            name='maneuverable_rating',
        ),
        migrations.RemoveField(
            model_name='overallracketrating',
            name='power_rating',
        ),
        migrations.RemoveField(
            model_name='overallracketrating',
            name='racket_sweet_spot_rating',
        ),
        migrations.RemoveField(
            model_name='overallracketrating',
            name='serving_rating',
        ),
        migrations.RemoveField(
            model_name='overallracketrating',
            name='spin_rating',
        ),
        migrations.RemoveField(
            model_name='overallracketrating',
            name='stable_rating',
        ),
        migrations.RemoveField(
            model_name='overallracketrating',
            name='volley_rating',
        ),
        migrations.AddField(
            model_name='overallracketrating',
            name='points',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='overallracketrating',
            name='rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='overallracketrating',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='comments_rackets_app.categoryrating'),
        ),
    ]
