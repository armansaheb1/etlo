from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import HealthInsuranceCompany, HealthInsurancePriceList, HealthInsuranceUserDiscount, HealthInsuranceRequest
from .serializers import HealthInsurancePriceListSerializer, HealthInsuranceCompanySerializer, HealthInsuranceRequestSerializer, HealthInsuranceUserDiscountSerializer
from main.models import Wallet, Currency
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import requests
import json


def checkid(id):
    if not id.isnumeric():
        return Response({'data': 'ID Should Be a Number'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

# Create your views here.


class HealthInsuranceDetails(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        checkid(request.data['id'])
        if not len(HealthInsuranceRequest.objects.filter(id=request.data['id'])):
            return Response({'data': 'Invalid ID'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        query = HealthInsuranceRequest.objects.filter(
            id=request.data['id']).first()
        serializer = HealthInsuranceRequestSerializer(
            query, context={'user': request.user})
        return Response(serializer.data)


class HealthInsurancePriceLists(APIView):

    def post(self, request):
        serializer = []
        age = relativedelta(datetime.now(), datetime.strptime(
            request.data['birthday_date'], '%Y-%m-%d')).years
        query1 = HealthInsuranceCompany.objects.all()
        for item in query1:
            if len(HealthInsurancePriceList.objects.filter(company=item, start_age__lte=int(age), end_age__gte=int(age))):
                if len(HealthInsuranceUserDiscount.objects.filter(user=request.user)):
                    dis = HealthInsuranceUserDiscount.objects.filter(
                        user=request.user).order_by('-last_modify_date').first()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                elif len(HealthInsuranceUserDiscount.objects.filter(user=None)):
                    dis = HealthInsuranceUserDiscount.objects.filter(
                        user=None).order_by('-last_modify_date').first()
                serializer.append({'company': HealthInsuranceCompanySerializer([item], many=True).data[0], 'pricelist': HealthInsurancePriceListSerializer(
                    HealthInsurancePriceList.objects.filter(company=item, start_age__lte=int(age), end_age__gte=int(age)), many=True, context={'user': request.user}).data[0]})
        return Response({'age': age, 'data': tuple(serializer)})


class HealthInsurancePriceLists2(APIView):

    def post(self, request):
        payload = {
            "policebaslangictarihi": "30.09.2022",
            "sigortalidogumtarihi": "07.08.2000",
            "uyrukid": 3,
            "policesuresi": 2
        }
        headers = {
            "username": "TurkeyRahyab",
            "password": "12345",
        }
        r = requests.post('https://destek.mpsyazilim.com/veriEntegrasyonWS/VeriEntegrasyonWebServer.dll/yabancisaglikfiyatihesapla',
                          params=payload, headers=headers)
        r = r.json()['Result']
        serializer = []
        for item in r:
            serializer.append(
                {'company': {'id': item['sirketid'], 'name': item['sirketadi'], 'image': '', 'get_image': ''}, 'pricelist': {'id': '', 'company': item['sirketid'], 'get_company_name': item['sirketadi'], 'get_company_image': '', 'first_year': item['ilkyilpolicetutari'], 'second_year': item['ikinciyilpolicetutari'], 'sum': item['toplampolicetutari'], 'discount_percent': item['indirimorani']}})
        return Response(serializer)


class HealthInsuranceRequests(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = HealthInsuranceRequestSerializer(
            data=request.data, context={'user': request.user, 'insurance': request.data['insurance']})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class CheckDiscount(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if len(HealthInsuranceUserDiscount.objects.filter(user=request.user)):
            dis = HealthInsuranceUserDiscount.objects.filter(
                user=request.user).order_by('-last_modify_date').first()
            serializer = HealthInsuranceUserDiscountSerializer(dis)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif len(HealthInsuranceUserDiscount.objects.filter(user=None)):
            dis = HealthInsuranceUserDiscount.objects.filter(
                user=None).order_by('-last_modify_date').first()
            serializer = HealthInsuranceUserDiscountSerializer(dis)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'data': 'There is no discount for you'}, status=status.HTTP_404_NOT_FOUND)


class MyInsurances(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = HealthInsuranceRequest.objects.filter(user=request.user.id)
        serializer = HealthInsuranceRequestSerializer(
            query, many=True, context={'user': request.user})
        return Response(serializer.data)


class HealthInsurancePayment(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        checkid(request.data['id'])
        if not len(HealthInsuranceRequest.objects.filter(id=request.data['id'])):
            return Response({'data': 'ID Not Found'}, status=status.HTTP_404_NOT_FOUND)
        req = HealthInsuranceRequest.objects.get(id=request.data['id'])
        if req.period == 1:
            price = req.first_year
        else:
            price = req.second_year
        wallet = Wallet.objects.get(
            user=request.user, currency=Currency.objects.get(symbol='TRL').id)
        if wallet.balance >= price:
            wallet.balance = wallet.balance - price
            wallet.save()
            req.payment_status = True
        else:
            return Response({'data': 'Insufficient Balance'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


'''



'''
