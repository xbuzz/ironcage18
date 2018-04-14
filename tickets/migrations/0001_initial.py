# Generated by Django 2.0.3 on 2018-04-14 18:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.CharField(max_length=40)),
                ('sat', models.BooleanField()),
                ('sun', models.BooleanField()),
                ('mon', models.BooleanField()),
                ('tue', models.BooleanField()),
                ('wed', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TicketInvitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_addr', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('token', models.CharField(max_length=12, unique=True)),
                ('status', models.CharField(default='unclaimed', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to='tickets.Ticket')),
            ],
        ),
    ]
