from rest_framework import serializers
from django.contrib.auth.models import User
from .models import HealthInsuranceCompany, HealthInsurancePriceList, HealthInsuranceUserDiscount, HealthInsuranceRequest


def set_user(context, mainmodel, validated_data):
    user = context
    validated_data['user'] = user
    model = mainmodel.objects.create(**validated_data)
    return model


class HealthInsuranceCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthInsuranceCompany
        fields = (
            "id",
            "add_date",
            "last_modify_date",
            "last_modify_user",
            "name",
            "image",
            "get_image",
        )


class HealthInsurancePriceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthInsurancePriceList
        fields = (
            "id",
            "company",
            "start_age",
            "end_age",
            "add_date",
            "last_modify_date",
            "last_modify_user",
            "get_company_name",
            "get_company_image",
            "first_year",
            "second_year"
        )


class HealthInsuranceUserDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthInsuranceUserDiscount
        fields = (
            "add_date",
            "last_modify_date",
            "last_modify_user",
            "id",
            "name",
            "user",
            "percent",
            "expiration_time",
        )


class HealthInsuranceRequestSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = self.context['user']
        if len(HealthInsuranceUserDiscount.objects.filter(user=user)):
            dis = HealthInsuranceUserDiscount.objects.filter(
                user=user).order_by('-last_modify_date').last()
            validated_data['discount'] = dis
            validated_data['discount_percent'] = dis.percent
        elif len(HealthInsuranceUserDiscount.objects.filter(user=None)):
            dis = HealthInsuranceUserDiscount.objects.filter(
                user=None).order_by('-last_modify_date').last()
            validated_data['discount'] = dis
            validated_data['discount_percent'] = dis.percent
        else:
            validated_data['discount'] = None
            validated_data['discount_percent'] = 0
        insurance = HealthInsurancePriceList.objects.get(
            id=self.context['insurance'])
        validated_data['first_year_price'] = insurance.first_year
        validated_data['second_year_price'] = insurance.second_year

        validated_data['user'] = user
        model = HealthInsuranceRequest.objects.create(**validated_data)
        return model

    class Meta:
        model = HealthInsuranceRequest
        fields = (
            "id",
            "user",
            "insurance",
            "passport_number",
            "cimlinc_number",
            "country",
            "state",
            "city",
            "addressDesc",
            "apartmentNo",
            "buildingNo",
            "street",
            "district",
            "gender",
            "period",
            "birthday_date",
            "weight",
            "height",
            "first_name",
            "last_name",
            "father_name",
            "description",
            "phone_number",
            "email_address",
            "start_date",
            "code",
            "status",
            "first_year_price",
            "second_year_price",
            "discount_percent",
            "discount",
            "price",
            "file"
        )
