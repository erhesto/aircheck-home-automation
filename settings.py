import os
import logging


AIRLY_API_KEY = os.environ.get('AIRLY_API_KEY')
LONGITUDE = float(os.environ.get('LONGITUDE', 0))
LATITUDE = float(os.environ.get('LATITUDE', 0))
MAX_DISTANCE_KM = int(os.environ.get('MAX_DISTANCE_KM', 5))
MAX_RESULTS = int(os.environ.get('MAX_RESULTS', 1))
API_URL = 'https://airapi.airly.eu/v2'
OUTPUT_PATH = 'status_file'
LOG_FILE = 'aircheck.log'
DEBUG = True
LOG_FORMAT='%(asctime)s:%(message)s'

# set up logging to file - see previous section for more details
logging.basicConfig(
    level=logging.DEBUG, 
    format=LOG_FORMAT,               
    datefmt='%m-%d %H:%M',
    filename=LOG_FILE,
    filemode='w'
)
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter(LOG_FORMAT)
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

