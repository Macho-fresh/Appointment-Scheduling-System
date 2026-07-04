# Appointment App
### This project is an API for scheduing appointments with any provider, it includes timezones, appointment duration, appointments conflicts detection, unit tests,available slots for providers, cancel and complete appointments

## Table of content
- [Usage](#usage)
- [Tests](#tests)

# Usage
### Auth: The enndpoints for login,register and register provider are in accounts/urls.py I used JWT authentication

### App: the main app sits in appointment_app the endpoints are in appointment_app/urls.py. I made a small db normalization mistake and was too lazy to fix it so to send a request to /api/create-appointment/ youl send it in this format
# request to create appointment
# {
#   "provider": 3,
#   "provider_user": 1,
#   "start_date_time": "2026-07-01 08:30:00",
#   "end_date_time": "2026-07-01 09:00:00",
#   "weekday": "Monday"
# }

# Tests
### You'll find the unit tests in test.py of both accounts and appointment_app directories