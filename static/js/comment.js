function handleKeyPress(event, postId) {
    if (event.key === 'Enter') {
        event.preventDefault();

        const form = document.getElementById('comment-form-' + postId);

        // Submit the form
        form.submit();
    }
}