import csv
from config import config
from logger import Logger
from helper import Helper
from db import DB


TEMP_DIR = config['DATA']['TEMP_DIR']

logger = Logger('ETL')
helper = Helper.getHelper()
db     = DB.getDB()

csv.register_dialect('Dialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)


class ETL:

  def __init__(self, sources):
    self._sources = sources

    logger.info(f"Found '{len(sources)}' files from sources")

  def create_staging_file(self, header, row_handler):
    with open(helper.join_path(TEMP_DIR, 'staging.csv'), 'a') as stage_file:
      writer = csv.writer(stage_file, dialect='Dialect')
      writer.writerow(header)

      for file in self._sources:
        with open(file, 'r', encoding = 'utf8', newline='') as data_file:
          reader = csv.reader(data_file) 
          next(reader)

          for row in reader:
            if row[0]:
              writer.writerow(row_handler(row))

    logger.info(f"Create staging file")


  def load_data():
    return None
