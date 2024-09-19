document.addEventListener("DOMContentLoaded", function() {
    var alertMessages = document.querySelectorAll('.alert');

    alertMessages.forEach(function(alertMessage) {
        setTimeout(function() {
            alertMessage.classList.add('fade-out');
            alertMessage.addEventListener('transitionend', function() {
                alertMessage.remove();
            });
        }, 5000); // Adjust the timeout as needed (in milliseconds)
    });
});
