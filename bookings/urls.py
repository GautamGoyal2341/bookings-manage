# bookings/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BookingCreateView,
    CancelBookingView,
    BookingListView,
    AvailableRoomsView,
    UserViewSet,
    login_view,
    RoomListView
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Authentication
    path('auth/login/', login_view, name='login'),
    
    # Booking endpoints
    path('bookings/', BookingCreateView.as_view(), name='create-booking'),
    path('rooms/', RoomListView.as_view(), name='all-rooms'),
    path('bookings/all/', BookingListView.as_view(), name='list-bookings'),
    path('cancel/<uuid:booking_id>/', CancelBookingView.as_view(), name='cancel-booking'),
    path('rooms/available/', AvailableRoomsView.as_view(), name='available-rooms'),
    path('', include(router.urls)), 
]
