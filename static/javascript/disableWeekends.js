function disableWeekends(input) {
    var selectedDate = new Date(input.value);
    var dayOfWeek = selectedDate.getDay(); // 0 for Sunday, 1 for Monday, ..., 6 for Saturday
    
    // Disable Saturday (Day 6) and Sunday (Day 0)
    if (dayOfWeek === 0 || dayOfWeek === 6) {
      alert("Weekends (Saturday and Sunday) are not allowed. Please select a weekday.");
      input.value = ''; // Clear the input value
    }
  }