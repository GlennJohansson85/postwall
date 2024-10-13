// Alert Messages which fades out
document.addEventListener("DOMContentLoaded", function() {

    // Select all elements with the class 'alert'
    var alertMessages = document.querySelectorAll('.alert');

    // Loop through each alert message
    alertMessages.forEach(function(alertMessage) {

        // Timeout to start the fade-out process after 3 seconds
        setTimeout(function() {
            alertMessage.classList.add('fade-out'); // Class to initiate fade-out

            // Listen for the end of the effect
            alertMessage.addEventListener('transitionend', function() {
                alertMessage.remove(); // Remove alert message from the DOM after fade-out
            });
        }, 3000); // Delay before fade-out starts
    });
});
