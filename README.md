# Zambia Prayer Times App

A Flask web application that displays Islamic prayer times for mosques in Zambia. The app features prayer time countdowns, daily prayer schedules with iqamah times, Hijri/Gregorian date conversion, and mosque information display.

## Features

- **Prayer Time Countdown**: Real-time countdown to the next prayer
- **Daily Prayer Schedule**: View today's prayer times for selected mosque
- **Weekly Schedule**: Full 7-day prayer time schedule
- **Mosque Information**: View details about different mosques in Zambia
- **Hijri Date Conversion**: Display of the current Hijri date
- **Responsive Design**: Mobile-friendly interface with a blue gradient theme

## Screenshots

(Screenshots would be included here when the app is running)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/zambia-prayer-times.git
cd zambia-prayer-times
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Visit `http://localhost:5000` in your browser to view the app

## Project Structure

```
/
├── app.py                 # Main Flask application
├── requirements.txt       # Project dependencies
├── README.md              # Project documentation
├── static/                # Static files (CSS, JS, images)
├── templates/             # HTML templates
│   ├── base.html          # Base template with layout
│   ├── index.html         # Homepage with countdown timer
│   ├── mosque.html        # Mosque details page
│   └── schedule.html      # Weekly schedule page
├── utils/                 # Utility functions
│   └── prayer_times.py    # Prayer time calculations
└── data/                  # JSON data storage
    ├── mosques.json       # Mosque information
    └── prayer_times/      # Prayer time schedules
        ├── mecca-islamic-center.json
        ├── masjid-al-noor.json
        └── islamic-center-ndola.json
```

## Implementation Notes

- **Prayer Time Calculation**: The current implementation uses static JSON data for prayer times. In a production environment, you would use a proper prayer time calculation library based on geographical coordinates.
- **Hijri Date Conversion**: A simplified implementation is used. For more accurate conversion, consider using a dedicated Hijri calendar library.
- **Data Storage**: JSON files are used for simplicity. For a production application, consider using a database.

## Future Improvements

- Implement actual prayer time calculation based on latitude/longitude
- Add user accounts for mosque administrators to update prayer times
- Integrate with a real map service for mosque locations
- Create a mobile app version
- Add notification features for prayer times
- Implement multi-language support

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Built with [Flask](https://flask.palletsprojects.com/)
- Styled with [Tailwind CSS](https://tailwindcss.com/)
- Icons from [Heroicons](https://heroicons.com/) 