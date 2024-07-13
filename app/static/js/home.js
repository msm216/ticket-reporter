document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('add-paragraph-btn').addEventListener('click', function() {
        const paragraphContainer = document.getElementById('paragraph-container');
        const newParagraph = document.createElement('p');
        newParagraph.textContent = Array(1000).fill(null).map(() => Math.random().toString(36).charAt(2)).join('');
        paragraphContainer.appendChild(newParagraph);
    });
});