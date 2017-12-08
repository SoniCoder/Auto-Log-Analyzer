"""
Author: Hritik Soni

Description:

This module is used for functioning of automatic mode.

All variable mentioned here will be passed to various procedures in the core module.

"""

# Log File locations
LOG_FILE = "C:\\Users\\1018848\\Desktop\\Upgrade Manager Standalone\\Upgrade Manager Standalone\\Database Logs\\Database Logs\\alert_mydprd.log"
LOG_FILES = []
LOG_FILES.append(LOG_FILE)
COMBINE_FILES = True

# Pattern Information
PATTERN = "TNS-\d{5}: .*"
PATTERNS = []
PATTERNS.append(PATTERN)

# Histogram Options
HISTOGRAM = True
WEEKLY_DISPLAY = True
YEAR = '2017'
MONTH = 'JAN'
WEEK = 3
ERROR = None

# Scheduler TIME_DELTA, MAX_DURATION (in minutes)
TIME_DELTA = 0.5
MAX_DURATION = 2

# Mailer Options
ATTACHMENTS = []
SUBJECT = "Test Subject"
FROM = "Achint.Gupta@jda.com"
TO = "Nikhar.Bajaj@jda.com"
TEXT = "Test Content"
SERVER = "mailout.jdadelivers.com"
PORT = "25"
PASSWORD = ""

# Turn this option to true if you always want to run in auto mode
FORCE_AUTO = False