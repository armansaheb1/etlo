from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.utils import timezone
import random
from etlo.settings import ROOT
from PIL import Image
from io import BytesIO
from django.core.files import File
from django_softdelete.models import SoftDeleteModel
from django.core.validators import MaxValueValidator, MinValueValidator
from main.models import Currency, CustomUser, DepartmentService, Address
from django.utils.deconstruct import deconstructible


def rand():
    while True:
        code = random.randint(1111111111, 9999999999)
        if not CustomUser.objects.filter(etlo_id=code).exists():
            return code


@deconstructible
class PathRename(object):

    def __init__(self, sub_path, part):
        self.path = sub_path
        self.part = part

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(
            self.part + '-' + timezone.now().strftime("%m/%d/%Y-%H:%M:%S"), ext)
        return os.path.join(self.path, filename)


class ForeignBuyPost(SoftDeleteModel):
    last_modify_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True)
    add_date = models.DateTimeField(auto_now_add=True, editable=True)
    last_modify_date = models.DateTimeField(auto_now=True, editable=True)
    name = models.CharField(max_length=50, null=True)
    percent_price = models.BooleanField(default=True)
    price = models.FloatField()

    class Meta:
        verbose_name_plural = ' Foreign Buy Posts '


class ForeignBuyCategory(SoftDeleteModel):
    last_modify_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True)
    add_date = models.DateTimeField(auto_now_add=True, editable=True)
    last_modify_date = models.DateTimeField(auto_now=True, editable=True)
    department = models.ForeignKey(
        DepartmentService, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    details = models.CharField(max_length=250, null=True)
    icon = models.CharField(max_length=50, null=True)
    image = models.ImageField(upload_to=PathRename(
        'ForeignBuyCategories', 'ForeignBuyCategories'), null=True)

    def get_image(self):
        if not self.image:
            return ''
        return ROOT + self.image.url

    class Meta:
        verbose_name_plural = ' Foreign Buy Categories '


class ForeignBuySites(SoftDeleteModel):
    last_modify_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True)
    add_date = models.DateTimeField(auto_now_add=True, editable=True)
    last_modify_date = models.DateTimeField(auto_now=True, editable=True)
    category = models.ForeignKey(ForeignBuyCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    details = models.CharField(max_length=250, null=True)
    icon = models.CharField(max_length=50, null=True)
    image = models.ImageField(upload_to=PathRename(
        'ForeignBuyCategories', 'ForeignBuyCategories'), null=True)
    link = models.URLField()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    def get_image(self):
        if not self.image:
            return ''
        return ROOT + self.image.url

    class Meta:
        verbose_name_plural = ' Foreign Buy Sites '


class ForeignBuyRequests(SoftDeleteModel):
    request_id = models.CharField(
        max_length=10, default=rand, editable=False, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    site = models.ForeignKey(ForeignBuySites, on_delete=models.CASCADE)
    details = models.CharField(max_length=250, null=True)
    image = models.URLField()
    link = models.URLField()
    price = models.FloatField()
    weight = models.IntegerField()
    quantity = models.IntegerField()
    payment_status = models.BooleanField()
    status = models.IntegerField(default=0)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    sum_price = models.FloatField(null=True, blank=True)
    recieve_date = models.DateTimeField(null=True)
    post = models.ForeignKey(
        ForeignBuyPost, on_delete=models.CASCADE, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def get_post(self):
        if not self.post:
            return ''
        else:
            return self.post.name

    def irt_price(self):
        if self.sum_price:
            return self.sum_price * self.currency.to_irt
        if not self.currency.to_irt:
            return ''
        sumprice = self.price
        return float(sumprice * self.currency.to_irt)

    def all_product_price(self):
        return float(self.price * self.quantity)

    def all_product_irt_price(self):
        if not self.currency.to_irt:
            return ''
        sumprice = self.quantity * self.price
        return float(sumprice * self.currency.to_irt)

    def post_price(self):
        if not self.post:
            return ''
        if self.post.percent_price:
            return float(self.quantity * self.price * self.currency.to_irt) * self.post.price / 100
        else:
            return self.post.price

    def pay_price(self):
        return self.all_product_irt_price() + self.post_price()

    class Meta:
        verbose_name_plural = ' Foreign Buy Requests '
