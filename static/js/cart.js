document.addEventListener('DOMContentLoaded', function () {
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');

    addToCartButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();

            const itemId = this.getAttribute('data-item-id');

            fetch('/ajax/add-to-cart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCSRFToken(),
                },
                body: new URLSearchParams({
                    'item_id': itemId
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Update cart number without page reload
                    document.getElementById('cart-count').textContent = data.total_items;
                } else {
                    alert(data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // Helper function to get CSRF token
    function getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }
})