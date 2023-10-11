# Quickfire Bulletin

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technical Stack](#technical-stack)
- [Installation](#installation)
- [Development](#development)
  - [Initial Setup](#initial-setup)
  - [API Integration](#api-integration)
  - [Natural Language Processing](#natural-language-processing)
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

  ## User Stories

### Admin Stories

As an admin, you can:
- Log in and access the admin panel.
- Create, edit, and delete posts.
- Manage user accounts.
- Organize posts into categories.
- Monitor user activity.

### User Stories

As a user, you can:
- Register an account or log in.
- View the latest posts.
- Filter posts by category.
- Comment on posts.
- Receive notifications for new posts and comments.
- Search for specific posts.

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

### Natural Language Processing
Using Natural Language Processing my Quickfire Bulletin application enhances text readability by intelligently dividing articles into coherent paragraphs. NLP understands the context and semantic structure, ensuring each paragraph focuses on a single idea. This not only improves user experience but also scales easily as the platform grows. Well-structured content can also boost user engagement and potentially improve SEO rankings. Overall, NLP offers a dynamic, automated solution for text formatting, crucial for delivering easily digestible news articles.

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
I used Natural Language Processing in this step. 

### Deployment

The application was prepared for deployment with the inclusion of Whitenoise for static file management.

### Troubleshooting

## Issue 1: Form Validation

### Problem:
When testing the app's comment submission form, I noticed that the form was submitting even when some fields were left empty.

### Solution:
To ensure data integrity, I implemented client-side form validation using JavaScript. This validation checks whether the "Name," "Email," and "Comment" fields are all filled out before allowing form submission. This way, users are prompted to provide all required information before submitting a comment.

## Issue 2: Missing Fields in Form

### Problem:
The comment form initially lacked "Name" and "Email" fields.

### Solution:
I integrated the "Name" and "Email" fields into the comment form to gather additional user information when submitting a comment. These fields were added as text input and email input fields, respectively.

## Issue 3: Form Data Not Including Name and Email

### Problem:
Even after adding "Name" and "Email" fields to the form, the form data being sent to the server did not include this information.

### Solution:
To include the "Name" and "Email" in the form data when submitting a comment, I modified the JavaScript code that handles form submission. Specifically, I added code to retrieve the values of these fields and append them to the form data using the `formData.append()` method.

By addressing these issues, I improved the functionality and usability of the app's comment submission feature, ensuring that users provide complete information and that all relevant data is sent to the server for processing.


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
