import datetime
import pytz

def get_current_time_in_nairobi():
    # Set the timezone for Nairobi
    nairobi_timezone = pytz.timezone('Africa/Nairobi')
    
    # Get the current time in UTC
    utc_time = datetime.datetime.now(pytz.utc)
    
    # Convert UTC time to Nairobi time
    nairobi_time = utc_time.astimezone(nairobi_timezone)
    
    # Format the datetime object as "day, month, year, hour, and seconds"
    formatted_time = nairobi_time.strftime("%A, %B %d, %Y, %H:%M:%S")
    
    return formatted_time
