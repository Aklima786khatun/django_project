// Run after DOM is ready
$(document).ready(function () {

    // 1. Initialize Owl Carousel (The Sliding Images)
    if ($('.owl-1').length > 0) {
        $('.owl-1').owlCarousel({
            items: 1,
            loop: true,
            margin: 0,
            autoplay: true,
            autoplayTimeout: 5000, // 5 seconds per slide
            animateOut: 'fadeOut', // Clean transition
            nav: false,
            dots: true,
            smartSpeed: 1000
        });
    }

    // 2. Navbar shrink on scroll
    const navbar = document.getElementById("mainNav");
    if (navbar) {
        window.addEventListener("scroll", () => {
            if (window.scrollY > 50) {
                navbar.classList.add("navbar-shrink");
                // Optional: makes navbar sticky at the very top
                navbar.style.top = "0"; 
            } else {
                navbar.classList.remove("navbar-shrink");
                // Return to position below the top bars
                navbar.style.top = "75px"; 
            }
        });
    }

    // 3. Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener("click", function (e) {
            const targetId = this.getAttribute("href");
            if (targetId === "#") return; // Skip if it's just a placeholder

            e.preventDefault();
            const target = document.querySelector(targetId);
            if (target) {
                // Adjusting scroll position to account for fixed header height
                const headerOffset = 100;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: "smooth"
                });
            }
        });
    });

    // 4. Close mobile menu after clicking a link
    $('.navbar-nav>li>a').on('click', function(){
        $('.navbar-collapse').collapse('hide');
    });

});