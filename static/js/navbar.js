// Handle navbar-brand
document.addEventListener('DOMContentLoaded', function () {
    const currentPath = window.location.pathname;
    console.log('Current Path:', currentPath);
    
    // Handle navbar-brand (Post Wall)
    const navbarBrand = document.querySelector('.navbar-brand');
    if (navbarBrand) {
        const brandHref = navbarBrand.getAttribute('href');
        console.log('Navbar Brand Href:', brandHref);
        if (brandHref === currentPath || brandHref + '/' === currentPath) {
            navbarBrand.classList.add('active');
        } else {
            navbarBrand.classList.remove('active');
        }
    }

    // Handle nav-links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        const linkHref = link.getAttribute('href');
        console.log('Nav Link Href:', linkHref);
        if (linkHref === currentPath || linkHref + '/' === currentPath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
});

