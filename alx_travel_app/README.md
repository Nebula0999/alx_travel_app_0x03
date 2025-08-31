# alx_travel_app_0x00

A Django-based travel listing application with user, listing, booking, and review management.

## Features

- User registration and management (custom `User` model)
- Create, view, and manage travel listings
- Bookings for listings with start and end dates
- Reviews for listings
- REST API with Django REST Framework
- API documentation via Swagger and ReDoc (drf-yasg)

## Project Structure

## Main Components

### Models

- **User**: Custom user with roles (guest, host, admin), phone number, and timestamps.
- **Listing**: Travel listing with title, description, price, location, and host.
- **Booking**: Booking for a listing by a user, with start/end dates.
- **Review**: User review for a listing, with rating and comment.

### Serializers

- Serializers for User, Listing, Booking, and Review for API representation.

### API Documentation

- Swagger UI: `/swagger/`
- ReDoc UI: `/redoc/`

### Management Commands

- `seed.py`: (To be implemented) Command to populate the database with sample data.

## Setup

1. Install dependencies:
    ```sh
    pip install -r requirement.txt
    ```
2. Run migrations:
    ```sh
    python manage.py migrate
    ```
3. (Optional) Seed the database:
    ```sh
    python manage.py seed
    ```
4. Run the development server:
    ```sh
    python manage.py runserver
    ```

## Requirements

See [requirement.txt](requirement.txt).

## License

### ViewSets

- **UserViewSet**: Handles user CRUD operations and authentication endpoints.
- **ListingViewSet**: Manages travel listings (create, retrieve, update, delete).
- **BookingViewSet**: Handles booking creation, listing, and management.
- **ReviewViewSet**: Manages reviews for listings (create, list, update, delete).

### Celery Integration

- **Purpose**: Celery is used in this project to handle asynchronous tasks, specifically for sending emails (such as booking confirmations, password resets, etc.).
- **How it works**: When an action requires an email to be sent (e.g., a user makes a booking), the email sending task is queued and processed by Celery workers in the background. This ensures the main application remains responsive and users don’t experience delays.
- **Configuration**: Celery is configured with a message broker (like Redis or RabbitMQ). Email tasks are defined in a separate tasks module and called from relevant viewsets or signals.
- **Example usage**:
    - After a booking is created, the `BookingViewSet` triggers a Celery task to send a confirmation email to the user.

