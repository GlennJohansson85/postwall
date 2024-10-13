function handleKeyPress(event, postId) {

    // Check if the key pressed is the 'Enter' key
    if (event.key === 'Enter') {

        // Prevent the default action of the Enter key (e.g., adding a new line in the textarea)
        event.preventDefault();

        // Get the form element corresponding to the post by constructing its ID
        const form = document.getElementById('comment-form-' + postId);

        // Submit the form
        form.submit();
    }
}