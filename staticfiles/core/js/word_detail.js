document.addEventListener('DOMContentLoaded', function() {
    const saveWordBtn = document.getElementById('saveWordBtn');
    
    if (saveWordBtn) {
        saveWordBtn.addEventListener('click', function() {
            const word = this.getAttribute('data-word');
            // const isSaved = this.innerHTML.includes('fa-bookmark'); // Check if already saved
            let isSaved = this.getAttribute('data-saved') === 'true';
            
            // Get CSRF token from cookies
            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = cookies[i].trim();
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            const csrftoken = getCookie('csrftoken');
            
            // Show loading state
            const originalHTML = saveWordBtn.innerHTML;
            saveWordBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing';
            saveWordBtn.disabled = true;
            
            // Send AJAX request
            fetch('/userdata/toggle_save_word/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ word: word })
            })
            .then(response => response.json())
           
            .then(data => {
                if (data.reply === "added") {
                    saveWordBtn.innerHTML = '<i class="fas fa-bookmark"></i> Saved';
                    saveWordBtn.setAttribute('data-saved', 'true');
                    showAlert('Word added to your vocabulary!', 'success');
                } else if (data.reply === "already_saved") {
                    saveWordBtn.innerHTML = '<i class="fas fa-bookmark"></i> Saved';
                    saveWordBtn.setAttribute('data-saved', 'true');
                    showAlert('This word is already in your vocabulary.', 'info');
                } else {
                    // Unrecognized or error response
                    showAlert(data.reply || 'An error occurred', 'error');
                    saveWordBtn.innerHTML = originalHTML;
                }
            })


            .catch(error => {
                showAlert('Network error. Please try again.', 'error');
                saveWordBtn.innerHTML = originalHTML;
            })
            .finally(() => {
                saveWordBtn.disabled = false;
            });
        });
    }
    
    // Function to show alerts
    function showAlert(message, type) {
        // Remove any existing alerts
        const existingAlert = document.querySelector('.custom-alert');
        if (existingAlert) existingAlert.remove();
        
        // Create alert element
        const alertEl = document.createElement('div');
        alertEl.className = `custom-alert alert-${type}`;
        alertEl.textContent = message;
        document.body.appendChild(alertEl);
        
        // Position alert
        const headerHeight = document.querySelector('header').offsetHeight;
        alertEl.style.top = `${headerHeight + 20}px`;
        
        // Remove alert after 3 seconds
        setTimeout(() => {
            alertEl.style.opacity = '0';
            setTimeout(() => {
                if (alertEl.parentNode) alertEl.parentNode.removeChild(alertEl);
            }, 300);
        }, 3000);
    }
});




