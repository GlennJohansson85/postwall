// Function to scroll to the specific post
function scrollToPost() {
    // Get the current URL
    const urlParams = new URLSearchParams(window.location.search);
    const postId = urlParams.get('post_id');

    if (postId) {
        // Find the post with the corresponding data-post-id
        const postElement = document.querySelector(`.concrete[data-post-id="${postId}"]`);

        if (postElement) {
            // Scroll to the specific post element
            postElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }
}

// Run the function when the page loads
document.addEventListener('DOMContentLoaded', scrollToPost);