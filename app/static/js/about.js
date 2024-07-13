document.addEventListener('DOMContentLoaded', function() {
    function updateAboutPage() {
        document.getElementById('browserInfo').textContent = navigator.userAgent;
    }
    updateAboutPage(); // Call the function to update browser info
});