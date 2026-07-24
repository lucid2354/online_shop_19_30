import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0001_initial'),
        ('catalog', '0002_review_wishlist'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.CreateModel(
                    name='Review',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Оценка')),
                        ('comment', models.TextField(blank=True, verbose_name='Комментарий')),
                        ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                        ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='catalog.product', verbose_name='Товар')),
                        ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                    ],
                    options={
                        'verbose_name': 'Отзыв',
                        'verbose_name_plural': 'Отзывы',
                        'ordering': ['-created_at'],
                        'unique_together': {('product', 'user')},
                        'db_table': 'catalog_review',
                    },
                ),
                migrations.CreateModel(
                    name='Wishlist',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                        ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlisted_by', to='catalog.product', verbose_name='Товар')),
                        ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                    ],
                    options={
                        'verbose_name': 'Избранное',
                        'verbose_name_plural': 'Избранное',
                        'unique_together': {('user', 'product')},
                        'db_table': 'catalog_wishlist',
                    },
                ),
            ],
        ),
    ]
