from django.db import models
from django.contrib.auth.models import User
from django.core import validators
from django.urls import reverse
from PIL import Image
from django.utils.translation import gettext_lazy as _


def product_preview_directory_path(instance: "Product", filename: str) -> str:
    return f"product/product_{instance.pk}/image/{filename}"


class Product(models.Model):
    """
    Модель **Product** представляет товар,
    который можно продавать в магазине.

    Изображения товара тут: :model:`shopapp.ProductImage`

    Заказы тут: :model:`shopapp.Order`
    """
    class Meta:
        ordering = ["name", "price"]
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    name = models.CharField(max_length=100)
    description = models.TextField(
        null=False, blank=True,
        validators=[validators.RegexValidator(regex=r"Made in",
                                              message="The field must contain words 'Made in'")])
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.preview:
            img = Image.open(self.preview.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.preview.path)

    def get_absolute_url(self):
        return reverse("shopapp:product_details", kwargs={"pk": self.pk})
    # @property
    # def description_short(self) -> str:
    #     if len(self.description) < 48:
    #         return self.description
    #     return self.description[:48] + "..."

    def __str__(self) -> str:
        return f"Product(pk={self.pk}, name={self.name!r})"


def product_image_directory_path(instance: "ProductImage", filename: str) -> str:
    return f"product/product_{instance.product.pk}/image/{filename}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=product_image_directory_path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)


class Order(models.Model):
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    delivery_address = models.TextField(
        null=False, blank=False,
        validators=[validators.RegexValidator(regex=r"city",
                                              message="The field must contain word 'city'")])
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name="orders")
