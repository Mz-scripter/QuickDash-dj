document.addEventListener('DOMContentLoaded', function () {
    const wishlistButtons = document.querySelectorAll('.add-to-wishlist-btn');

    wishlistButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();

            const itemId = this.getAttribute('data-item-id');
            const buttonElement = this;

            fetch('/ajax/add-to-wishlist/', {
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
                if (data.status === 'added') {
                    // ✅ Change button style when item is added
                    buttonElement.innerHTML = `
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="#f00" viewBox="0 0 24 24" stroke="currentColor">
                            <path d="M12.1 21.35c-.33.11-.71.11-1.04 0C7.07 19.75 2 15.42 2 10.34A6.34 6.34 0 016.34 4c2.09 0 4.22 1.03 5.66 2.55C13.44 5.03 15.57 4 17.66 4A6.34 6.34 0 0122 10.34c0 5.08-5.07 9.41-8.94 10.99z"></path>
                        </svg>
                    `;
                    buttonElement.setAttribute('title', 'Remove from Wishlist');
                } else if (data.status === 'removed') {
                    // ✅ Change button style when item is removed
                    buttonElement.innerHTML = `
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M4.318 6.318a4.5 4.5 0 016.364 0L12 7.636l1.318-1.318a4.5 4.5 0 116.364 6.364L12 20.364l-7.682-7.682a4.5 4.5 0 010-6.364z" />
                        </svg>
                    `;
                    buttonElement.setAttribute('title', 'Add to Wishlist');
                } else {
                    alert(data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

    // CSRF token helper
    function getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }
});
