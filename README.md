# Secure Django API

## Overview

This project sets up a Django application with Django REST Framework (DRF) to provide two API endpoints: `get_details` and `save_details`. It uses Cerbos, an authorization service, to handle role-based access control. The application is containerized with Docker, and a `docker-compose` file is provided to orchestrate the services.

## Project Structure

- **Dockerfile**: Defines the Docker image for the Django application.
- **docker-compose.yml**: Sets up the services including Django, PostgreSQL, and Cerbos.
- **tondo_project/transactions/views.py**: Contains the views for handling API requests.
- **tondo_project/transactions/urls.py**: Defines the URL routes for the API.
- **tondo_project/transactions/models.py**: Defines the `Transaction` model.
- **tondo_project/transactions/serializers.py**: Serializes the `Transaction` model.
- **tondo_project/transactions/services/cerbos_client.py**: Communicates with Cerbos for authorization checks.
- **tondo_project/transactions/services/user_roles.py**: Provides static user role mappings.
- **tondo_project/transactions/tests.py**: Contains tests for the API endpoints.

## Endpoints

### `GET /api/get_details`

Fetches transaction details. Authorization is based on user roles.

**Headers:**
- `userid`: The ID of the user making the request.

**Response:**
- `200 OK`: If the user has permission.
- `403 Forbidden`: If the user does not have permission.

### `POST /api/save_details`

Saves a new transaction. Authorization is based on user roles.

**Headers:**
- `userid`: The ID of the user making the request.

**Request Body:**
```json
{
  "date_time": "2024-08-29T12:00:00Z",
  "currency": "USD",
  "sender": "Alice",
  "receiver": "Bob",
  "transaction_type": "transfer"
}
```

**Response:**
- `200 OK`: If the user has permission and the data is valid.
- `400 Bad Request`: If the data is invalid or missing.
- `403 Forbidden`: If the user does not have permission.

## Setup

### Prerequisites

- Docker
- Docker Compose

### Build and Run

1. **Clone the Repository**

   ```bash
   git clone https://github.com/RazElbaz/Secure-Django-API.git
   cd Secure-Django-API/tondo_project
   ```

2. **Build the Docker Image**

   ```bash
   docker-compose build
   ```

3. **Start the Services**

   ```bash
   docker-compose up
   ```

4. **Database Migration**

   In a new terminal, run:

   ```bash
   docker-compose exec django python manage.py migrate
   ```

5. **Stop and Remove Containers**

   To stop and remove all running containers, use:

   ```bash
   docker-compose down
   ```

### Configuration

- **Cerbos**: The configuration file `tondo_project/cerbos/config/conf.yaml` defines the Cerbos setup and policies.

## Testing

Run tests using Django's test suite:

```bash
docker-compose run django python manage.py test
```

## Notes

- User roles are hardcoded in `tondo_project/transactions/services/user_roles.py`.
- Ensure Cerbos policies are correctly defined in `tondo_project/cerbos/policies/transaction.yaml`.

## References

- [Django REST Framework: Creating an API](https://blog.logrocket.com/django-rest-framework-create-api/)
- [Cerbos: Adding Global Authorization for Python Microservices](https://www.cerbos.dev/blog/how-to-add-global-authorization-for-python-microservices)
- [Cerbos Documentation: Calling Cerbos](https://docs.cerbos.dev/cerbos/latest/tutorial/03_calling-cerbos.html)

https://blog.logrocket.com/django-rest-framework-create-api/
https://www.cerbos.dev/blog/how-to-add-global-authorization-for-python-microservices
https://docs.cerbos.dev/cerbos/latest/tutorial/03_calling-cerbos.html