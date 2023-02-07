from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ForeignBuySites, ForeignBuyRequests, ForeignBuyCategory


class ForeignBuySitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForeignBuySites
        fields = (
            "id",
            "add_date",
            "last_modify_date",
            "last_modify_user",
            "name",
            "category",
            "details",
            "icon",
            "image",
            "currency",
            "get_image",
        )


class ForeignBuyRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForeignBuyRequests
        fields = (
            "request_id",
            "user",
            "name",
            "site",
            "details",
            "image",
            "link",
            "price",
            "weight",
            "quantity",
            "status",
            "currency",
            "date",
            "sum_price",
            "recieve_date",
            "address",
            "irt_price",
            "all_product_price",
            "all_product_irt_price",
            "post_price",
            "pay_price",
            "get_post"
        )


class ForeignBuyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ForeignBuyCategory
        fields = (
            "id",
            "name",
            "details",
            "icon",
            "image",
        )
