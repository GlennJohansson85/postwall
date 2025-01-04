// Function to handle key press (Enter key) and submit the comment
function handleKeyPress(event, postId) {
    if (event.key === 'Enter') {
        event.preventDefault();

        // Add the post_id to the URL before form submission
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set('post_id', postId); // Add the post_id query parameter
        window.history.pushState({}, '', currentUrl); // Update the URL in the address bar

        // Submit the form after updating the URL
        const form = document.getElementById('comment-form-' + postId);
        form.submit();
    }
}

// Function to scroll to the specific post after page load
function scrollToPost() {
    // Get the current URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const postId = urlParams.get('post_id'); // Extract the 'post_id' from the URL

    if (postId) {
        // Find the post element with the corresponding data-post-id
        const postElement = document.querySelector(`.concrete[data-post-id="${postId}"]`);

        if (postElement) {
            // Scroll to the specific post element
            postElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }
}

// Run the scroll function when the page loads (use window.onload to ensure it's fully loaded)
window.onload = function() {
    scrollToPost();
};
