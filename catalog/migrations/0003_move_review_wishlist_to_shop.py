from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('catalog', '0002_review_wishlist'),
        ('shop', '0002_review_wishlist'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.DeleteModel(name='Review'),
                migrations.DeleteModel(name='Wishlist'),
            ],
        ),
    ]
