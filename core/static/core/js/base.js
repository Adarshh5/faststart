document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu auto-close
    const navbarCollapse = document.getElementById('navbarNav');
    const bsCollapse = new bootstrap.Collapse(navbarCollapse, {toggle: false});
    
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            if(window.innerWidth < 768) {
                bsCollapse.hide();
            }
        });
    });
});