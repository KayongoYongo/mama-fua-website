// JavaScript to hide the flash message after 5 seconds
setTimeout(function() {
    var flashMessage = document.getElementById('flash-message');
    if (flashMessage) {
        flashMessage.style.display = 'none';
    }
}, 5000); // 5000 milliseconds = 5 seconds