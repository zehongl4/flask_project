// blog-interactions.js - JavaScript for blog interactions
// This file handles AJAX functionality for likes, bookmarks and comments

// blog-interactions.js - JavaScript for blog interactions
// This file handles AJAX functionality for likes, bookmarks and comments

document.addEventListener('DOMContentLoaded', function() {
    console.log("Document loaded, initializing interactions...");
    
    // Debug info
    console.log("Found like form:", !!document.querySelector('.like-form'));
    console.log("Found bookmark form:", !!document.querySelector('.bookmark-form'));
    console.log("Found comment form:", !!document.querySelector('.comment-form form'));
    
    // 读取并保存初始状态
    const likeBtn = document.getElementById('likeBtn');
    const initialLikeState = likeBtn ? likeBtn.classList.contains('liked') : false;
    
    const bookmarkBtn = document.getElementById('bookmarkBtn');
    const initialBookmarkState = bookmarkBtn ? bookmarkBtn.classList.contains('bookmarked') : false;
    
    console.log("Initial like state:", initialLikeState);
    console.log("Initial bookmark state:", initialBookmarkState);
    
    // 确保状态被保留，通过明确地添加类
    if (initialLikeState && likeBtn) {
        likeBtn.classList.add('liked');
    }
    
    if (initialBookmarkState && bookmarkBtn) {
        bookmarkBtn.classList.add('bookmarked');
    }
    
    // Initialize like buttons
    initializeLikes();
    
    // Initialize bookmark buttons
    initializeBookmarks();
    
    // Initialize comment form
    initializeCommentForm();
});

/**
 * Initialize like functionality with AJAX
 */
function initializeLikes() {
    const likeForm = document.querySelector('.like-form');
    if (!likeForm) return;
    
    // 确保初始状态被保留
    const likeBtn = document.getElementById('likeBtn');
    if (likeBtn && likeBtn.classList.contains('liked')) {
        console.log("Initial state: post is liked");
    }
    
    likeForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // query right URL using data-api-url
        const apiUrl = this.getAttribute('data-api-url');
        const likeBtn = document.getElementById('likeBtn');
        const likeCountElem = document.querySelector('#likeBtn span');
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        
        // print URL
        console.log("Submitting like to URL:", apiUrl);
        
        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({})
        })
        .then(response => {
            console.log("Response status:", response.status);
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Response data:", data);
            if (data.status === 'success') {
                // Update like count
                likeCountElem.textContent = data.like_count;
                
                // Update button state
                if (data.is_liked) {
                    likeBtn.classList.add('liked');
                } else {
                    likeBtn.classList.remove('liked');
                }
                
                // Show a brief message
                showNotification(data.is_liked ? 'Post liked' : 'Post unliked');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('There was an error processing your request', 'error');
        });
    });
}

/**
 * Initialize bookmark functionality with AJAX
 */
function initializeBookmarks() {
    const bookmarkForm = document.querySelector('.bookmark-form');
    if (!bookmarkForm) return;
    
    // 确保初始状态被保留
    const bookmarkBtn = document.getElementById('bookmarkBtn');
    if (bookmarkBtn && bookmarkBtn.classList.contains('bookmarked')) {
        console.log("Initial state: post is bookmarked");
    }
    
    bookmarkForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // query right URL using data-api-url
        const apiUrl = this.getAttribute('data-api-url');
        const bookmarkBtn = document.getElementById('bookmarkBtn');
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        
        // print URL
        console.log("Submitting bookmark to URL:", apiUrl);
        
        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({})
        })
        .then(response => {
            console.log("Response status:", response.status);
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Response data:", data);
            if (data.status === 'success') {
                // Update button state
                if (data.is_bookmarked) {
                    bookmarkBtn.classList.add('bookmarked');
                    showNotification('Post added to bookmarks');
                } else {
                    bookmarkBtn.classList.remove('bookmarked');
                    showNotification('Post removed from bookmarks');
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('There was an error processing your request', 'error');
        });
    });
}

/**
 * Initialize comment form with AJAX submission
 */
