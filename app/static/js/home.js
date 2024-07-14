document.addEventListener('DOMContentLoaded', function() {
    const paragraphContainer = document.getElementById('paragraph-container');
    const addParagraphBtn = document.getElementById('add-paragraph-btn');
    const exampleRange = document.getElementById('exampleRange');
    const rangeValue = document.getElementById('rangeValue');
    const exampleInput = document.getElementById('exampleInput');

    // Initialize the range value display
    rangeValue.textContent = exampleRange.value;

    addParagraphBtn.addEventListener('click', function() {
        // Get the input value and convert it to a positive integer
        let inputValue = parseInt(exampleInput.value, 10);
        if (isNaN(inputValue) || inputValue <= 0) {
            inputValue = 500; // Default value if input is invalid
        }

        const newParagraph = document.createElement('p');
        newParagraph.textContent = Array(inputValue).fill(null).map(() => Math.random().toString(36).charAt(2)).join('');
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
});;