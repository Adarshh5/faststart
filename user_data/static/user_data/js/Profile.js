document.addEventListener('DOMContentLoaded', function() {
  // Highlight active navigation links
  const navLinks = document.querySelectorAll('.nav-link');
  
  navLinks.forEach(link => {
    link.addEventListener('click', function() {
      // Remove active class from all links
      navLinks.forEach(l => l.classList.remove('active'));
      
      // Add active class to clicked link
      this.classList.add('active');
      
      // Close mobile sidebar if open
      const mobileSidebar = bootstrap.Offcanvas.getInstance(document.getElementById('mobileSidebar'));
      if (mobileSidebar) {
        mobileSidebar.hide();
      }
    });
  });
  
  // Set first link as active by default
  if (navLinks.length > 0) {
    navLinks[0].classList.add('active');
  }
  
  // Initialize Bootstrap offcanvas
  const mobileSidebar = new bootstrap.Offcanvas('#mobileSidebar');
});