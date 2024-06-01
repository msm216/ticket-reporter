document.addEventListener('DOMContentLoaded', function() {
    // Handle opening the modal
    document.getElementById('addTaskBtn').addEventListener('click', function() {
        openModal('Add Task', '/add_task', {});
    });

    // Handle form submission
    document.getElementById('form').addEventListener('submit', function(event) {
        event.preventDefault();
        submitForm();
    });

    // Handle closing the modal
    document.querySelector('.closeBtn').addEventListener('click', function() {
        closeModal();
    });

    // Event delegation for edit and delete buttons
    document.querySelector('table').addEventListener('click', function(event) {
        if (event.target.classList.contains('editBtn')) {
            const taskId = event.target.dataset.id;
            fetch(`/get_task/${taskId}`)
                .then(response => response.json())
                .then(data => {
                    openModal('Edit Task', `/edit_task/${taskId}`, data);
                });
        } else if (event.target.classList.contains('deleteBtn')) {
            const taskId = event.target.dataset.id;
            if (confirm('Are you sure you want to delete this task?')) {
                fetch(`/delete_task/${taskId}`, {
                    method: 'DELETE'
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload();
                    } else {
                        alert('Error deleting task');
                    }
                });
            }
        }
    });
});

function openModal(title, action, data) {
    document.getElementById('formModal').style.display = 'block';
    document.querySelector('.modal-content h2').textContent = title;
    document.getElementById('form').action = action;

    // Populate form fields with data
    for (const [key, value] of Object.entries(data)) {
        if (document.getElementById(key)) {
            document.getElementById(key).value = value;
        }
    }
}

function closeModal() {
    document.getElementById('formModal').style.display = 'none';
}

function submitForm() {
    const form = document.getElementById('form');
    const formData = new FormData(form);
    const action = form.action;

    fetch(action, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            closeModal();
            location.reload();
        } else {
            alert('Error submitting form');
        }
    });
}

// Chart.js for rendering charts on the home page
if (document.getElementById('taskBarChart') && document.getElementById('taskPieChart')) {
    fetch('/task_statistics')
        .then(response => response.json())
        .then(data => {
            const ctxBar = document.getElementById('taskBarChart').getContext('2d');
            const ctxPie = document.getElementById('taskPieChart').getContext('2d');

            new Chart(ctxBar, {
                type: 'bar',
                data: {
                    labels: data.bar.labels,
                    datasets: [{
                        label: 'Tasks per Week',
                        data: data.bar.data,
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

            new Chart(ctxPie, {
                type: 'pie',
                data: {
                    labels: data.pie.labels,
                    datasets: [{
                        label: 'Task Distribution',
                        data: data.pie.data,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)'
                        ],
                        borderWidth: 1
                    }]
                }
            });
        });
}