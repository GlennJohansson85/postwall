// User can filter through, select one and be redirected to the details of the post, or
// be redirected to a search results page where all suggestions are presented -
// if the user does not choose a specific title.

document.addEventListener('DOMContentLoaded', () => {
    const searchButton = document.getElementById('btn-search'); // Get the search button element
    const searchInput = document.querySelector('.search-input'); // Get the search input field
    const suggestionsContainer = document.querySelector('.suggestions'); // Get the suggestions container

    suggestionsContainer.style.display = 'none'; // Hide the suggestions container on page load

    // Create an array of posts with titles and IDs from the DOM elements
    const posts = Array.from(document.querySelectorAll('.concrete')).map(postElement => {
        const titleElement = postElement.querySelector('.postwall-title'); // Get the title element
        const postId = postElement.getAttribute('data-post-id'); // Get the post ID from a data attribute
        return {
            title: titleElement.textContent.toLowerCase(), // Store title in lowercase
            id: postId // Store post ID
        };
    });

    // Add click event listener to the search button
    searchButton.addEventListener('click', () => {
        const query = searchInput.value.toLowerCase(); // Get the search input value
        showSuggestions(query); // Show suggestions based on the query
    });

    // Add input event listener to the search input field
    searchInput.addEventListener('input', () => {
        const query = searchInput.value.toLowerCase(); // Get the search input value
        showSuggestions(query); // Show suggestions based on the query
    });

    // Function to show suggestions based on the user's input
    function showSuggestions(query) {
        suggestionsContainer.innerHTML = ''; // Clear previous suggestions

        // Filter posts that include the search query and are not empty
        const filteredPosts = posts.filter(post => post.title.includes(query) && query !== '');

        if (filteredPosts.length === 0) {
            suggestionsContainer.style.display = 'none'; // Hide if no suggestions
        } else {
            suggestionsContainer.style.display = 'block'; // Show when suggestions exist

            // Create suggestion items for each filtered post
            filteredPosts.forEach(post => {
                const suggestionItem = document.createElement('div'); // Create a new div for the suggestion
                suggestionItem.className = 'suggestion-item'; // Set the class for styling
                suggestionItem.textContent = post.title; // Set the text to the post title

                // Add click event listener to redirect on suggestion click
                suggestionItem.addEventListener('click', () => {
                    window.location.href = `/post/${post.id}/`; // Redirect to the post page
                    suggestionsContainer.innerHTML = ''; // Clear suggestions after selection
                });

                suggestionsContainer.appendChild(suggestionItem); // Add suggestion item to the container
            });
        }
    }
});
