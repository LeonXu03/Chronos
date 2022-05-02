import datetime
from datetime import datetime, timedelta
from pytz import timezone
import re

format_with_timezone = '%Y-%m-%d %H:%M:%S %Z%z'
format_without_seconds = '%Y-%m-%d %H:%M'
format_date = '%Y-%m-%d'
format_time = '%H:%M'

# Get system's current datetime
def get_current_datetime_string_est(format):
    eastern = timezone('US/Eastern')

    current_datetime_est = datetime.now(eastern).strftime(format)

    return current_datetime_est

def get_integers_of_string(string):
    return int(re.search(r'\d+', string).group())

def has_digit(string):
    return any(char.isdigit() for char in string)

def valid_interval(interval):
    chars = "dhm"
    if any((char in interval and interval.count(char)==1 and interval.replace(char,"").isdigit()) for char in chars): return True
    else: return False

def check_valid_datetime(value):
    try:
        valid_datetime = datetime.strptime(value, "%Y-%m-%d %H:%M")
        if datetime_to_string_no_seconds(valid_datetime)>=get_current_datetime_string_est(format_without_seconds): return True
        else: False
    except:
        return False

def get_valid_datetime(value):
    try: 
        return datetime.strptime(value, "%Y-%m-%d %H:%M")
    except:
        return None

def datetime_to_string_no_seconds(value):
    try: 
        return datetime.strftime(value, "%Y-%m-%d %H:%M")
    except:
        return None

def add_time_to_datetime(past_datetime, interval):
        if "d" in interval:
            time = int(interval.replace("d", ""))
            time_change = timedelta(days=time)
            return past_datetime + time_change
        elif "h" in interval:
            time = int(interval.replace("h", ""))
            time_change = timedelta(hours=time)
            return past_datetime + time_change
        elif "m" in interval: 
            time = int(interval.replace("m", ""))
            time_change = timedelta(minutes=time)
            return past_datetime + time_change
        else: return None

def is_valid_team_channel(channel_name):
    pattern = re.compile('^team-\d-[a-z]')
    if pattern.match(channel_name) is None: return False
    else: return True

def is_expert_cohort_name(name):
    name = name.replace(" ", "")
    pattern = re.compile('^expert:cohort\d', re.IGNORECASE)
    if pattern.match(name) is None: return False
    else: return True

def case_insensitive_replace(word_to_be_replaced, word, string):
    return re.sub(word_to_be_replaced, word, string, flags=re.IGNORECASE).strip()