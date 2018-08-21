# Generated by Django 2.1 on 2018-08-21 18:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppForProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('covering_letter', models.TextField(max_length=1000)),
                ('status', models.CharField(blank=True, choices=[('m', 'Moderation'), ('a', 'Approved'), ('r', 'Rejected')], default=1, help_text='Application status', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('interests', models.TextField(max_length=1000)),
                ('achievements', models.TextField(max_length=1000)),
                ('faculty', models.CharField(blank=True, choices=[('a', 'ApMath'), ('c', 'Chemistry'), ('p', 'Physics'), ('m', 'MathMech'), ('b', 'Biology'), ('l', 'Faculty of Law'), ('s', 'Social Faculty')], default=1, help_text='Faculty', max_length=1)),
                ('status', models.CharField(blank=True, choices=[('b', 'Bachelor'), ('m', 'Master'), ('g', 'Graduate Student'), ('t', 'Teacher')], default=1, help_text='Status', max_length=1)),
                ('grade', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.TextField(max_length=255)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='starting date')),
                ('end_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='ending date')),
                ('brief_summary', models.TextField(max_length=1000)),
                ('content', models.TextField(max_length=1000)),
                ('app_deadline', models.DateTimeField(default=django.utils.timezone.now, verbose_name='application deadline')),
                ('num_places', models.PositiveIntegerField(default=1)),
                ('status', models.CharField(blank=True, choices=[('m', 'Moderation'), ('c', 'Collecting participants'), ('p', 'In progress'), ('f', 'Finished')], default=1, help_text='Project status', max_length=1)),
                ('head', models.ManyToManyField(related_name='head', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(blank=True, related_name='members', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='skill',
            field=models.ManyToManyField(related_name='skills', to='fairapp.Skill'),
        ),
        migrations.AddField(
            model_name='project',
            name='tag',
            field=models.ManyToManyField(related_name='tags', to='fairapp.Tag'),
        ),
        migrations.AddField(
            model_name='project',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fairapp.Type'),
        ),
        migrations.AddField(
            model_name='appforproject',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fairapp.Project'),
        ),
        migrations.AddField(
            model_name='appforproject',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
