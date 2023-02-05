from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import random
from etlo.settings import ROOT
from PIL import Image
from io import BytesIO
from django.core.files import File
from django_softdelete.models import SoftDeleteModel
from main.models import CustomUser, Country, State, City, DepartmentService
from django.core.validators import MinValueValidator
import os
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


class HealthInsuranceCompany(SoftDeleteModel):
    last_modify_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True)
    add_date = models.DateTimeField(auto_now_add=True, editable=True)
    last_modify_date = models.DateTimeField(auto_now=True, editable=True)
    department = models.ForeignKey(
        DepartmentService, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to=PathRename(
        'Insurances', 'Insurances'), null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Health Insurance Company'
        verbose_name_plural = 'Health Insurance Companies'

    def get_image(self):
        if not self.image:
            return ''
        return ROOT + self.image.url


class HealthInsurancePriceList(SoftDeleteModel):
    last_modify_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True)
    add_date = models.DateTimeField(auto_now_add=True, editable=True)
    last_modify_date = models.DateTimeField(auto_now=True, editable=True)
    company = models.ForeignKey(
        HealthInsuranceCompany, related_name='pricelist', on_delete=models.CASCADE)
    start_age = models.IntegerField(
        validators=[MinValueValidator(1)], null=True)
    end_age = models.IntegerField(validators=[MinValueValidator(1)], null=True)
    first_year = models.FloatField(null=True)
    second_year = models.FloatField(null=True)

    def __str__(self):
        return self.company.name + ' - (' + str(self.start_age) + ' - ' + str(self.end_age) + ')'

    def get_company_name(self):
        return self.company.name

    def get_company_image(self):
        return self.company.get_image()

    class Meta:
        verbose_name_plural = 'Health Insurance Price List '
        verbose_name_plural = 'Health Insurance Price Lists '


class HealthInsuranceUserDiscount(SoftDeleteModel):
    last_modify_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True)
    add_date = models.DateTimeField(auto_now_add=True, editable=True)
    last_modify_date = models.DateTimeField(auto_now=True, editable=True)
    name = models.CharField(max_length=100)
    percent = models.IntegerField(validators=[MinValueValidator(1)], )
    user = models.ForeignKey(
        CustomUser, related_name='discounts', on_delete=models.CASCADE, null=True)
    expiration_time = models.DateTimeField()


class HealthInsuranceRequest(SoftDeleteModel):
    request_id = request_id = models.CharField(
        max_length=10, default=rand, editable=False, unique=True)
    user = models.ForeignKey(
        CustomUser, related_name='insuraneRequests', on_delete=models.CASCADE, null=True)
    passport_number = models.CharField(max_length=30)
    cimlinc_number = models.CharField(max_length=30)
    insurance = models.ForeignKey(
        HealthInsurancePriceList, related_name='reuqests', on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    birthday_date = models.DateField()
    weight = models.FloatField()
    height = models.FloatField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    father_name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=30, null=True)
    email_address = models.EmailField(null=True)
    insurance_number = models.CharField(max_length=20, null=True, blank=True)
    addressDesc = models.CharField(max_length=30)
    apartmentNo = models.CharField(max_length=30)
    buildingNo = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    gender = models.CharField(max_length=30)
    submit_date = models.DateField(null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    code = models.IntegerField(validators=[MinValueValidator(1)], null=True)
    status = models.IntegerField(validators=[MinValueValidator(1)], default=0)
    payment_status = models.BooleanField(default=False)
    period = models.IntegerField(validators=[MinValueValidator(1)],)
    first_year_price = models.IntegerField(
        validators=[MinValueValidator(1)], null=True)
    second_year_price = models.IntegerField(
        validators=[MinValueValidator(1)], null=True)
    discount_percent = models.IntegerField(
        validators=[MinValueValidator(1)], null=True)
    discount = models.ForeignKey(
        HealthInsuranceUserDiscount, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to=PathRename(
        'files', 'files'), null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def price(self):
        if self.period:
            if self.period == 1:
                price = self.insurance.first_year
            else:
                price = self.insurance.second_year
            return price
        else:
            return 0

    def get_file(self):
        if not self.file:
            return ''
        return ROOT + self.file.url
