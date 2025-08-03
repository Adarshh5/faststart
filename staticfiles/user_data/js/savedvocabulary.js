document.addEventListener('DOMContentLoaded', function() {
    // Delete word functionality
    document.querySelectorAll('.btn-delete').forEach(button => {
        button.addEventListener('click', function() {
            const vocabItem = this.closest('.vocab-item');
            const word = vocabItem.dataset.word;
            
            if (confirm(`Are you sure you want to delete "${word}"?`)) {
                deleteWord(word, vocabItem);
            }
        });
    });
    
    // View details functionality
    document.querySelectorAll('.btn-detail').forEach(button => {
        button.addEventListener('click', function() {
            const word = this.closest('.vocab-item').dataset.word;
            viewWordDetails(word);
        });
    });
    
    // Delete word via AJAX
    function deleteWord(word, element) {
        fetch("/userdata/removesavedvocabulary/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ word: word })
        })
        .then(response => response.json())
        .then(data => {
            if (data.reply === "Removed") {
                // Remove from UI
                element.remove();
                
                // Update word count
                const totalEl = document.getElementById('totalWords');
                totalEl.textContent = parseInt(totalEl.textContent) - 1;
                
                // Renumber items
                renumberItems();
            } else {
                alert('Error: ' + data.reply);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while deleting the word.');
        });
    }
    
    // View word details
    function viewWordDetails(word) {
        fetch("/userdata/savedworddetail/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ word: word })
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            } else {
                return response.json();
            }
        })
        .then(data => {
            if (data && data.error) {
                alert(data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while loading word details.');
        });
    }
    
    // Renumber items after deletion
    function renumberItems() {
        document.querySelectorAll('.vocab-item').forEach((item, index) => {
            item.querySelector('.item-number').textContent = `${index + 1}.`;
        });
    }
    
    // Get CSRF token
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }
});