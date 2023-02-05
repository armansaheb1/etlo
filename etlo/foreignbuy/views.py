from django.shortcuts import render

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import ForeignBuyRequests
from .serializers import ForeignBuyRequestsSerializer
from main.models import Wallet, Currency
# Create your views here.


def checkid(id):
    if not id.isnumeric():
        return Response({'data': 'ID Should Be a Number'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ForeignBuyRequestDetails(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        checkid(request.data['id'])
        if not len(ForeignBuyRequests.objects.filter(id=request.data['id'])):
            return Response({'data': 'Invalid ID'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        query = ForeignBuyRequests.objects.filter(id=request.data['id'])
        serializer = ForeignBuyRequestsSerializer(query, many=True)
        return Response({'data': serializer.data})


class ForeignBuyRequest(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = ForeignBuyRequests.objects.filter(user=request.user)
        serializer = ForeignBuyRequestsSerializer(query, many=True)
        return Response({'data': serializer.data})

    def post(self, request):
        request.data._mutable = True
        request.data['user'] = request.user.id
        serializer = ForeignBuyRequestsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data})
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def put(self, request, id):
        checkid(id)
        try:
            request.data._mutable = True
            request.data['user'] = request.user.id
            serializer = ForeignBuyRequestsSerializer(
                ForeignBuyRequests.objects.get(id=id), data=request.data,)
            if serializer.is_valid():
                serializer.save()
                return Response({'data': serializer.data})
            else:
                return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({'data': 'ID Not Found'}, status=status.HTTP_404_NOT_FOUND)


class ForeignBuyRequestDetails(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        checkid(id)
        query = ForeignBuyRequests.objects.filter(id=id)
        serializer = ForeignBuyRequestsSerializer(query, many=True)
        return Response({'data': serializer.data})


class ForeignBuyPayment(APIView):
    authentication_classes = [SessionAuthentication,
                              BasicAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        reqs = ForeignBuyRequests.objects.filter(payment_status=False)
        if not len(reqs):
            return Response({'data': 'Cart is empty'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not len(Wallet.objects.filter(currency=Currency.objects.get(symbol='IRT'))):
            return Response({'data': 'Insufficient Balance'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        price = 0
        for item in reqs:
            price = price + item.pay_price()
        wallet = Wallet.objects.get(
            user=request.user, currency=Currency.objects.get(symbol='IRT').id)
        if wallet.balance >= price:
            wallet.balance = wallet.balance - price
            wallet.save()
            for item in reqs:
                item.payment_status = True
                item.save()
                return Response(status=status.HTTP_200_OK)
        else:
            return Response({'data': 'Insufficient Balance'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
