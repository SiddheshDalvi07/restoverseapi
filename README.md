Here's a README file based on the project details you provided:

---

# Google Login and Review Section Integration

## Project Overview

This project integrates **Google OAuth 2.0 login** with a review and comment system. Users can log in using their Google account, post reviews, and comment on existing reviews. The project is built with **Django** for the backend and **React.js** for the frontend, ensuring a full stack implementation.

## Technologies Used

### Frontend
- **React.js**
- **Redux** (State Management)
- **Bootstrap** (Responsive Design)
- **CSS** (Styling)

### Backend
- **Django** (Python Web Framework)
- **Django Rest Framework** (API Development)

### Authentication
- **Google OAuth 2.0** (Google Login)

### Database
- **SQLite** (Default Django Database)

### APIs
- **Google Business Profile Performance API** (for retrieving business data)

## Features

- **Google Login**: Users can log in using their Google accounts through OAuth 2.0.
- **Review Section**: Users can post reviews.
- **Comment System**: Users can reply and comment on reviews.
- **Responsive Design**: The UI is built to be responsive and intuitive across devices.
- **Secure Authentication**: Google OAuth provides secure authentication, and Redux is used for efficient state management.

## Project Setup

### Backend Setup (Django)

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/SiddheshDalvi07/restoverseapi.git
    cd backend
    ```

2. **Install Required Python Packages**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run Migrations to Set Up the Database**:
    ```bash
    python manage.py migrate
    ```

4. **Start the Django Development Server**:
    ```bash
    python manage.py runserver
    ```

### Frontend Setup (React)

1. **Navigate to the Frontend Folder**:
    ```bash
    cd frontend
    ```

2. **Install the Required npm Packages**:
    ```bash
    npm install
    ```

3. **Start the React Development Server**:
    ```bash
    npm run dev
    ```

## Google Login Integration

### Google OAuth 2.0 Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. Navigate to the **Credentials** section and create an **OAuth 2.0 Client ID**.
4. Configure the **Authorized redirect URIs** to include your backend's login endpoint.
5. Save the **Client ID** and **Client Secret** for later use in both Django and React configuration.

### Backend Implementation (Django)

1. **Install the Required Django Package**:
    ```bash
    pip install social-auth-app-django
    ```

2. **Configure Google Login** in your `settings.py`:
    ```python
    AUTHENTICATION_BACKENDS = (
        'social_core.backends.google.GoogleOAuth2',
        ...
    )

    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '<your-client-id>'
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '<your-client-secret>'
    ```

3. **Update URL Configuration**:
    Make sure to add the appropriate URLs for handling Google login.

### Frontend Implementation (React)

1. **Install the Google Login npm Package**:
    ```bash
    npm install react-google-login
    ```

2. **Handle Google Login**:
    - Use the `react-google-login` package to trigger Google login and store the user’s details (name, email, profile picture) in the Redux store.

3. **Display User Data**:
    - After a successful login, display user details (name, email, profile picture) and give the user the ability to post reviews and comments.

## Testing

- **Google Login**: Test the Google login functionality with different Google accounts.
- **Review & Comment**: Ensure that users can add reviews and reply to existing reviews.
- **Multi-User Functionality**: Verify that the review and comment system works as expected with multiple users.

## Conclusion

This project demonstrates how to integrate **Google OAuth 2.0 login** and implement a review and comment system in a full-stack web application using **Django** and **React**. By leveraging OAuth 2.0 and REST APIs, the application ensures secure authentication and efficient data management.
