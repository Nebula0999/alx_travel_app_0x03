from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, BookingViewSet, ListingViewSet, InitiatePaymentView, VerifyPaymentView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'listings', ListingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("initiate-payment/", InitiatePaymentView.as_view(), name="initiate-payment"),
    path("verify-payment/", VerifyPaymentView.as_view(), name="verify-payment"),
]