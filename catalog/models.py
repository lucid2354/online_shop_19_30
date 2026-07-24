from django.db import models
from django.core.validators import MinValueValidator



class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True,
                               related_name='children', verbose_name='Родительская категория')
    is_active = models.BooleanField(default=True, verbose_name='Активность')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name='Категория')
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='Цена')
    old_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],
                                    null=True, blank=True, verbose_name='Старая цена')
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name='Изображение')
    stock = models.PositiveIntegerField(default=0, verbose_name='Наличие')
    is_active = models.BooleanField(default=True, verbose_name='Активность')
    is_featured = models.BooleanField(default=False, verbose_name='Рекомендуемый')
    is_new = models.BooleanField(default=False, verbose_name='Новинка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return int((1 - self.price / self.old_price) * 100)
        return 0

    @property
    def in_stock(self):
        return self.stock > 0

    @property
    def avg_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(
                sum(review.rating for review in reviews) / reviews.count(), 1)

        return 0

    @property
    def reviews_count(self):
        return self.reviews.count()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Товар')
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name='Изображение')
    alt = models.CharField(verbose_name='Alt текст', max_length=200, blank=True)
    order = models.PositiveIntegerField(verbose_name='Порядок', default=0)

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'
        ordering = ['order']

    def __str__(self):
        return f'Изображение: {self.product.name}'

