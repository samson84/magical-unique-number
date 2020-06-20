from os import path, environ
from dotenv import load_dotenv

TEST_DIR = path.dirname(path.realpath(__file__))
INIT_SCRIPT = path.join(TEST_DIR, '..', '..', 'sql','init',  'init.sql')
TEST_ENV_FILE = path.join(TEST_DIR, '..', '..', 'test.env')

load_dotenv(TEST_ENV_FILE)

# keep the unique test db-s after test runs for debugging
KEEP_DB = False
TEST_DB_USER=environ['POSTGRES_USER']
TEST_DB_PASSWORD=environ['POSTGRES_PASSWORD']
TEST_DB_HOST=environ['POSTGRES_HOST']
TEST_DB_PORT=environ['POSTGRES_PORT']
TEST_DB_BASE_DB_NAME=environ['POSTGRES_DB']

