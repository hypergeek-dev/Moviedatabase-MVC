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
    - [Issue 1: Form Validation](#issue-1-form-validation)
    - [Issue 2: Missing Fields in Form](#issue-2-missing-fields-in-form)
    - [Issue 3: Form Data Not Including Name and Email](#issue-3-form-data-not-including-name-and-email)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting-1)
- [Contributing](#contributing)
- [License](#license)

## Overview

Quickfire Bulletin is a Django-based web application that serves as a news bulletin platform. It allows users to read news articles fetched from an external API, comment on them, and like each other's comments. The application is designed with a focus on modularity and extensibility, allowing for easy integration of additional features.

[The site is live here](https://quickfire-bulletin-1054d3494a4d.herokuapp.com/)

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
6. Download the NLP model
    python -m spacy download en_core_web_sm

7. Create a `.env` file in the project root and add your environment variables:
    ```env
    SECRET_KEY=your_secret_key
    DEBUG=True
    DATABASE_URL=your_database_url
    NEWS_API_KEY=your_news_api_key
    ```

8. Run migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

9. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

10. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Development

The development of Quickfire Bulletin involved several key steps and challenges, which are outlined below:

### Initial Setup

The project started with the basic setup of a Django project and the creation of a main app to handle the core functionality. The initial setup also included configuring the database and setting up user authentication.

### API Integration

One of the first major tasks was to integrate the NewsData.io API to fetch news articles. This involved writing a function (`fetch_news`) that makes an HTTP request to the API, processes the JSON response, and populates the database with news articles.


## Testing

### Comments

Automatic testing has been created for the add, edit and delete comment function.

1. Ensures the user is authenticated.
2. Creates a mock article object or use a fixture to insert an article into the test database.
3. Simulates a POST request with valid form data.
4. Asserts that the response indicates success and the comment has been added to the database.


### Feedback form

#### GET Request Test
- **Status Code:** Ensures the feedback page is accessible with a 200 OK response.
- **Template Use:** Confirms `feedback.html` is used for the feedback form.
- **Form Instance:** Verifies `FeedbackForm` is passed to the template.

#### POST Request Test (Invalid Data)
- **Status Code:** Checks for a 200 OK response, indicating the form is reloaded with errors.
- **Form Error:** Validates the presence of expected errors for missing or invalid data.


### Debugging and Error Handling

### Troubleshooting

#### Issue 1: Form Validation

**Problem**:
When testing the app's comment submission form, I noticed that the form was submitting even when some fields were left empty.

**Solution**:
To ensure data integrity, I implemented client-side form validation using JavaScript. This validation checks whether the "Name," "Email," and "Comment" fields are all filled out before allowing form submission. This way, users are prompted to provide all required information before submitting a comment.

#### Issue 2: Missing Fields in Form

**Problem**:
Initially the comment form initially lacked "Name" and "Email" fields. When I integrated the "Name" and "Email" fields into the comment form to gather additional user information when submitting a comment the form data being sent to the server did not include this information.

**Solution**:
To include the "Name" and "Email" in the form data when submitting a comment, I modified the JavaScript code that handles form submission. Specifically, I added code to retrieve the values of these fields and append them to the form data using the `formData.append()` method.

#### Issue 3.

### Text Formatting

The news articles fetched from the API initially appeared as a single text string without line breaks. A text processing step was added to divide the content into paragraphs for better readability. I used a Natural Language Processing model from spacy called `en_core_web_sm` and python logic to break lines into statements and parce dem nicely as a readable text-article.

#### Issue 4.

During development, the newsapi.io made changes to their policy on free accounts making the content of articles only available to paying users. That caused the limitation of not being able to get new content. 

**solution**

I migrated the content of the database and created a local SQlite database for demonstration purposes. Users will have to find either another free news api or be a paid user to use this app successfully.

## Wireframes

Here are wireframes illustrating the initial design of Quickfire Bulletin:

![Wireframe 1](https://github.com/hypergeek-dev/Quickfire_bulletin1/blob/main/static/images/Wireframe1.png)
![Wireframe 2](https://github.com/hypergeek-dev/Quickfire_bulletin1/blob/main/static/images/Wireframe2.png)
![Wireframe 3](https://github.com/hypergeek-dev/Quickfire_bulletin1/blob/main/static/images/Wireframe3.png)

These wireframes provide a visual representation of the app's layout and design during the planning phase.

## Lighthouse
![Lighthouse](https://github.com/hypergeek-dev/Quickfire_bulletin1/blob/main/static/images/lighthouse.png)

## 

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