function initializeCommentForm() {
    const commentForm = document.querySelector('.comment-form form');
    if (!commentForm) return;
    
    console.log("Comment form action:", commentForm.action);
    console.log("Comment form data-api-url:", commentForm.getAttribute('data-api-url'));
    
    commentForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // query right URL using data-api-url
        const apiUrl = this.getAttribute('data-api-url') || this.action;
        const commentInput = this.querySelector('textarea[name="content"]');
        const content = commentInput.value.trim();
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        
        // print URL
        console.log("Submitting comment to URL:", apiUrl);
        
        if (!content) {
            showNotification('Comment cannot be empty', 'error');
            return;
        }
        
        // create FormData object
        const formData = new FormData(this);
        
        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
                
            },
            body: JSON.stringify({ content: content })
        })
        .then(response => {
            console.log("Response status:", response.status);
            console.log("Response headers:", response.headers);
            
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.status}`);
            }
            
            // check JSON
            const contentType = response.headers.get("content-type");
            if (contentType && contentType.indexOf("application/json") !== -1) {
                return response.json();
            } else {
               
                console.log("Non-JSON response received");

                window.location.reload();
                return { status: 'reload' };
            }
        })
        .then(data => {
            console.log("Response data:", data);
            

            if (data.status === 'reload') return;
            
            if (data.status === 'success') {
                // Clear the input
                commentInput.value = '';
                
                // Add the new comment to the list
                addCommentToList(data.comment);
                
                // Update comment count
                updateCommentCount(1);
                
                // Show success message
                showNotification('Comment posted successfully');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('There was an error posting your comment', 'error');
        });
    });
    
    // Initialize comment delete buttons
    initializeCommentDeleteButtons();
}

/**
 * Initialize comment delete buttons with AJAX
 */
function initializeCommentDeleteButtons() {
    document.querySelectorAll('.comment-action-delete').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            
            if (!confirm('Are you sure you want to delete this comment?')) {
                return;
            }
            
            // query right URL using data-api-url
            const apiUrl = this.getAttribute('data-api-url');
            const commentId = this.getAttribute('data-comment-id');
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            
            // print URL
            console.log("Deleting comment at URL:", apiUrl);
            
            // create FormData object
            const formData = new FormData();
            formData.append('csrf_token', csrfToken);
            
            fetch(apiUrl, {
                method: 'POST',  
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData
            })
            .then(response => {
                console.log("Response status:", response.status);
                
                if (!response.ok) {
                    throw new Error(`Network response was not ok: ${response.status}`);
                }
                
                // check JSON
                const contentType = response.headers.get("content-type");
                if (contentType && contentType.indexOf("application/json") !== -1) {
                    return response.json();
                } else {


                    window.location.reload();
                    return { status: 'reload' };
                }
            })
            .then(data => {
                console.log("Response data:", data);
                

                if (data.status === 'reload') return;
                
                if (data.status === 'success') {
                    // Remove the comment from DOM
                    const commentElement = document.querySelector(`.comment[data-comment-id="${commentId}"]`);
                    if (commentElement) {
                        commentElement.remove();
                        
                        // Update comment count
                        updateCommentCount(-1);
                        
                        // Show success message
                        showNotification('Comment deleted');
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('There was an error deleting the comment', 'error');
            });
        });
    });
}

/**
 * Add a new comment to the comment list
 */
function addCommentToList(comment) {
    const commentList = document.querySelector('.comment-list');
    const noCommentsMessage = commentList.querySelector('p');
    
    // Remove "No comments yet" message if it exists
    if (noCommentsMessage && noCommentsMessage.textContent === 'No comments yet') {
        noCommentsMessage.remove();
    }
    

    const deleteUrlTemplate = document.querySelector('.comment-form form').getAttribute('data-delete-url-template');
    console.log("Delete URL template:", deleteUrlTemplate);
    

    let deleteUrl = deleteUrlTemplate;
    if (deleteUrlTemplate) {
        deleteUrl = deleteUrlTemplate.replace('0', comment.id);
    }
    console.log("Generated delete URL:", deleteUrl);
    
    // Create new comment element
    const commentElement = document.createElement('div');
    commentElement.className = 'comment';
    commentElement.setAttribute('data-comment-id', comment.id);
    
    // Format the HTML for the new comment
    commentElement.innerHTML = `
        <div class="comment-header">
            <span class="comment-author">${comment.username}</span>
            <span class="comment-date">${comment.created_at}</span>
        </div>
        <div class="comment-content">${comment.content}</div>
        <div class="comment-actions">
            <a href="#" class="comment-action comment-action-delete" 
               data-comment-id="${comment.id}"
               data-api-url="${deleteUrl}">Delete</a>
            <a href="#commentSection" 
               class="comment-action" 
               onclick="document.querySelector('.comment-input').value = '@${comment.username} '; document.querySelector('.comment-input').focus();">
                Reply
            </a>
        </div>
    `;
    
    // Add to the beginning of the list (newest first)
    commentList.insertBefore(commentElement, commentList.firstChild);
    
    // Add event listener to the delete button
    const deleteButton = commentElement.querySelector('.comment-action-delete');
    if (deleteButton) {
        deleteButton.addEventListener('click', function(event) {
            event.preventDefault();
            
            if (!confirm('Are you sure you want to delete this comment?')) {
                return;
            }
            
            const apiUrl = this.getAttribute('data-api-url');
            const commentId = this.getAttribute('data-comment-id');
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            
            // query right URL using data-api-url
            console.log("Deleting comment at URL:", apiUrl);
            
            // create FormData object
            const formData = new FormData();
            formData.append('csrf_token', csrfToken);
            
            fetch(apiUrl, {
                method: 'POST',  
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData
            })
            .then(response => {
                console.log("Response status:", response.status);
                
                if (!response.ok) {
                    throw new Error(`Network response was not ok: ${response.status}`);
                }
                
                // check JSON
                const contentType = response.headers.get("content-type");
                if (contentType && contentType.indexOf("application/json") !== -1) {
                    return response.json();
                } else {
                
                    console.log("Non-JSON response received");
 
                    window.location.reload();
                    return { status: 'reload' };
                }
            })
            .then(data => {
                console.log("Response data:", data);
                

                if (data.status === 'reload') return;
                
                if (data.status === 'success') {
                    commentElement.remove();
                    updateCommentCount(-1);
                    showNotification('Comment deleted');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('There was an error deleting the comment', 'error');
            });
        });
    }
}

/**
 * Update the comment count display
 */
function updateCommentCount(change) {
    const countDisplay = document.querySelector('.interaction-btn[href="#commentSection"] span');
    if (countDisplay) {
        let currentCount = parseInt(countDisplay.textContent);
        countDisplay.textContent = currentCount + change;
        
        // Also update the heading
        const commentsHeading = document.querySelector('.comment-section h3');
        if (commentsHeading) {
            commentsHeading.textContent = `Comments (${currentCount + change})`;
        }
    }
}

/**
 * Show notification message
 */
function showNotification(message, type = 'success') {
    // Check if notification container exists, if not create it
    let notificationContainer = document.getElementById('notification-container');
    
    if (!notificationContainer) {
        notificationContainer = document.createElement('div');
        notificationContainer.id = 'notification-container';
        notificationContainer.style.position = 'fixed';
        notificationContainer.style.top = '20px';
        notificationContainer.style.right = '20px';
        notificationContainer.style.zIndex = '1000';
        document.body.appendChild(notificationContainer);
    }
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.style.padding = '12px 16px';
    notification.style.marginBottom = '10px';
    notification.style.borderRadius = '4px';
    notification.style.boxShadow = '0 2px 4px rgba(0,0,0,0.2)';
    notification.style.transition = 'all 0.3s ease';
    
    if (type === 'success') {
        notification.style.backgroundColor = '#4caf50';
        notification.style.color = 'white';
    } else if (type === 'error') {
        notification.style.backgroundColor = '#f44336';
        notification.style.color = 'white';
    } else {
        notification.style.backgroundColor = '#2196f3';
        notification.style.color = 'white';
    }
    
    notification.textContent = message;
    
    // Add to container
    notificationContainer.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}