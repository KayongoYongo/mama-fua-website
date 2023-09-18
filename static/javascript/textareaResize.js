// textareaResize.js
document.addEventListener('DOMContentLoaded', function () {
    const textarea = document.getElementById('message');

    textarea.addEventListener('input', function () {
        this.style.height = 'auto';
        this.style.height = `${this.scrollHeight}px`;
    });
});