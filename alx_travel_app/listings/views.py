from django.shortcuts import render
from rest_framework import viewsets
from .models import User, Booking, Listing, Review, Payment
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, BookingSerializer, ListingSerializer, ReviewSerializer
from rest_framework import status
from django.conf import settings
import requests

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing booking instances.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class ListingViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing listing instances.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

# Create your views here.

class InitiatePaymentView(APIView):
    def post(self, request):
        booking_ref = request.data.get("booking_reference")
        amount = request.data.get("amount")
        email = request.data.get("email")
        currency = "ETB"  # Adjust if needed

        payload = {
            "amount": str(amount),
            "currency": currency,
            "email": email,
            "tx_ref": booking_ref,
            "callback_url": "http://127.0.0.1:8000/api/verify-payment/"
        }

        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
        }

        response = requests.post(
            f"{settings.CHAPA_API_BASE_URL}/transaction/initialize",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            data = response.json()
            tx_id = data.get("data", {}).get("tx_ref")

            Payment.objects.create(
                booking_reference=booking_ref,
                amount=amount,
                transaction_id=tx_id,
                status="Pending"
            )

            return Response({"checkout_url": data.get("data", {}).get("checkout_url")})
        else:
            return Response({"error": "Payment initiation failed"}, status=status.HTTP_400_BAD_REQUEST)

class VerifyPaymentView(APIView):
    def get(self, request):
        tx_ref = request.query_params.get("tx_ref")
        if not tx_ref:
            return Response({"error": "Transaction reference required"}, status=status.HTTP_400_BAD_REQUEST)

        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
        }

        verify_url = f"{settings.CHAPA_API_BASE_URL}/transaction/verify/{tx_ref}"
        response = requests.get(verify_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            status_text = data.get("data", {}).get("status", "Failed").capitalize()

            Payment.objects.filter(transaction_id=tx_ref).update(status=status_text)

            return Response({"status": status_text})
        else:
            return Response({"error": "Verification failed"}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import viewsets
from .models import Booking
from .serializers import BookingSerializer
from .tasks import send_booking_confirmation_email

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save()
        user_email = booking.user.email  # adjust based on your model
        send_booking_confirmation_email.delay(user_email, booking.id)
