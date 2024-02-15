# Quickfire Bulletin Documentation

## Table of Contents

## Introduction
![amiresponsive](/static/images/amiresponsive.png)

Quickfire Bulletin is a Django-based web application designed to revolutionize the way users engage with news bulletins. Unlike traditional platforms, it uniquely integrates real-time news fetching from the source, converts it into neat and readable articles without no to little need of editing. Users have the oppertunity to comment on articles
and the design is responsive on all devices. 

[Live Demo](https://quickfirebulletin-9159c210d03e.herokuapp.com)


## Features

- **News API Integration**: The application fetches news articles from the NewsData.io API and populates the database with the latest news.
- **User Authentication**: Users can register, log in, and log out.
- **Admin Dashboard**: Admin users have the ability to edit or delete news articles.
- **Commenting**: Users can comment on news articles.
- **Pagination**: The home page displays news articles in a paginated format.


# User Stories

## Admin Stories

- **As an admin, I can log in and access the admin panel.** This allows me to manage the platform efficiently.

- **As an admin, I can create, edit, and delete articles.** This enables me to keep the content on the platform up-to-date and relevant.

- **As an admin, I can moderate comments on articles.** This helps in maintaining a respectful and constructive discussion environment on the platform.

## Registered User Stories

- **As a registered user, I can comment on news articles.** This enables me to participate in discussions and share my thoughts on news articles after logging in.

## Visitor Stories (Not Registered)

- **As a visitor, I can view the latest news articles.** This allows me to stay informed about the latest news and events without needing to register or log in.

This process is also described

## Technical Stack

- **Backend**: Python, Django
- **Frontend**: HTML, CSS, Javascript.
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
    source venv/bin/activate  
    # or
    .\\venv\\Scripts\\Activate  
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

#### Development
I planned from the beginning for a simplistic design, aiming for high accessibility and at the same time minimal use of ressources.

![Wireframe 1](/static/images/Wireframe1.png)

<p float="left">
  <img src="/static/images/Wireframe2.png" alt="Wireframe 2" width="400" />
  <img src="/static/images/Wireframe3.png" alt="Wireframe 3" width="400" />
</p>

As part of my development process, I've identified and prioritized features and tasks using the MoSCoW method (Must have, Should have, Could have, Won't have this time). For a more detailed breakdown and elaboration of these priorities and how they align with my project goals, please refer to my detailed planning document available here: [Detailed Project Planning and Prioritization](https://docs.google.com/spreadsheets/d/e/2PACX-1vSc2WF7hxm_uG6K457U6--8xUPsG_PwHrYmqWHSsuqquLTdcb1B4_4z4T3kIlQv10pu5oYnb2gAz86V/pubhtml).

### Development Challenges

- **API Integration**: Integrating NewsData.io API to fetch and display news articles.
First I had to fetch the response from the API. The response was then formed as a Json which I in turn had to convert to readable article. I implemented Spacy and NLP to segment the text into phrases and I then divided out the amount of phrases in paragraphs. 


- **Form Validation Issues**: Initially, the comment form was submitting even when some fields were left empty. Implementing client-side validation using JavaScript ensured all required information was provided before submission.

- **Missing Fields in Form**: After adding "Name" and "Email" fields, the form data sent to the server did not include this information. Adjusting the JavaScript code handling form submission to include these values solved the issue.

##### Validation

Note: I noticed Djangos built in authentication causes validation errors. I chose not to solve this issue, waiting for future updates to the authentication module. 

All pages except before mentioned, has been validated in a HTML validator. Using the rendered result. 
CSS has been validated.
<p>
    <a href="http://jigsaw.w3.org/css-validator/check/referer">
        <img style="border:0;width:88px;height:31px"
            src="http://jigsaw.w3.org/css-validator/images/vcss"
            alt="Valid CSS!" />
    </a>
</p>

All python code has been based on PEP8 standards and explanatory docstrings implemented.

I have used JShint to validate my javascript implemented for handling user feedback when commenting.
The results shows that the variables showEditForm and hideEditForm are not in use.
My conclusion is that through observation they are functioning and in use, so it must be a false positive. 

# Testing

##Lighthouse

![Lighthouse](/static/images/lighthouse.png)

Because of the simplistic design without the need of images. I was able to achieve a high evaluation in lighthouse

At [Website Page Size Checker Output](https://www.toolscrowd.com/website-page-size-checker/)
I checked the size of the initial load.

![Filezise](/static/images/filesize.png)

## Manual testing of the UI

### From an *admins perspective*, I have tested the following

Expected outcome: 

#### Full access to admin panel
I was able to access the admin panel

### Full managability on articles
I was able to add, edit and delete articles.

### Full managability on comments
I was able to add, edit and delete comments.

### Full managability on users

I was able to add, edit and delete users.
<hr>

### From an *authenticated users* perspective:

Expected outcome

### Access to content
I was able to read articles and comments readily accessible on the website

### Full managability on own comments
I was able to read, edit and delete own comments

## Manual Testing of the javafunctions

### From an *authenticated user's perspective*:

#### Adding Comments
- **When adding comments**: I was able to fill out and submit the feedback form without page reload. The AJAX request correctly targeted the `/comments/add_comment/` endpoint when an article ID was present, and feedback was immediately visible on the page after a successful submission.

#### Editing Comments
- **When editing comments**: By clicking the edit button next to a comment, the form for editing was displayed, and the submission was processed without reloading the page. The AJAX request was sent to `/comments/edit_comment/[commentId]/`, and the edited content was correctly updated on the page.

#### Deleting Comments
- **When deleting comments**: The delete button next to each comment triggered an AJAX call to `/comments/delete_comment/[commentId]/` without reloading the page. Upon successful deletion, the comment was removed from the display, confirming the operation's success.

Each action was followed by appropriate user feedback through alerts, indicating success or error messages based on the operation outcome. The CSRF token handling ensured secure post requests, and the dynamic response to AJAX calls facilitated a smooth, interruption-free user experience.


## Automated testing
### How to Run Tests:

1. To run automatic tests for rendering articles functionality:

Run the following command:
 ```bash
python manage.py test qfb_main
```

This test does the following:
- `test_make_api_call_success`: Tests that the `make_api_call` function successfully makes an API call and returns a 200 status code with expected JSON response.
- `test_group_into_paragraphs`: Validates that the `group_into_paragraphs` function correctly groups a list of sentences into paragraphs of a specified length.
- `test_news_article_list_view`: Ensures the home page (`news_article_list` view) correctly displays an article titled "Test Article" when it has a status that matches the view's filtering criteria.

In running this test I received one fail and I resolved it by changing the expected status of the article to "Published" by adding a value of 1.

2. To run automatic tests for commenting functionality:
Run the following command:
 ```bash
python manage.py test comments
```
- `test_valid_form_data`: Confirms that submitting valid form data to the `add_comment_to_article` endpoint returns a 200 status code, indicating success, and verifies the response content to ensure the comment was added successfully. The test checks for a `success` flag in the response and a valid `comment_id`.

- `test_authenticated_user`: Verifies that an authenticated user can post a comment and that the comment is correctly associated with the user. It checks if the comment's user, name, and email fields match the logged-in user's details.

- `test_invalid_http_method`: Ensures that using an invalid HTTP method (GET instead of POST) to the `add_comment_to_article` endpoint results in a 405 status code, indicating that the method is not allowed.

- `test_article_not_found`: Tests the scenario where the specified article ID does not exist. It confirms that attempting to add a comment to a non-existent article returns a 404 status code, indicating that the article was not found.

- `test_error_saving_comment`: Simulates an error during the comment saving process by mocking the `Comment.save` method to throw an exception. It verifies that the server responds with a 500 status code, indicating an internal server error.

- `test_associate_comment_with_article`: Checks that a comment is correctly associated with the intended article. It posts valid form data and verifies that the comment's `news_article` field matches the article used in the setup.

3.  To run automatic tests for feedback functionality:
Run the following command:
 ```bash
python manage.py test feedback
```
- `test_feedback_view_get_request`: Verifies that the `feedback_view` correctly renders the expected template and form upon a GET request, ensuring the user interface meets design specifications.

- `test_feedback_view_post_request_invalid`: Tests the `feedback_view`'s handling of invalid form submissions, expecting it to return specific form errors and validate input data integrity, ensuring robust error handling and user feedback mechanisms.

# Contribution

# License

Quickfire Bulletin is licensed under the MIT License. This permits personal and commercial use, modification, distribution, and private use. [More about the MIT License](https://opensource.org/licenses/MIT).
