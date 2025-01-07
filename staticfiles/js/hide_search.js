document.addEventListener('DOMContentLoaded', () => {
    const searchButton = document.getElementById('btn-search');
    const searchInput = document.querySelector('.search-input');
    const suggestionsContainer = document.querySelector('.suggestions');
    suggestionsContainer.style.display = 'none';
    // Create an array of posts with titles and IDs from the DOM elements
    const posts = Array.from(document.querySelectorAll('.concrete')).map(postElement => {
        const titleElement = postElement.querySelector('.postwall-title');
        const postId = postElement.getAttribute('data-post-id');
        return {
            title: titleElement.textContent.toLowerCase(),
            id: postId
        };
    });
    // Add click event listener to the search button
    searchButton.addEventListener('click', () => {
        const query = searchInput.value.toLowerCase();
        showSuggestions(query);
    });
    // Add input event listener to the search input field
    searchInput.addEventListener('input', () => {
        const query = searchInput.value.toLowerCase();
        showSuggestions(query);
    });
    // Function to show suggestions based on the user's input
    function showSuggestions(query) {
        suggestionsContainer.innerHTML = '';
        // Filter posts that include the search query and are not empty
        const filteredPosts = posts.filter(post => post.title.includes(query) && query !== '');
        if (filteredPosts.length === 0) {
            suggestionsContainer.style.display = 'none';
        } else {
            suggestionsContainer.style.display = 'block';
            // Create suggestion items for each filtered post
            filteredPosts.forEach(post => {
                const suggestionItem = document.createElement('div');
                suggestionItem.className = 'suggestion-item';
                suggestionItem.textContent = post.title;
                // Add click event listener to redirect on suggestion click
                suggestionItem.addEventListener('click', () => {
                    window.location.href = `/post/${post.id}/`;
                    suggestionsContainer.innerHTML = '';
                });
                suggestionsContainer.appendChild(suggestionItem);
            });
        }
    }
});
