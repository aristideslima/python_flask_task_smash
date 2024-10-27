import datetime
import pytz  # Recommended for timezone handling

# Get the current UTC datetime (timezone-aware)
utc_now = datetime.datetime.now(tz=datetime.timezone.utc)
print(f"Current UTC Time (timezone-aware): {utc_now}")
print(f"ISO Format: {utc_now.isoformat()}")  # Often useful for APIs and databases

# Get the current time in a specific timezone (e.g., Los Angeles)
la_timezone = pytz.timezone('America/Los_Angeles')
la_now = datetime.datetime.now(tz=la_timezone)
print(f"Current LA Time (timezone-aware): {la_now}")

# Get the current time in a specific timezone (e.g., Recife)
rec_timezone = pytz.timezone('America/Recife')
rec_now = datetime.datetime.now(tz=rec_timezone)
print(f"Current Recife Time (timezone-aware): {rec_now}")

# Correct way to work with timezones and calculations:

utc_dt = datetime.datetime(2024, 1, 15, 10, 0, 0, tzinfo=datetime.timezone.utc)
la_dt = utc_dt.astimezone(la_timezone)  # Convert to LA time
print(f"UTC Time: {utc_dt}")
print(f"LA Time: {la_dt}")
