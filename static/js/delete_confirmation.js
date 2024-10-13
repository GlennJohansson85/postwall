// Confirmation container when a user/admin deletes a post
function showDeleteConfirmation() {
    document.getElementById("delete-confirmation-container").style.display = "block";
}

// Hides the confirmation container when the user/admin cancels the deletion
function hideDeleteConfirmation() {
    document.getElementById("delete-confirmation-container").style.display = "none";
}
