document.addEventListener('DOMContentLoaded', function() {
    const paragraphContainer = document.getElementById('paragraph-container');
    const addParagraphBtn = document.getElementById('add-paragraph-btn');
    const exampleRange = document.getElementById('exampleRange');
    const rangeValue = document.getElementById('rangeValue');

    // Initialize the range value display
    rangeValue.textContent = exampleRange.value;

    addParagraphBtn.addEventListener('click', function() {
        const newParagraph = document.createElement('p');
        newParagraph.textContent = Array(500).fill(null).map(() => Math.random().toString(36).charAt(2)).join('');
        newParagraph.style.fontSize = `${exampleRange.value}px`;
        paragraphContainer.appendChild(newParagraph);
    });

    exampleRange.addEventListener('input', function() {
        const paragraphs = paragraphContainer.getElementsByTagName('p');
        for (let p of paragraphs) {
            p.style.fontSize = `${exampleRange.value}px`;
        }
        rangeValue.textContent = exampleRange.value; // Update the range value display
    });
});