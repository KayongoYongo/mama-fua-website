// Check Date
function checkDate(input) {
    var selectedDate = new Date(input.value);
    var currentDate = new Date();

    // Check if the selected date is before the current date
    if (selectedDate < currentDate) {
        alert("Please select a date beyond today.");
        input.value = ''; // Clear the input value
    }
}