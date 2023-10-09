# Quickfire Bulletin

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technical Stack](#technical-stack)
- [Installation](#installation)
- [Development](#development)
  - [Initial Setup](#initial-setup)
  - [API Integration](#api-integration)
  - [Debugging and Error Handling](#debugging-and-error-handling)
  - [User Interface](#user-interface)
  - [Admin Dashboard](#admin-dashboard)
  - [Commenting and Likes](#commenting-and-likes)
  - [Text Formatting](#text-formatting)
  - [Deployment](#deployment)
  - [Troubleshooting](#troubleshooting)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting-1)
- [Contributing](#contributing)
- [License](#license)

## Overview

Quickfire Bulletin is a Django-based web application that serves as a news bulletin platform. It allows users to read news articles fetched from an external API, comment on them, and like each other's comments. The application is designed with a focus on modularity and extensibility, allowing for easy integration of additional features.

## Features

- **News API Integration**: The application fetches news articles from the NewsData.io API and populates the database with the latest news.
- **User Authentication**: Users can register, log in, and log out.
- **Admin Dashboard**: Admin users have the ability to edit or delete news articles.
- **Commenting**: Users can comment on news articles.
- **Likes**: Users can like each other's comments.
- **Pagination**: The home page displays news articles in a paginated format.

## Technical Stack

- **Backend**: Python, Django
- **Frontend**: HTML, CSS
- **Database**: PostgreSQL
- **Static Files**: Managed using Whitenoise
- **API**: NewsData.io

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/quickfire_bulletin.git
    ```

2. Navigate to the project directory:
    ```bash
    cd quickfire_bulletin
    ```

3. Create a virtual environment:
    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:
    ```bash
    source venv/bin/activate  # Linux/Mac
    # or
    .\\venv\\Scripts\\Activate  # Windows
    ```

5. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

6. Create a `.env` file in the project root and add your environment variables:
    ```env
    SECRET_KEY=your_secret_key
    DEBUG=True
    DATABASE_URL=your_database_url
    NEWS_API_KEY=your_news_api_key
    ```

7. Run migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

8. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

9. Run the development server:
    ```bash
    python manage.py runserver
    ```
## Development

The development of Quickfire Bulletin involved several key steps and challenges, which are outlined below:

### Initial Setup

The project started with the basic setup of a Django project and the creation of a main app to handle the core functionality. The initial setup also included configuring the database and setting up user authentication.

### API Integration

One of the first major tasks was to integrate the NewsData.io API to fetch news articles. This involved writing a function (`fetch_news`) that makes an HTTP request to the API, processes the JSON response, and populates the database with news articles.

### Debugging and Error Handling

During the development, several issues were encountered, such as missing imports, API key errors, and database issues. These were debugged using Django's built-in debugging tools, logging, and Python's traceback module.

### User Interface

The frontend was designed using HTML and CSS. Pagination was implemented to display a limited number of articles per page. The UI also includes forms for user registration, login, and commenting.

### Admin Dashboard

An admin dashboard was created using Django's built-in admin interface. This allows admin users to manage news articles and user accounts.

### Commenting and Likes

The ability for users to comment on articles and like each other's comments was added. This involved creating new models and forms, as well as modifying the views and templates.

### Text Formatting

The news articles fetched from the API initially appeared as a single text string without line breaks. A text processing step was added to divide the content into paragraphs for better readability.

### Deployment

The application was prepared for deployment with the inclusion of Whitenoise for static file management.

### Troubleshooting

Several issues were encountered during development, such as:

- Missing 'articles' key in the API response
- Admin panel access issues
- Static file management with Whitenoise

Each of these issues required specific troubleshooting steps, including code debugging, environment variable checks, and server log reviews.

By overcoming these challenges, the project has reached its current state, offering a robust set of features for a news bulletin platform.

## Usage

1. Open your web browser and navigate to `http://127.0.0.1:8000/`.
2. Use the admin dashboard at `http://127.0.0.1:8000/admin` to manage news articles and user accounts.

## Troubleshooting

- If you encounter issues with missing imports, make sure all dependencies are installed and the virtual environment is activated.
- If the news articles are not displaying, check the API key and the fetch function.
- If you encounter issues with the admin panel, make sure the superuser is created and you are logged in as the superuser.

## Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.
