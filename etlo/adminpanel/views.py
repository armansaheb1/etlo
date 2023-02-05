from main.models import Country, DepartmentBanner, Currency, Department, DepartmentService, Wallet, CustomUser, Chat, Notification, Transaction, BankCard, BankSheba, Withdraw, Banner, MobileConfirmationCode, DepositSettings, TransactionType
from main.serializers import CountrySerializer, DepartmentBannerSerializer,  CurrencySerializer, DepartmentSerializer, DepartmentServiceSerializer, WalletSerializer, ChatSerializer, BankCardSerializer, BankShebaSerializer, WithdrawSerializer, CurrentUserSerializer, BannerSerializer, LoginSerializer, TransactionSerializer, DepositSettingSerializer, TransactionTypeSerializer
from insurance.models import HealthInsuranceCompany, HealthInsurancePriceList, HealthInsuranceUserDiscount, HealthInsuranceRequest
from insurance.serializers import HealthInsurancePriceListSerializer, HealthInsuranceCompanySerializer, HealthInsuranceUserDiscountSerializer, HealthInsuranceRequestSerializer
from foreignbuy.models import ForeignBuyCategory, ForeignBuyRequests, ForeignBuySites
from foreignbuy.serializers import ForeignBuyCategorySerializer, ForeignBuyRequestsSerializer, ForeignBuySitesSerializer
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAdminUser, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status
from .serializers import RejectSerializer, HealthInsuranceSubmitSerializer
from datetime import datetime
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.hashers import check_password
# Create your views here.


