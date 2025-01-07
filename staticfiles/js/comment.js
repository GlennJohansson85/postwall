function submitCommentForm(event, postId) {
    event.preventDefault();
    const form = document.getElementById("comment" + postId);
    const formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Comment submission response:', data);  // Log response to check success

        if (data.success) {
            // After successful comment submission, scroll to the post
            console.log('Comment added successfully, scrolling to post');
            scrollToPost(postId);
        } else {
            console.error('Failed to add comment');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
