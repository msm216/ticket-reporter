document.addEventListener('DOMContentLoaded', function() {
    const paragraphContainer = document.getElementById('paragraph-container');
    const addParagraphBtn = document.getElementById('add-paragraph-btn');
    const exampleRange = document.getElementById('example-range');
    const rangeValue = document.getElementById('range-value');
    const exampleInput = document.getElementById('example-input');
    const exampleSelect = document.getElementById('example-select');

    // Initialize the range value display
    rangeValue.textContent = exampleRange.value;

    // Initialize the input value to 500 if empty
    if (!exampleInput.value) {
        exampleInput.value = 500;
    }

    addParagraphBtn.addEventListener('click', function() {
        // Get the input value and convert it to a positive integer
        let inputValue = parseInt(exampleInput.value, 10);
        if (isNaN(inputValue) || inputValue <= 0) {
            inputValue = 500; // Default value if input is invalid
            exampleInput.value = 500; // Reset input to default
        }

        const newParagraph = document.createElement('p');
        newParagraph.textContent = Array(inputValue).fill(null).map(() => Math.random().toString(36).charAt(2)).join('');
        newParagraph.style.fontSize = `${exampleRange.value}px`;
        newParagraph.style.fontFamily = exampleSelect.value;
        paragraphContainer.appendChild(newParagraph);
    });

    // Update input value in real-time
    exampleInput.addEventListener('input', function() {
        let inputValue = parseInt(exampleInput.value, 10);
        if (isNaN(inputValue) || inputValue <= 0) {
            // Don't clear the input, just let it be invalid
        }
    });

    exampleRange.addEventListener('input', function() {
        const paragraphs = paragraphContainer.getElementsByTagName('p');
        for (let p of paragraphs) {
            p.style.fontSize = `${exampleRange.value}px`;
        }
        rangeValue.textContent = exampleRange.value; // Update the range value display
    });

    exampleSelect.addEventListener('change', function() {
        const paragraphs = paragraphContainer.getElementsByTagName('p');
        for (let p of paragraphs) {
            p.style.fontFamily = exampleSelect.value;
        }
    });
});;