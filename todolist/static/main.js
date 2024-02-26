// main.js

document.addEventListener('DOMContentLoaded', function () {
    // Get the Status header link
    var statusHeader = document.querySelector('.tableheaderlink a[href*="order_by=status"]');

    // Get the h2 element with the class 'current_tasks'
    var currentTasksHeader = document.querySelector('h2.current_tasks');

    // Add a click event listener to the Status header link
    statusHeader.addEventListener('click', function (event) {
        // Toggle between 'Current Tasks' and 'Completed Tasks'
        currentTasksHeader.innerText = currentTasksHeader.innerText === 'Current Tasks' ? 'Completed Tasks' : 'Current Tasks';

        // Prevent the default behavior of the link
        event.preventDefault();
    });
});
