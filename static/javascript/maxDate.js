// Set the maximum date for the date picker to 7 days from today
var maxDate = new Date();
maxDate.setDate(maxDate.getDate() + 7);

var ddMax = String(maxDate.getDate()).padStart(2, '0');
var mmMax = String(maxDate.getMonth() + 1).padStart(2, '0'); // January is 0!
var yyyyMax = maxDate.getFullYear();

var maxDateString = yyyyMax + '-' + mmMax + '-' + ddMax;
document.getElementById('datePicker').setAttribute('max', maxDateString);