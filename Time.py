"""
This code calculate the time between 01-01-2026 00:00am till current
time and print it in two lines one has every format (mm,w,d,h,m) 
and the second line has only hours
"""

from datetime import datetime

start = datetime(2026, 1, 1, 0, 0)
now = datetime.now()
delta = now - start
total_minutes = int(delta.total_seconds() // 60)
total_hours = total_minutes // 60
total_days = total_hours // 24

months = total_days // 30
weeks = total_days // 7

if months >= 1:
    m = months
    d = total_days % 30
    h = total_hours % 24
    mn = total_minutes % 60
    print(f"{m} mois {d} jours {h} heures {mn} minutes")
elif weeks >= 1:
    w = weeks
    d = total_days % 7
    h = total_hours % 24
    mn = total_minutes % 60
    print(f"{w} semaines {d} jours {h} heures {mn} minutes")
else:
    d = total_days
    h = total_hours % 24
    mn = total_minutes % 60
    print(f"{d} jours {h} heures {mn} minutes")

print(f"{total_hours} heures")

# Pause the program so the window stays open
input()
