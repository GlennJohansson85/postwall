// Displays Post titles based on user input and redirects to choosen post/ search results page
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input'); // Get the search input element
    const suggestionsDiv = document.querySelector('.suggestions'); // Get the suggestions container

    if (searchInput) {

        // Add an event listener for input changes
        searchInput.addEventListener('input', function () {
            const searchValue = this.value; // Get the input value

            if (searchValue) {

                // Fetch search suggestions
                fetch(`/search/suggestions/?keyword=${encodeURIComponent(searchValue)}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok'); // Handle network errors
                        }
                        return response.json(); // Parse the JSON response
                    })
                    .then(data => {
                        suggestionsDiv.innerHTML = ''; // Clear previous suggestions

                        // If there are suggestions, create suggestion elements
                        if (data.suggestions.length > 0) {
                            data.suggestions.forEach(suggestion => {
                                const suggestionItem = document.createElement('div'); // New div for each suggestion
                                suggestionItem.className = 'suggestion'; // Assign the suggestion class

                                // Set the inner HTML with a link to the post
                                suggestionItem.innerHTML = `<a href="/post/${suggestion.id}">${suggestion.title}</a>`;

                                // Append the suggestion to the suggestions container
                                suggestionsDiv.appendChild(suggestionItem);
                            });
                            suggestionsDiv.style.display = 'block'; // Show suggestions
                        } else {
                            suggestionsDiv.style.display = 'none'; // Hide when no suggestions
                        }
                    })

                    // Log any fetch errors
                    .catch(error => {
                        console.error('There was a problem with the fetch operation:', error);
                    });
            } else {

                // Clear suggestions when input is empty
                suggestionsDiv.innerHTML = '';
                suggestionsDiv.style.display = 'none'; // Hide suggestions
            }
        });

        // Handle clicks on suggestion items
        suggestionsDiv.addEventListener('click', function (event) {
            if (event.target.closest('.suggestion')) { // Check if a suggestion was clicked
                const title = event.target.innerText; // Get the title of the clicked suggestion
                searchInput.value = title; // Set the search input value to the suggestion title
                suggestionsDiv.innerHTML = ''; // Clear suggestions
                suggestionsDiv.style.display = 'none'; // Hide suggestions
                const postLink = event.target.closest('a').href; // Get the link to the post
                window.location.href = postLink; // Redirect to the selected post
            }
        });
    }
});

