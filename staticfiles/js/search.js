// Displays Post titles based on user input and redirects to choosen post/ search results page
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input');
    const suggestionsDiv = document.querySelector('.suggestions');
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            const searchValue = this.value;
            if (searchValue) {
                // Fetch search suggestions
                fetch(`/search/suggestions/?keyword=${encodeURIComponent(searchValue)}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        suggestionsDiv.innerHTML = '';
                        // If there are suggestions, create suggestion elements
                        if (data.suggestions.length > 0) {
                            data.suggestions.forEach(suggestion => {
                                const suggestionItem = document.createElement('div');
                                suggestionItem.className = 'suggestion';
                                // Set the inner HTML with a link to the post
                                suggestionItem.innerHTML = `<a href="/post/${suggestion.id}">${suggestion.title}</a>`;
                                // Append the suggestion to the suggestions container
                                suggestionsDiv.appendChild(suggestionItem);
                            });
                            suggestionsDiv.style.display = 'block';
                        } else {
                            suggestionsDiv.style.display = 'none';
                        }
                    })
                    // Log any fetch errors
                    .catch(error => {
                        console.error('There was a problem with the fetch operation:', error);
                    });
            } else {
                suggestionsDiv.innerHTML = '';
                suggestionsDiv.style.display = 'none';
            }
        });
        // Handle clicks on suggestion items
        suggestionsDiv.addEventListener('click', function (event) {
            if (event.target.closest('.suggestion')) {
                const title = event.target.innerText;
                searchInput.value = title;
                suggestionsDiv.innerHTML = '';
                suggestionsDiv.style.display = 'none';
                const postLink = event.target.closest('a').href;
                window.location.href = postLink;
            }
        });
    }
});

