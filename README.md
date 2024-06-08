# Socialnetwork
# Social Network API

This is a social networking application API built with Django and Django Rest Framework.

## Installation

Follow these steps to set up the project on your local machine.

### Prerequisites

- Python 3.x
- pip (Python package installer)
- virtualenv (optional but recommended)

### Steps

1. **Clone the repository**:

    ```sh
    git clone https://github.com/tamilarasana/Socialnetwork.git
    cd Socialnetwork
    ```

2. **Create and activate a virtual environment (optional but recommended)**:

    ```
    1. pip install shell
    2. pipenv shell   
    ```

3. **Install the dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

4. **Apply migrations**:

    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a superuser**:

    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server**:

    ```sh
    python manage.py runserver
    ```

7. **Access the application**:
    The application will be available at `http://localhost:8000`.

## Usage
 Hints: In This project i added one file Socialnetwork.postman_collection.json use this one for all api collection just import your Postman

Ex:
- **Signup**: `POST  http://127.0.0.1:8000/members/signup/`
- **Login**: `POST  http://127.0.0.1:8000/members/login/`
- **Search**: `GET  http://127.0.0.1:8000/members/search/?keyword=a`
- **Search**: `POST  http://127.0.0.1:8000/members/friend_req/`
- **Friends Request**: `POST  http://127.0.0.1:8000/members/friend_req/`
- **Friendts Request By id**: `POST http://127.0.0.1:8000/members/friend_request/1/`
- **Friends**: ` GET http://127.0.0.1:8000/members/friends/?user_id=1`
- **Pending Request**: `GET http://127.0.0.1:8000/members/pending_request/?user_id=1`

### Example of an authenticated request
 Example of Authorization Token in Headers
    Key: Authorization
    Value: Token e937df23d0bcb79b0a148f6c9674865b16ee3945

```sh
curl -H "Authorization: Token your_token" http://localhost:8000/api/search/?keyword=am

