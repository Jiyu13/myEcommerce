# Generated by Django 4.2.5 on 2023-10-31 05:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myshop', '0004_contactrequest_delete_customerprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactrequest',
            name='receiver_email',
        ),
        migrations.AddField(
            model_name='contactrequest',
            name='full_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='contactrequest',
            name='sender_email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='contactrequest',
            name='sender',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_contact_requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='contactrequest',
            name='subject',
            field=models.CharField(choices=[('Order issues', 'Order status'), ('Product question', 'Product question'), ('Report an issue', 'Report an issue'), ('Request refund or discount', 'Request refund or discount'), ('Feedback', 'Feedback'), ('Other', 'Other')], max_length=255),
        ),
    ]
