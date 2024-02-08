document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".user-feedback").forEach((form) => {
        form.addEventListener("submit", function (event) {
            event.preventDefault();
            const formData = new FormData(this);
            const commentId = formData.get("comment_id") || null;
            const articleId = formData.get("article_id") || null;
            const url = commentId ? `/comments/edit_comment/${commentId}/` : (articleId ? `/comments/add_comment/${articleId}/` : "/comments/add_comment/");
            sendAjaxRequest(url, formData);
        });
    });

    document.querySelectorAll(".delete-comment-btn").forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const commentId = this.getAttribute('data-comment-id');
            const url = `/comments/delete_comment/${commentId}/`;
            sendAjaxRequest(url, new FormData());
        });
    });
});

function sendAjaxRequest(url, formData) {
    const csrftoken = getCookie("csrftoken");
    const headers = {
        'X-CSRFToken': csrftoken,
    };
    const options = {
        method: "POST",
        headers: headers,
    };
    if (formData) {
        options.body = formData;
    }

    fetch(url, options)
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((data) => {
            if (data.success) {
                alert(data.message || "Operation successful.");
                window.location.reload(); 
            } else {
              
                alert("Error: " + (data.error || "An unexpected error occurred."));
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("Error: " + error.message);
        });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showEditForm(commentId) {
    document.getElementById('edit-form-' + commentId).style.display = 'block';
    document.getElementById('comment-content-' + commentId).style.display = 'none';
}

function hideEditForm(commentId) {
    document.getElementById('edit-form-' + commentId).style.display = 'none';
    document.getElementById('comment-content-' + commentId).style.display = 'block';
}