def checkid(id):
    if not id.isnumeric():
        return Response({'data': 'ID Should Be a Number'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class SetAdmin(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        if not len(CustomUser.objects.filter(id=request.data['id'])):
            return Response({'data': 'Invalid User ID'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        user = CustomUser.objects.get(id=request.data['id'])
        user.is_admin = True
        user.save()
        serializer = CurrentUserSerializer([user], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Login(APIView):

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
            'expiration_time': datetime.datetime.fromtimestamp(refresh['exp'])
        }

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            if not len(CustomUser.objects.filter(Q(phone_number=serializer.data['username']) | Q(email=serializer.data['username']))):
                if not len(MobileConfirmationCode.objects.filter(phone_number=serializer.data['username'])):
                    return Response({'data': 'Wrong or Expired Code'}, status=status.HTTP_403_FORBIDDEN)
                elif MobileConfirmationCode.objects.get(phone_number=serializer.data['username']).code != int(serializer.data['password']):
                    return Response({'data': 'Wrong Code'}, status=status.HTTP_403_FORBIDDEN)
                elif MobileConfirmationCode.objects.get(phone_number=serializer.data['username']).date + datetime.timedelta(minutes=1) < timezone.now():
                    return Response({'data': 'Expired Code'}, status=status.HTTP_403_FORBIDDEN)
                else:
                    cc = CustomUser(phone_number=serializer.data['username'], country_code=Country.objects.get(
                        dial_code=int(serializer.data['country_code'])), phone_verification=True)
                    cc.save()
            user = CustomUser.objects.filter(Q(phone_number=serializer.data['username']) | Q(
                email=serializer.data['username'])).last()
            if (str(MobileConfirmationCode.objects.get(phone_number=user.phone_number).code) != serializer.data['password']):
                if user.password:
                    if not check_password(serializer.data['password'], user.password):
                        return Response({'data': 'Wrong Password'}, status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response({'data': 'Wrong Password'}, status=status.HTTP_403_FORBIDDEN)
            refresh = self.get_tokens_for_user(user)
            return Response({'data': refresh}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class TransactionTypes(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = TransactionType.objects.all()
        serializer = TransactionTypeSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data._mutable = True
        serializer = TransactionTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def put(self, request, id):
        checkid(id)
        serializer = TransactionTypeSerializer(
            TransactionType.objects.get(id=id), data=request.data,)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def patch(self, request, id):
        checkid(id)
        serializer = TransactionTypeSerializer(
            TransactionType.objects.get(id=id), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, id):
        checkid(id)
        Currency.objects.get(id=id).delete()
        return Response({'data': True}, status=status.HTTP_200_OK)


class Currencies(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = Currency.objects.all()
        serializer = CurrencySerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data._mutable = True
        serializer = CurrencySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def put(self, request, id):
        checkid(id)
        serializer = CurrencySerializer(
            Currency.objects.get(id=id), data=request.data,)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def patch(self, request, id):
        checkid(id)
        serializer = CurrencySerializer(
            Currency.objects.get(id=id), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, id):
        checkid(id)
        Currency.objects.get(id=id).delete()
        return Response({'data': True}, status=status.HTTP_200_OK)


class Wallets(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = Wallet.objects.all()
        serializer = WalletSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data._mutable = True
        serializer = WalletSerializer(data=request.data)
        if len(Wallet.objects.filter(user=request.data['user'], currency=request.data['currency'])):
            return Response({'data': 'Wallet already exists'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def put(self, request, id):
        checkid(id)
        try:
            request.data._mutable = True
            wallet = Wallet.objects.get(id=id)
            request.data['currency'] = wallet.currency.id
            serializer = WalletSerializer(wallet, data=request.data,)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({'data': 'ID Not Found'}, status=status.HTTP_404_NOT_FOUND)


class ChargeWallets(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        if not len(Currency.objects.filter(id=request.data['currency'])):
            return Response({'data': 'Currency Not Found'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not len(CustomUser.objects.filter(id=request.data['user'])):
            return Response({'data': 'User Not Found'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if len(Wallet.objects.filter(user=request.data['user'], currency=request.data['currency'])):
            serializer2 = TransactionSerializer(data=request.data)
            if serializer2.is_valid():
                wallet = Wallet.objects.get(
                    user=request.data['user'], currency=request.data['currency'])
                wallet.balance = wallet.balance + float(request.data['amount'])
                wallet.save()
                serializer2.save()
                serializer = WalletSerializer([wallet], many=True)
            else:
                return Response(serializer2.errors)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = WalletSerializer(data=request.data, context={
                                      'amount': request.data['amount']})
        serializer2 = TransactionSerializer(
            data=request.data, context={'type': 1})
        if serializer.is_valid():
            if serializer2.is_valid():
                serializer.save()
                serializer2.save()
            else:
                return Response(serializer.errors)
        else:
            return Response(serializer.errors)
        return Response(serializer.data)


class HealthInsuranceCompanies(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = HealthInsuranceCompany.objects.all()
        serializer = HealthInsuranceCompanySerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data._mutable = True
        serializer = HealthInsuranceCompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def put(self, request, id):
        checkid(id)
        try:
            request.data._mutable = True

            serializer = HealthInsuranceCompanySerializer(
                HealthInsuranceCompany.objects.get(id=id), data=request.data,)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({'data': 'ID Not Found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        checkid(id)
        HealthInsuranceCompany.objects.get(id=id).delete()
        return Response({'data': True})


class HealthInsurancePriceLists(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = HealthInsurancePriceList.objects.all()
        serializer = HealthInsurancePriceListSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data._mutable = True
        if len(HealthInsurancePriceList.objects.filter(company=HealthInsuranceCompany.objects.get(id=int(request.data['company'])), start_age__lte=int(request.data['start_age']), end_age__gte=int(request.data['start_age']))) or len(HealthInsurancePriceList.objects.filter(company=HealthInsuranceCompany.objects.get(id=int(request.data['company'])), start_age__lte=int(request.data['end_age']), end_age__gte=int(request.data['end_age']))):
            return Response({'data': 'Repeated Age Problem'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        serializer = HealthInsurancePriceListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def put(self, request, id):
        checkid(id)
        try:
            request.data._mutable = True

            if len(HealthInsurancePriceList.objects.filter(~Q(id=id), company=HealthInsuranceCompany.objects.get(id=int(request.data['company'])), start_age__lte=int(request.data['start_age']), end_age__gte=int(request.data['start_age']))) or len(HealthInsurancePriceList.objects.filter(~Q(id=id), company=HealthInsuranceCompany.objects.get(id=int(request.data['company'])), start_age__lte=int(request.data['end_age']), end_age__gte=int(request.data['end_age']))):
                return Response({'data': 'Repeated Age Problem'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            serializer = HealthInsurancePriceListSerializer(
                instance=HealthInsurancePriceList.objects.get(id=id), data=request.data,)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({'data': 'ID Not Found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        checkid(id)
        HealthInsurancePriceList.objects.get(id=id).delete()
        return Response({'data': True})


class Banners(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = Banner.objects.all()
        serializer = BannerSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data._mutable = True
        serializer = BannerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def put(self, request, id):
        checkid(id)
        try:
            request.data._mutable = True

            serializer = BannerSerializer(
                Banner.objects.get(id=id), data=request.data,)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({'data': 'ID Not Found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        checkid(id)
        Banner.objects.get(id=id).delete()
        return Response({'data': True})


class Departments(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = Department.objects.all()
        serializer = DepartmentSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data._mutable = True
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def put(self, request, id):
        checkid(id)
        try:
            request.data._mutable = True

            serializer = DepartmentSerializer(
                Department.objects.get(id=id), data=request.data,)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({'data': 'ID Not Found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        checkid(id)
        Department.objects.get(id=id).delete()
        return Response({'data': True})


class DepartmentBanners(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = DepartmentBanner.objects.all()
        serializer = DepartmentBannerSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data._mutable = True
        serializer = DepartmentBannerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def put(self, request, id):
        checkid(id)
        try:
            request.data._mutable = True

            serializer = DepartmentBannerSerializer(
                DepartmentBanner.objects.get(id=id), data=request.data,)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({'data': 'ID Not Found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        checkid(id)
        DepartmentBanner.objects.get(id=id).delete()
        return Response({'data': True})


class DepartmentServices(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = DepartmentService.objects.all()
        serializer = DepartmentServiceSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data._mutable = True
        serializer = DepartmentServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def put(self, request, id):
        checkid(id)
        try:
            request.data._mutable = True

            serializer = DepartmentServiceSerializer(
                DepartmentService.objects.get(id=id), data=request.data,)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({'data': 'ID Not Found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        checkid(id)
        DepartmentService.objects.get(id=id).delete()
        return Response({'data': True})


class ActiveCountries(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = Country.objects.filter(have_service=True)
        serializer = CountrySerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        checkid(id)
        try:
            cc = Country.objects.get(id=id)
            cc.have_service = not cc.have_service
            cc.save()
            query = Country.objects.filter(id=id)
            serializer = CountrySerializer(query, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'data': 'ID Not Found'}, status=status.HTTP_404_NOT_FOUND)


class HealthInsuranceDiscounts(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = HealthInsuranceUserDiscount.objects.filter(user=None)
        serializer = HealthInsuranceUserDiscountSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data._mutable = True
        serializer = HealthInsuranceUserDiscountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def put(self, request, id):
        checkid(id)
        try:
            request.data._mutable = True

            serializer = HealthInsuranceUserDiscountSerializer(
                HealthInsuranceUserDiscount.objects.get(id=id), data=request.data,)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({'data': 'ID Not Found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        checkid(id)
        HealthInsuranceUserDiscount.objects.get(id=id).delete()
        return Response({'data': True})


class HealthInsuranceUserDiscounts(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = HealthInsuranceUserDiscount.objects.filter(~Q(user=None))
        serializer = HealthInsuranceUserDiscountSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data._mutable = True
        serializer = HealthInsuranceUserDiscountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def put(self, request, id):
        checkid(id)
        try:
            request.data._mutable = True

            serializer = HealthInsuranceUserDiscountSerializer(
                HealthInsuranceUserDiscount.objects.get(id=id), data=request.data,)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({'data': 'ID Not Found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        checkid(id)
        HealthInsuranceUserDiscount.objects.get(id=id).delete()
        return Response({'data': True})


class HealthInsurancePendings(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = HealthInsuranceRequest.objects.filter(
            status=0, payment_status=True)
        serializer = HealthInsuranceRequestSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HealthInsuranceRejecteds(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = HealthInsuranceRequest.objects.filter(
            status=2, payment_status=True)
        serializer = HealthInsuranceRequestSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HealthInsuranceSubmiteds(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = HealthInsuranceRequest.objects.filter(
            status=1, payment_status=True)
        serializer = HealthInsuranceRequestSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HealthInsuranceReject(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = RejectSerializer(data=request.data)
        if serializer.is_valid():
            if not len(HealthInsuranceRequest.objects.filter(id=request.data['id'])):
                return Response({'data': 'ID Not Found'}, status=status.HTTP_404_NOT_FOUND)
            query = HealthInsuranceRequest.objects.get(id=request.data['id'])
            query.status = 2
            query.save()
            nt = Notification(user=query.user, title='Your Health Insurance Request Has Been Rejacted',
                              text=request.data['data'], icon=query.insurance.company.department.icon)
            nt.save()
            return Response({'data': True})
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class HealthInsuranceSubmit(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = HealthInsuranceSubmitSerializer(data=request.data)
        if serializer.is_valid():
            query = HealthInsuranceRequest.objects.get(
                id=serializer.data['id'])
            query.start_date = serializer.data['start_date']
            query.end_date = serializer.data['end_date']
            query.insurance_number = serializer.data['insurance_number']
            query.file = serializer.data['file']
            query.status = 1
            query.save()
            nt = Notification(user=query.user, title='Your Health Insurance Request Has Been Submited',
                              text=serializer.data['data'], icon=query.insurance.company.department.icon)
            nt.save()
            return Response({'data': True})
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class ActiveChats(APIView):
    def get(self, request):
        list = []
        for item in CustomUser.objects.all():
            chats = Chat.objects.filter(owner=item)
            if len(chats):
                list.append({'user_id': item.id, 'first_name': item.first_name, 'last_name': item.last_name, 'admin_unreads': Chat.objects.filter(
                    owner=item, admin_read=False).count(), 'last_message_date': chats.last().date, 'last_message_user': chats.last().user.etlo_id})
        return Response({'data': list})


class UserChats(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, id):
        checkid(id)
        query = Chat.objects.filter(owner=id)
        for item in query:
            item.admin_read = True
            item.save()
        serializer = ChatSerializer(query, many=True)
        return Response({'data': {'unread': Chat.objects.filter(owner=request.user.id, user_read=False).count(), 'messages': serializer.data}})

    def post(self, request, id):
        checkid(id)
        request.data._mutable = True
        request.data['user_read'] = True
        request.data['owner'] = id
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ForeignBuyCategories(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = ForeignBuyCategory.objects.all()
        serializer = ForeignBuyCategorySerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data._mutable = True
        serializer = ForeignBuyCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def put(self, request, id):
        checkid(id)
        try:
            request.data._mutable = True

            serializer = ForeignBuyCategorySerializer(
                ForeignBuyCategory.objects.get(id=id), data=request.data,)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({'data': 'ID Not Found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        checkid(id)
        ForeignBuyCategory.objects.get(id=id).delete()
        return Response({'data': True})


class ForeignBuySites(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = ForeignBuySites.objects.all()
        serializer = ForeignBuySitesSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data._mutable = True
        serializer = ForeignBuySitesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def put(self, request, id):
        checkid(id)
        try:
            request.data._mutable = True

            serializer = ForeignBuySitesSerializer(
                ForeignBuySites.objects.get(id=id), data=request.data,)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({'data': 'ID Not Found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        checkid(id)
        ForeignBuySites.objects.get(id=id).delete()
        return Response({'data': True})


class ForeignBuyCheckPendings(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = ForeignBuyRequests.objects.filter(
            status=0, payment_status=False)
        serializer = ForeignBuyRequestsSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ForeignBuyPendings(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = ForeignBuyRequests.objects.filter(
            status=0, payment_status=True)
        serializer = ForeignBuyRequestsSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ForeignBuyRejecteds(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = ForeignBuyRequests.objects.filter(
            status=2, payment_status=True)
        serializer = ForeignBuyRequestsSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ForeignBuySubmiteds(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = ForeignBuyRequests.objects.filter(
            status=1, payment_status=True)
        serializer = ForeignBuyRequestsSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ForeignBuyReject(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = RejectSerializer(data=request.data)
        if serializer.is_valid():
            if not len(ForeignBuyRequests.objects.filter(id=request.data['id'])):
                return Response({'data': 'ID Not Found'}, status=status.HTTP_404_NOT_FOUND)
            query = ForeignBuyRequests.objects.get(id=request.data['id'])
            query.status = 3
            query.save()
            nt = Notification(user=query.user, title='Your Health Insurance Request Has Been Rejacted',
                              text=request.data['data'], icon=query.site.category.icon)
            nt.save()
            return Response({'data': True})
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ForeignBuySubmit(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        checkid(request.data['id'])
        if not len(ForeignBuyRequests.objects.filter(id=request.data['id'])):
            return Response({'data': 'ID Not Found'}, status=status.HTTP_404_NOT_FOUND)
        query = ForeignBuyRequests.objects.get(id=request.data['id'])
        query.status = 2
        query.save()
        nt = Notification(user=query.user, title='Your Foreign Buy Request Has Been Submited',
                          text=request.data['data'], icon=query.insurance.company.department.icon)
        nt.save()
        return Response({'data': True})


class IdRequests(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        user = CustomUser.objects.filter(
            ~Q(id_image=''), id_verification_error=None, id_verification=False)
        serializer = CurrentUserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        checkid(request.data['id'])
        user = CustomUser.objects.get(id=request.data['id'])
        user.id_verification = True
        user.save()
        user = CustomUser.objects.filter(id=request.data['id'])
        serializer = CurrentUserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        checkid(request.data['id'])
        user = CustomUser.objects.get(id=request.data['id'])
        user.id_verification_error = request.data['data']
        user.id_verification = False
        user.save()
        user = CustomUser.objects.filter(id=request.data['id'])
        serializer = CurrentUserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class IdRequestRejecteds(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        user = CustomUser.objects.filter(~Q(id_image=''), ~Q(
            id_verification_error=None), id_verification=False)
        serializer = CurrentUserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ImageRequests(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        user = CustomUser.objects.filter(
            ~Q(profile_image=''), image_verification_error=None, image_verification=False)
        serializer = CurrentUserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        checkid(request.data['id'])
        user = CustomUser.objects.get(id=request.data['id'])
        user.image_verification = True
        user.save()
        user = CustomUser.objects.filter(id=request.data['id'])
        serializer = CurrentUserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        checkid(request.data['id'])
        user = CustomUser.objects.get(id=request.data['id'])
        user.image_verification_error = request.data['data']
        user.image_verification = False
        user.save()
        user = CustomUser.objects.filter(id=request.data['id'])
        serializer = CurrentUserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ImageRequestRejecteds(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        user = CustomUser.objects.filter(~Q(profile_image=''), ~Q(
            image_verification_error=None), image_verification=False)
        serializer = CurrentUserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BankCardRequests(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = BankCard.objects.filter(status=0)
        serializer = BankCardSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        checkid(id)
        bank = BankCard.objects.get(id=id)
        bank.status = 1
        bank.save()
        serializer = BankCardSerializer([bank], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        checkid(id)
        bank = BankCard.objects.get(id=id)
        bank.status = 2
        bank.save()
        serializer = BankCardSerializer([bank], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BankShebaRequests(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = BankSheba.objects.filter(status=0)
        serializer = BankShebaSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        checkid(id)
        bank = BankSheba.objects.get(id=id)
        bank.status = 1
        bank.save()
        serializer = BankShebaSerializer([bank], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        checkid(id)
        bank = BankSheba.objects.get(id=id)
        bank.status = 2
        bank.save()
        serializer = BankShebaSerializer([bank], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WithdrawRequests(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = Withdraw.objects.filter(status=0)
        serializer = WithdrawSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        checkid(id)
        bank = Withdraw.objects.get(id=id)
        bank.status = 1
        bank.save()
        serializer = WithdrawSerializer([bank], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        checkid(id)
        bank = Withdraw.objects.get(id=id)
        bank.status = 2
        bank.save()
        serializer = WithdrawSerializer([bank], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DepositSetting(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAdminUser]

    def patch(self, request):
        serializer = DepositSettingSerializer(
            DepositSettings.objects.get(), data=request.data, partial=True, context={'tips': request.data['tips']})
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)
        return Response({'data': serializer.data})
