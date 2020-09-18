from config import config
from logger import Logger
from helper import Helper
from db import DB
from etl import ETL


DATA_EVENT = config['DATA']['DATA_EVENT']
TEMP_DIR   = config['DATA']['TEMP_DIR']
LOG_DIR    = config['LOG']['LOG_DIR']

helper = Helper.getHelper()

def setup_db():
  db = DB.getDB()
  db.create_keyspace()

def shutdown_db():
  db = DB.getDB()
  db.shutdown()

def main():
  helper.remove_files_from_folder(TEMP_DIR)

  data_sources = helper.get_files_from_folder(DATA_EVENT)

  etl = ETL(data_sources)
  etl.create_staging_file(['artist','firstName','gender','itemInSession',\
                          'lastName','length', 'level','location',\
                          'sessionId','song','userId'],
                          lambda row : [row[0], row[2], row[3], row[4], \
                                        row[5], row[6], row[7], row[8], \
                                        row[12], row[13], row[16]]
                          )


if __name__ == "__main__":
  setup_db()
  main()
  shutdown_db()