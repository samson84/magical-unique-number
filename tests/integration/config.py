from os import path

# keep the unique test db-s after test runs for debugging
KEEP_DB = False
TEST_DB_USER='test'
TEST_DB_PASSWORD='test'
TEST_DB_HOST='localhost'
TEST_DB_PORT=5001
TEST_DB_BASE_DB_NAME='postgres'

TEST_DIR = path.dirname(path.realpath(__file__))
INIT_SCRIPT = path.join(TEST_DIR, '..', '..', 'sql','init',  'init.sql')
