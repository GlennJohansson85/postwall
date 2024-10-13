// Allow manipulation of the navbar elements 
document.addEventListener('DOMContentLoaded', function () {

    // Retrieve the current URL path for comparison
    const currentPath = window.location.pathname;
    console.log('Current Path:', currentPath);

    // Navbar Brand 
    const navbarBrand = document.querySelector('.navbar-brand'); // Select the brand
    if (navbarBrand) { // Check if the navbar brand element exist

        // Get the href attribute of the brand
        const brandHref = navbarBrand.getAttribute('href');
        console.log('Navbar Brand Href:', brandHref);

        // If it match, add the 'active' class to highlight the current page
        if (brandHref === currentPath || brandHref + '/' === currentPath) {
            navbarBrand.classList.add('active');
        } else {

            // If not, remove the 'active' class
            navbarBrand.classList.remove('active');
        }
    }

    // Navbar Links
    const navLinks = document.querySelectorAll('.nav-link'); // Select all nav-links
    navLinks.forEach(link => {

        // Get the href attribute of each link
        const linkHref = link.getAttribute('href');
        console.log('Nav Link Href:', linkHref);

        // If it match, add the 'active' class to highlight the current page
        if (linkHref === currentPath || linkHref + '/' === currentPath) {
            link.classList.add('active');
        } else {

            // If not, remove the 'active' class
            link.classList.remove('active');
        }
    });
});

