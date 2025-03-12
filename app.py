from flask import Flask, render_template, jsonify, request # type: ignore
from datetime import datetime, timedelta
import json
import os
from utils.prayer_times import get_prayer_times, get_next_prayer, calculate_countdown, convert_to_hijri

app = Flask(__name__)

# Custom Jinja filter to format current year
@app.template_filter('now')
def now_filter(format_string):
    return datetime.now().strftime(format_string)

# Load mosque data
def load_mosque_data():
    try:
        with open('data/mosques.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def load_prayer_times(mosque_id, date_str=None):
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')
    
    try:
        with open(f'data/prayer_times/{mosque_id}.json', 'r') as f:
            mosque_data = json.load(f)
            return mosque_data.get('prayer_times', {}).get(date_str)
    except FileNotFoundError:
        return None

@app.route('/')
def home():
    # Get current date
    today = datetime.now()
    date_str = today.strftime('%Y-%m-%d')
    
    # Get list of all mosques
    mosques = load_mosque_data()
    
    # Default to first mosque if available
    default_mosque_id = mosques[0]['id'] if mosques else None
    
    # Get selected mosque (from query param or default)
    mosque_id = request.args.get('mosque_id', default_mosque_id)
    
    # Get prayer times for the selected mosque and date
    prayer_times = load_prayer_times(mosque_id, date_str)
    
    # Get next prayer and countdown
    next_prayer = None
    countdown = None
    
    if prayer_times:
        next_prayer = get_next_prayer(prayer_times)
        if next_prayer:
            tomorrow = next_prayer.get('tomorrow', False)
            countdown = calculate_countdown(next_prayer['time'], tomorrow)
    
    # Find selected mosque info
    selected_mosque = next((m for m in mosques if m['id'] == mosque_id), None)
    
    # Get Hijri date
    hijri_date = convert_to_hijri(today)
    
    return render_template('index.html', 
                          date=today,
                          hijri_date=hijri_date,
                          mosque=selected_mosque,
                          mosques=mosques,
                          selected_mosque_id=mosque_id,
                          prayer_times=prayer_times,
                          next_prayer=next_prayer,
                          countdown=countdown)

@app.route('/mosque/<mosque_id>')
def mosque_details(mosque_id):
    # Get mosque information
    mosques = load_mosque_data()
    mosque = next((m for m in mosques if m['id'] == mosque_id), None)
    
    if not mosque:
        return "Mosque not found", 404
    
    # Get today's prayer times
    today = datetime.now().strftime('%Y-%m-%d')
    prayer_times = load_prayer_times(mosque_id, today)
    
    # Get Hijri date
    hijri_date = convert_to_hijri(datetime.now())
    
    return render_template('mosque.html', 
                          mosque=mosque,
                          mosques=mosques,
                          selected_mosque_id=mosque_id,
                          prayer_times=prayer_times,
                          date=datetime.now(),
                          hijri_date=hijri_date)

@app.route('/schedule')
def schedule():
    # Get all mosques
    mosques = load_mosque_data()
    
    if not mosques:
        return render_template('schedule.html', 
                              mosque=None,
                              mosques=[],
                              selected_mosque_id=None,
                              dates=[])
    
    # Get selected mosque (from query param or default to first)
    mosque_id = request.args.get('mosque_id', mosques[0]['id'])
    
    # Get dates for the next 7 days
    dates = []
    today = datetime.now()
    for i in range(7):
        date = today + timedelta(days=i)
        date_str = date.strftime('%Y-%m-%d')
        
        # Get prayer times for this date
        prayer_times = load_prayer_times(mosque_id, date_str)
        
        # Get Hijri date
        hijri_date = convert_to_hijri(date)
        
        dates.append({
            'date': date,
            'hijri_date': hijri_date,
            'prayer_times': prayer_times
        })
    
    # Find selected mosque info
    selected_mosque = next((m for m in mosques if m['id'] == mosque_id), None)
    
    return render_template('schedule.html',
                          mosque=selected_mosque,
                          mosques=mosques,
                          selected_mosque_id=mosque_id,
                          dates=dates)

@app.route('/api/prayer-times/<mosque_id>/<date>')
def api_prayer_times(mosque_id, date):
    prayer_times = load_prayer_times(mosque_id, date)
    
    if not prayer_times:
        return jsonify({"error": "Prayer times not found"}), 404
    
    return jsonify(prayer_times)

# Helper function to update JSON files with current dates
def update_prayer_times_with_current_dates():
    """
    This function updates the prayer times in the JSON files to match the current dates.
    Useful for demonstration purposes so the app shows current dates instead of old dates.
    """
    try:
        # Get all mosque prayer time files
        mosque_files = os.listdir('data/prayer_times')
        
        for file in mosque_files:
            file_path = f'data/prayer_times/{file}'
            
            # Read the file
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Get the prayer times
            prayer_times = data.get('prayer_times', {})
            
            # If there are no prayer times, skip this file
            if not prayer_times:
                continue
            
            # Get sample dates and prayer times
            sample_dates = list(prayer_times.keys())
            sample_prayer_times = list(prayer_times.values())
            
            # Clear existing prayer times
            data['prayer_times'] = {}
            
            # Add prayer times for the current dates
            for i in range(min(len(sample_dates), 7)):
                current_date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
                data['prayer_times'][current_date] = sample_prayer_times[i % len(sample_prayer_times)]
            
            # Write the updated data back to the file
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
    
    except Exception as e:
        print(f"Error updating prayer times with current dates: {e}")

if __name__ == '__main__':
    # Ensure data directories exist
    os.makedirs('data/prayer_times', exist_ok=True)
    
    # Update prayer times with current dates (for demo purposes)
    update_prayer_times_with_current_dates()
    
    # Use environment variables for port if available (for deployment)
    port = int(os.environ.get('PORT', 8081))
    app.run(host='0.0.0.0', port=port, debug=False if os.environ.get('PRODUCTION') else True) 