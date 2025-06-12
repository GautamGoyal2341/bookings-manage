from django.db import transaction
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.pagination import  LimitOffsetPagination

from bookings.permissions import IsAdminUser
from .models import Room, Booking, User
from .serializers import (
    CreateBookingSerializer,
    BookingSerializer,
    RoomSerializer,
    UserSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'error': 'Email and password required'}, status=400)
    
    try:
        user = User.objects.get(email=email)
        # For Now simplicity, I we'll storing plain text password now
        # In production, we use proper password hashing
        if user.password == password: 
            return Response({
                'user_id': user.id,
                'email': user.email,
                'name': user.name,
                'role': user.role,
                'message': 'Login successful'
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=401)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    

class SimpleAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user_id = request.META.get('HTTP_USER_ID')
        if not user_id:
            return None
            
        try:
            user = User.objects.get(id=user_id)
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed('Invalid user ID')



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# BOOKING API
class BookingCreateView(APIView):
    def post(self, request):
        serializer = CreateBookingSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        slot = data['slot']
        room_type = data['room_type']
        user_id = data.get('user_id')
        team_id = data.get('team_id')

        try:
            with transaction.atomic():
                if room_type == 'SHARED':
                    # Try to find a shared room with less than 4 bookings in this slot
                    for room in Room.objects.filter(room_type='SHARED'):
                        current_count = Booking.objects.filter(room=room, slot=slot).count()
                        if current_count < room.capacity:
                            booking = Booking.objects.create(
                                slot=slot,
                                room=room,
                                user_id=user_id
                            )
                            return Response({'booking_id': booking.id}, status=status.HTTP_201_CREATED)
                    return Response({'detail': 'No available shared desks for the selected slot.'}, status=400)

                # For PRIVATE or CONFERENCE
                # Get all available rooms of that type for the slot
                booked_room_ids = Booking.objects.filter(slot=slot).values_list('room_id', flat=True)
                available_rooms = Room.objects.filter(room_type=room_type).exclude(id__in=booked_room_ids)

                if not available_rooms.exists():
                    return Response({'detail': 'No available room for the selected slot and type.'}, status=400)

                room = available_rooms.first()
                booking = Booking.objects.create(
                    slot=slot,
                    room=room,
                    user_id=user_id if user_id else None,
                    team_id=team_id if team_id else None
                )
                return Response({'booking_id': booking.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'detail': str(e)}, status=500)



# 2️ CANCEL BOOKING API
class CancelBookingView(APIView):
    authentication_classes = [SimpleAuthentication]
    permission_classes = [IsAdminUser]
    
    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id)
            booking.delete()
            return Response({'detail': 'Booking cancelled.'}, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({'detail': 'Booking not found.'}, status=404)



class BookingPagination(LimitOffsetPagination):
    default_limit = 20  # Number of bookings per page
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 100  # Maximum allowed limit

# 3️ LIST ALL BOOKINGS
class BookingListView(ListAPIView):
    serializer_class = BookingSerializer
    pagination_class = BookingPagination
    
    def get_queryset(self):
        return Booking.objects.select_related(
            'room', 'user', 'team'
        ).all().order_by('-slot')


# 4️ AVAILABLE ROOMS API
class AvailableRoomsView(APIView):


    def get(self, request):
        slot = request.GET.get('slot')
        if not slot:
            return Response({'detail': 'Query param "slot" is required.'}, status=400)

        try:
            slot = timezone.datetime.fromisoformat(slot)
        except Exception:
            return Response({'detail': 'Invalid datetime format. Use ISO format (YYYY-MM-DDTHH:00).'}, status=400)

        booked_room_ids = Booking.objects.filter(slot=slot).values_list('room_id', flat=True)
        available_rooms = Room.objects.exclude(id__in=booked_room_ids)

        serializer = RoomSerializer(available_rooms, many=True)
        return Response(serializer.data)


class RoomListView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)