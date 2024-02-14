# Quickfire Bulletin Documentation

## Table of Contents

## Introduction

Quickfire Bulletin is a cutting-edge Django-based web application designed to revolutionize the way users engage with news bulletins. Unlike traditional platforms, it uniquely integrates real-time news fetching with interactive user features like commenting and liking, fostering a dynamic community of informed individuals. What sets Quickfire Bulletin apart is its commitment to [unique selling points or features], designed with a focus on modularity, extensibility, and a seamless user experience.

[Live Demo](https://quickfirebulletin-9159c210d03e.herokuapp.com)


[The site is live here](https://quickfire-bulletin-1054d3494a4d.herokuapp.com/)

## Features

- **News API Integration**: The application fetches news articles from the NewsData.io API and populates the database with the latest news.
- **User Authentication**: Users can register, log in, and log out.
- **Admin Dashboard**: Admin users have the ability to edit or delete news articles.
- **Commenting**: Users can comment on news articles.
- **Pagination**: The home page displays news articles in a paginated format.

## User Stories

### Admin Stories

As an admin, I can:
- Log in and access the admin panel.
- Create, edit, and delete articles
- Create, edit, and delete comments
- Manage user accounts.

### Visitor Stories

As a visitor, I can:
- Register an account or log in.
- View the latest newsarticles.
- Comment on newsarticles.

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

## Testing

### How to Run Tests:

1. For main app function of rendering newsarticles:

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

Run the following command:
 ```bash
python manage.py test comments
```
This test does the following:
test_feedback_view_get_request: Verifies the feedback view renders the correct template and form on a GET request.
test_feedback_view_post_request_invalid: Tests handling of invalid form data submission in the feedback view, expecting specific form errors.




## Contributing

## License

Quickfire Bulletin is licensed under the MIT License. This permits personal and commercial use, modification, distribution, and private use. [More about the MIT License](https://opensource.org/licenses/MIT).
