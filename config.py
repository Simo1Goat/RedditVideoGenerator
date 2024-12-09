import os

CLIENT_ID = os.getenv('CLIENT_ID', 'CLIENT_ID_VALUE')
SECRET_ID = os.getenv('SECRET_ID', 'SECRET_ID_VALUE')
APP_NAME = os.getenv('APP_NAME', 'APP_NAME_VALUE')

ELEVENLABS_URL = "https://api.elevenlabs.io/v1"
XI_API_KEY = "<xi_api_key>"

GECKODRIVER = "../tmp/gecko/geckodriver.exe"
REDDIT_SUBMISSION_PATH = {
    "title": {
        "handle": By.ID,
        "value": "t3_%s"
    },
    "comments": {
        "handle": By.ID,
        "value": "t1_%s"
    }
}
