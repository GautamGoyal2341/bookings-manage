# Workspace Room Booking System

A Django REST Framework-based system for managing bookings of shared, private, and conference rooms within an organization. It supports team-based bookings, capacity handling, pagination, and admin role-based booking cancellations.

## 🚀 Setup Instructions

### 1. Clone the repository

git clone https://github.com/GautamGoyal2341/bookings-manage
cd bookingsmanage

2. Environment Variables
   Create a .env file in the root directory:

SECRET_KEY=your-secret-key
DEBUG=1
DATABASE_URL=postgres://postgres:postgres@db:5432/workspace_booking

3. Build and Run with Docker

docker-compose up --build

4. Run Initial Setup Commands

# Create default users (admin and regular user)

docker-compose exec web python manage.py create_default_users

# Create some default rooms (shared, private, conference)

docker-compose exec web python manage.py create_default_rooms

🧪 Assumptions Made
Admin-only permissions for booking cancellation are hard-coded.

Room double-booking is prevented based on time slot + duration overlap logic.

Children under 10 are included in booking headcount but do not occupy full seats.

# 📚 API Documentation

All endpoints follow RESTful conventions and are grouped below by functionality.

## 🔐 Authentication

### POST `/auth/login/`

Simulates user login.

**Request:**

```json
{
  "email": "admin@example.com",
  "password": "admin123"
}
```

**Response:**

```json
{
  "user_id": 3,
  "email": "admin@example.com",
  "name": "Admin User",
  "role": "ADMIN",
  "message": "Login successful"
}
```

## 🏢 Rooms

### GET /rooms/

List all rooms.

### GET `/rooms/available/?slot=<datetime>`

Check for available rooms at a given time.

**Example:**

```
GET /rooms/available/?slot=2025-06-12T10:00:00Z
```

**Response:**

```json
[
  {
    "user_id": "uuid",
    "room_type": "",
    "capacity": ""
  }
]
```

## 📅 Bookings

### POST `/bookings/`

Book a room.

**Request:**

```json
{
  "team_id": "team-uuid",
  "user_id": 1,
  "slot": "2025-06-12T11:00:00Z",
  "room_type": "PRIVATE"
}
```

**Response:**

```json
{
  "booking_id": "booking-uuid"
}
```

### GET `/bookings/all/`

Returns paginated list of all bookings (default page size: 10).

**Query Parameters:**

- `page`: Page number (optional)

**Response:**

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "ee5f4b59-1253-403c-bce2-b9624db2321d",
      "slot": "2025-07-12T10:00:00Z",
      "room": {
        "id": 1,
        "room_type": "PRIVATE",
        "capacity": 1
      },
      "user": {
        "id": 1,
        "name": "Alice",
        "age": 28,
        "gender": "female"
      },
      "team": null,
      "created_at": "2025-06-12T18:42:38.967750Z"
    }
  ]
}
```

### POST `/cancel/<booking_id>/`

**Headers:**

```
User-Id: {{admin_id}}
```

**Example:**

```bash
curl --location --request POST 'http://127.0.0.1:8000/api/v1/cancel/ee5f4b59-1253-403c-bce2-b9624db2321d/' \
--header 'User-Id: 3'
```

Cancel a booking (Admin only).

**Success Response:**

```json
{
  "detail": "Booking cancelled successfully."
}
```

## 📋 API Endpoints Summary

| Method | Route                   | Description                 |
| ------ | ----------------------- | --------------------------- |
| POST   | `/auth/login/`          | Mock login                  |
| GET    | `/rooms/`               | List all rooms              |
| GET    | `/rooms/available/`     | Available room lookup       |
| POST   | `/bookings/`            | Book a room                 |
| GET    | `/bookings/all/`        | View all bookings           |
| POST   | `/cancel/<booking_id>/` | Cancel booking (admin only) |
| POST   | `/users/`               | Add new user                |

## 🔑 Default Users

| Role  | Username       | Password   |
| ----- | -------------- | ---------- |
| Admin | `Admin User`   | `admin123` |
| User  | `	Regular User` | `user123`  |

### Creating Django Admin User

To access the Django admin panel, create a superuser:

```bash
docker-compose exec web python manage.py createsuperuser
```

Follow the prompts:

- **Username**: `root` (or leave blank to use default)
- **Email address**: (optional)
- **Password**: 

**Access Admin Panel**: http://127.0.0.1:8000/admin/

### 📦 Postman Collection

A Postman collection is available with all the above endpoints pre-configured for easy testing and integration.
How to use:

Download the collection JSON file from the link below
Open Postman
Click "Import" and paste the JSON content directly
All endpoints will be ready for testing

Link : https://drive.google.com/drive/folders/1KjlL4hoas5GWI-SLH6QOEcENPSxebFS-?usp=sharing
