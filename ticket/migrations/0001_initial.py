# Generated by Django 3.2.23 on 2024-02-25 00:13

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('evenement', '0003_auto_20240224_0630'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('price', models.IntegerField(default=0)),
                ('is_sold', models.BooleanField(default=False)),
                ('date_dold', models.DateField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='evenement.event')),
            ],
            options={
                'verbose_name_plural': 'billets',
                'ordering': ['-date_dold'],
            },
        ),
    ]