// Set the minimum date for the date picker to the current date
var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0'); // January is 0!
var yyyy = today.getFullYear();
    
var currentDate = yyyy + '-' + mm + '-' + dd;
document.getElementById('datePicker').setAttribute('min', currentDate);