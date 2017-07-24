# Log File locations
LOG_FILE = "C:\\Users\\1022285\\Documents\\Database Logs\\alert_mydprd.log"
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
FROM = "hothritik1@gmail.com"
TO = "f2014480@pilani.bits-pilani.ac.in"
TEXT = "Test Content"
SERVER = "smtp.gmail.com"
PORT = "587"
PASSWORD = ""

# Turn this option to true if you always want to run in auto mode
FORCE_AUTO = False