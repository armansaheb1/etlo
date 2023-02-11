from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomUser, Currency, Notification, Country, DepartmentService, DepartmentBanner, State, City, Wallet, Department, Address, Chat, Transaction, BankCard, BankSheba, Withdraw, Banner, MobileConfirmationCode, EmailConfirmationCode, BankIcon, DepositSettings, TransactionType


def set_user(context, mainmodel, validated_data):
    user = context
    validated_data['user'] = user
    model = mainmodel.objects.create(**validated_data)
    return model


class CurrentUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "phone_number",
            "email",
            "first_name",
            "last_name",
            "etlo_id",
            "is_active",
            "get_profile_image",
            "get_id_image",
            "is_admin",
            "id_image",
            "profile_image",
            "email_verification",
            "phone_verification",
            "image_verification",
            "id_verification_error",
            "image_verification_error",
            "id_verification",
            "is_verified"
        )


class CurrentUserSerializer2(serializers.ModelSerializer):
    def to_representation(self, instance):
        user = self.context['user']
        validated_data = super().to_representation(instance)
        if len(Wallet.objects.filter(user=user, currency=Currency.objects.get(symbol='IRT'))):
            balance = Wallet.objects.get(
                user=user, currency=Currency.objects.get(symbol='IRT')).balance
            validated_data['balance'] = balance
            validated_data['balance_icon'] = 'IRT'
        else:
            balance = 0
            validated_data['balance'] = balance
            validated_data['balance_icon'] = 'IRT'
        return validated_data

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "phone_number",
            "email",
            "first_name",
            "last_name",
            "etlo_id",
            "is_active",
            "get_profile_image",
            "get_id_image",
            "is_admin",
            "id_image",
            "profile_image",
            "email_verification",
            "phone_verification",
            "image_verification",
            "id_verification_error",
            "image_verification_error",
            "id_verification",
            "is_verified"
        )


class SetProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "id_image",
            "profile_image"
        )


class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = (
            "id",
            "code",
            "name",
            "color",
            "icon"
        )


class CurrencyConvertSerializer(serializers.Serializer):
    from_currency = serializers.IntegerField()
    to_currency = serializers.IntegerField()
    amount = serializers.FloatField()


class IdSerializer(serializers.Serializer):
    id = serializers.CharField()


class SetPhoneSerializer(serializers.Serializer):
    phone_code = serializers.CharField()
    phone = serializers.CharField()


class SetEmailSerializer(serializers.Serializer):
    email_code = serializers.CharField()
    email = serializers.EmailField()


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    re_new_password = serializers.CharField()


class SetCurrentPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    re_new_password = serializers.CharField()
    current_password = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    country_code = serializers.CharField()


class MobileConfirmationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileConfirmationCode
        fields = (
            "country_code",
            "phone_number",
        )


class EmailConfirmationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailConfirmationCode
        fields = (
            "email",
        )


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            "id",
            "title",
            "text",
            "icon_id",
            "read",
            "date",
            "icon"
        )


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = (
            "id",
            "name",
            "symbol",
            "dial_code",
            "image",
            "have_service",
            "get_flag"
        )


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = (
            "id",
            "name",
            "code",
        )


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            "id",
            "name",
        )


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = (
            "id",
            "country",
            "name",
            "code",
        )


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            "id",
            "state",
            "name",
        )


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = (
            "id",
            "add_date",
            "last_modify_date",
            "last_modify_user",
            "name",
            "img",
            "get_small_image",
            "get_medium_image",
            "get_large_image"
        )


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = (
            "id",
            "add_date",
            "last_modify_date",
            "last_modify_user",
            "name",
            "details",
            "icon",
            "is_active",
            "color",
            "background_item"
        )


class DepartmentBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentBanner
        fields = (
            "id",
            "add_date",
            "last_modify_date",
            "last_modify_user",
            "name",
            "department",
            "img",
            "get_small_image",
            "get_medium_image",
            "get_large_image"
        )


class DepartmentServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentService
        fields = (
            "id",
            "add_date",
            "last_modify_date",
            "last_modify_user",
            "name",
            "details",
            "department",
            "icon",
            "is_active"
        )


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = (
            "id",
            "add_date",
            "last_modify_date",
            "last_modify_user",
            "name",
            "symbol",
            "country",
            "icon",
            "is_active",
            "to_irt",
            "get_flag",
            "min_deposit",
            "max_deposit",
            "deposit_bank_fee",
            "min_withdraw",
            "max_withdraw",
            "withdraw_fee",
            "withdraw_bank_fee",
            "admin_address",
            "name_of_address",
            "can_do",
            "tips_deposit",
            "tips_deposit_online",
            "link1",
            "link2",
            "textbox"
        )


class DepositSettingSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['tips'] = self.context['tips'].split(',')
        model = Wallet.objects.create(**validated_data)
        return model

    class Meta:
        model = DepositSettings
        fields = (
            "can_do",
            "tips_deposit",
            "tips_deposit_online",
            "link1",
            "link2",
            "textbox"
        )


class WalletSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        if not 'balance' in validated_data:
            validated_data['balance'] = self.context['amount']
        model = Wallet.objects.create(**validated_data)
        return model

    class Meta:
        model = Wallet
        fields = (
            "id",
            "currency",
            "balance",
            "user",
            "get_currency_name",
            "get_flag",
            "get_icon",
            "get_currency",
            "can_do",
            "tips_deposit",
            "tips_deposit_online",
            "link1",
            "link2",
            "textbox"
        )


class AddressSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return set_user(mainmodel=Address, validated_data=validated_data,
                        context=self.context['user'])

    class Meta:
        model = Address
        fields = (
            "id",
            "user",
            "name",
            "reciever_first_name",
            "reciever_last_name",
            "country",
            "country_name",
            "state_name",
            "state",
            "address",
            "postal_code",
            "phone",
        )


class ChatSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return set_user(mainmodel=Chat, validated_data=validated_data,
                        context=self.context['user'])

    class Meta:
        model = Chat
        fields = (
            "id",
            "owner",
            "user",
            "text",
            "get_image",
            "admin_read",
            "user_read",
            "date",
            "order_id",
            "department",
            "service"
        )


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = (
            "id",
            "user",
            "currency",
            "type",
            "amount",
            "details",
            "bank_code",
            "get_currency_name",
            "get_flag",
            "get_icon",
            "get_symbol",
            "get_type",
            "date"
        )


class BankCardSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return set_user(mainmodel=BankCard, validated_data=validated_data,
                        context=self.context['user'])

    class Meta:
        model = BankCard
        fields = (
            "id",
            "user",
            "number",
            "full_name",
            "bank_name",
            "status",
            "image",
            "get_image",
            "date"
        )


class BankShebaSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return set_user(mainmodel=BankSheba, validated_data=validated_data,
                        context=self.context['user'])

    class Meta:
        model = BankSheba
        fields = (
            "id",
            "user",
            "number",
            "full_name",
            "bank_name",
            "status",
            "date"
        )


class WithdrawSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return set_user(mainmodel=Withdraw, validated_data=validated_data,
                        context=self.context['user'])

    class Meta:
        model = Withdraw
        fields = (
            "id",
            "user",
            "currency",
            "banksheba",
            "bankcard",
            "amount",
            "status",
            "date",
            "get_sheba",
            "get_card",
            "get_bank_name",
            "get_currency",
        )


class BankIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankIcon
        fields = (
            "card_code",
            "sheba_code",
            "bank_name",
            "bank_icon",
            "get_icon",
        )
