# Generated by Django 2.1 on 2018-08-29 09:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fairapp', '0005_auto_20180827_0751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appforproject',
            name='status',
            field=models.CharField(blank=True, choices=[('m', 'Moderation'), ('a', 'Approved'), ('r', 'Rejected')], default='m', help_text='Application status', max_length=1),
        ),
        migrations.AlterField(
            model_name='profile',
            name='faculty',
            field=models.CharField(blank=True, choices=[('a', 'ApMath'), ('c', 'Chemistry'), ('p', 'Physics'), ('m', 'MathMech'), ('b', 'Biology'), ('l', 'Faculty of Law'), ('s', 'Social Faculty')], help_text='Faculty', max_length=1),
        ),
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(blank=True, choices=[('b', 'Bachelor'), ('m', 'Master'), ('g', 'Graduate Student'), ('t', 'Teacher')], help_text='Status', max_length=1),
        ),
        migrations.AlterField(
            model_name='project',
            name='app_deadline',
            field=models.DateField(default=datetime.date.today, verbose_name='application deadline'),
        ),
        migrations.AlterField(
            model_name='project',
            name='content',
            field=models.TextField(max_length=2000),
        ),
        migrations.AlterField(
            model_name='project',
            name='end_date',
            field=models.DateField(default=datetime.date.today, verbose_name='ending date'),
        ),
        migrations.AlterField(
            model_name='project',
            name='pub_date',
            field=models.DateField(default=datetime.date.today, verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.DateField(default=datetime.date.today, verbose_name='starting date'),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(blank=True, choices=[('m', 'Moderation'), ('c', 'Collecting participants'), ('p', 'In progress'), ('f', 'Finished'), ('r', 'Rejected')], default='m', help_text='Project status', max_length=1),
        ),
    ]