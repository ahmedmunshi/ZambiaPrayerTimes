from datetime import datetime
import math

def get_prayer_times(date, latitude, longitude, timezone):
    """
    This is a placeholder function. In a real application, you would use 
    a proper prayer time calculation algorithm based on location.
    
    For now, we'll just use static data from our JSON files.
    
    Future implementation could use libraries like:
    - PrayTimes (http://praytimes.org/code/)
    - prayer-times-calculator (https://pypi.org/project/prayer-times-calculator/)
    """
    # In a real implementation, this would calculate prayer times
    # based on date, location, and calculation method
    
    return None

def get_next_prayer(prayer_times):
    """
    Determine the next prayer based on current time
    Returns a dict with name and time of the next prayer
    """
    if not prayer_times:
        return None
    
    now = datetime.now()
    current_hour = now.hour
    
    current_minute = now.minute
    current_total_minutes = current_hour * 60 + current_minute
    
    # Define prayer order
    prayers = [
        {'name': 'Fajr', 'key': 'fajr'},
        {'name': 'Dhuhr', 'key': 'dhuhr'},
        {'name': 'Asr', 'key': 'asr'},
        {'name': 'Maghrib', 'key': 'maghrib'},
        {'name': 'Isha', 'key': 'isha'}
    ]
    
    # Find the next prayer
    next_prayer = None
    min_time_diff = float('inf')
    
    for prayer in prayers:
        key = prayer['key']
        if key in prayer_times:
            prayer_time = prayer_times[key]['time'] if isinstance(prayer_times[key], dict) else prayer_times[key]
            
            # Convert prayer time to minutes
            prayer_hour, prayer_minute = map(int, prayer_time.split(':'))
            prayer_total_minutes = prayer_hour * 60 + prayer_minute
            
            # Calculate time difference (handling next day)
            if prayer_total_minutes > current_total_minutes:
                # Prayer is later today
                time_diff = prayer_total_minutes - current_total_minutes
                if time_diff < min_time_diff:
                    min_time_diff = time_diff
                    next_prayer = {
                        'name': prayer['name'],
                        'time': prayer_time,
                        'iqamah': prayer_times[key].get('iqamah', None) if isinstance(prayer_times[key], dict) else None
                    }
    
    # If no next prayer today, return the first prayer of the next day
    if next_prayer is None:
        first_prayer = prayers[0]
        key = first_prayer['key']
        
        if key in prayer_times:
            prayer_time = prayer_times[key]['time'] if isinstance(prayer_times[key], dict) else prayer_times[key]
            return {
                'name': first_prayer['name'],
                'time': prayer_time,
                'iqamah': prayer_times[key].get('iqamah', None) if isinstance(prayer_times[key], dict) else None,
                'tomorrow': True
            }
    
    return next_prayer

def calculate_countdown(prayer_time, tomorrow=False):
    """
    Calculate the countdown to the given prayer time
    Returns a dict with hours and minutes
    """
    now = datetime.now()
    
    # Parse prayer time
    hour, minute = map(int, prayer_time.split(':'))
    prayer_datetime = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    # If prayer time is in the past or marked as tomorrow, set it for tomorrow
    if tomorrow or prayer_datetime < now:
        prayer_datetime = prayer_datetime.replace(day=now.day + 1)
    
    # Calculate time difference
    diff = prayer_datetime - now
    total_seconds = diff.total_seconds()
    
    hours = math.floor(total_seconds / 3600)
    minutes = math.floor((total_seconds % 3600) / 60)
    seconds = math.floor(total_seconds % 60)
    
    return {
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds,
        'total_seconds': total_seconds
    }

def convert_to_hijri(gregorian_date):
    """
    Convert Gregorian date to Hijri date using the Kuwaiti algorithm
    For more accuracy in a production app, consider using a specialized library
    
    Returns a dict with year, month, day, and month_name
    """
    # Ensure we're working with a datetime object
    if not isinstance(gregorian_date, datetime):
        if isinstance(gregorian_date, str):
            gregorian_date = datetime.strptime(gregorian_date, '%Y-%m-%d')
        else:
            return None
    
    # Islamic calendar begins on 16 July 622 CE Julian (19 July 622 CE Gregorian)
    # This is 1/1/1 Hijri (1 Muharram 1 AH)
    hijri_epoch = datetime(622, 7, 19)
    
    # Get days since Hijri epoch
    days_since_epoch = (gregorian_date - hijri_epoch).days
    
    # Each Hijri year has about 354.36708 days on average (based on 30-year cycle)
    hijri_year = math.floor(days_since_epoch / 354.36708)
    
    # Adjust for the 30-year cycle 
    # (11 leap years of 355, 19 regular years of 354 days)
    thirty_year_cycles = math.floor(hijri_year / 30)
    year_in_cycle = hijri_year % 30
    
    # Leap years in a 30-year cycle are years 2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29
    leap_years_passed = 0
    leap_years = [2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29]
    for leap_year in leap_years:
        if year_in_cycle >= leap_year:
            leap_years_passed += 1
    
    # Adjust for leap years
    days_in_hijri_years = (hijri_year * 354) + thirty_year_cycles * 11 + leap_years_passed
    days_remaining = days_since_epoch - days_in_hijri_years
    
    # If remaining days are negative, adjust year
    if days_remaining < 0:
        hijri_year -= 1
        
        # Recalculate days in Hijri years
        thirty_year_cycles = math.floor(hijri_year / 30)
        year_in_cycle = hijri_year % 30
        
        leap_years_passed = 0
        for leap_year in leap_years:
            if year_in_cycle >= leap_year:
                leap_years_passed += 1
        
        days_in_hijri_years = (hijri_year * 354) + thirty_year_cycles * 11 + leap_years_passed
        days_remaining = days_since_epoch - days_in_hijri_years
    
    # Determine month and day
    # Odd-numbered months have 30 days, even-numbered months have 29 days
    # Except in leap years where the 12th month (Dhu al-Hijjah) has 30 days
    hijri_month = 1
    days_in_month = 30
    
    while days_remaining >= days_in_month:
        days_remaining -= days_in_month
        hijri_month += 1
        
        # Switch between 30-day and 29-day months
        if hijri_month <= 12:
            if hijri_month % 2 == 1:  # Odd months have 30 days
                days_in_month = 30
            else:  # Even months have 29 days
                days_in_month = 29
                
            # Exception: Last month has 30 days in leap years
            if hijri_month == 12 and (year_in_cycle + 1) in leap_years:
                days_in_month = 30
        else:
            break
    
    # The remaining days are the day of the month
    hijri_day = days_remaining + 1
    
    # Hijri month names
    hijri_month_names = [
        "Muharram", "Safar", "Rabi al-Awwal", "Rabi al-Thani",
        "Jumada al-Awwal", "Jumada al-Thani", "Rajab", "Sha'ban",
        "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah"
    ]
    
    # Ensure valid ranges
    if hijri_month > 12:
        hijri_month = 12
    if hijri_day > 30:
        hijri_day = 30
    
    return {
        'year': hijri_year,
        'month': hijri_month,
        'day': hijri_day,
        'month_name': hijri_month_names[hijri_month - 1]
    } 