import csv
import sys
import time
from datetime import timedelta
from config import config
from logger import Logger
from db import DB


TEMP_DIR = config['DATA']['TEMP_DIR']

logger = Logger('ETL')
db     = DB.getDB()

csv.register_dialect('Dialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)


class ETL:

  def __init__(self, name, sources, target, col_name, handler):
    self._name     = name
    self._sources  = sources
    self._target   = target
    self._col_name = col_name
    self._handler  = handler

    logger.info(f"{name} - Found '{len(sources)}' files from sources")

  def run(self):
    
    logger.info(f"Start '{self._name}' ETL process")

    start_time = time.time()

    if self._target["is_file"]:
      try:
        with open(self._target["target"], 'a') as target_file:
          writer = csv.writer(target_file, dialect='Dialect')
          writer.writerow(self._col_name)

          for file in self._sources:
            with open(file, 'r', encoding = 'utf8', newline='') as data_file:
              reader = csv.reader(data_file) 
              next(reader)

              for row in reader:
                if row[0]:
                  writer.writerow(self._handler(row))
      except IOError as e:
        logger.error(e)
      except:
        logger.error(f"Unexpected error: {sys.exc_info()[0]}")
    
    if self._target["target"] == "Cassandra":
      table_name = self._target["table"]
      cols_name  = ', '.join(self._col_name)
      values = ', '.join(['%s' for i in self._col_name])


      for file in self._sources:
        with open(file, 'r', encoding = 'utf8', newline='') as data_file:
          reader = csv.reader(data_file) 
          next(reader)

          for row in reader:
            if row[0]:
              db.execute(f"INSERT INTO {table_name} ({cols_name}) VALUES ({values})", self._handler(row))

    logger.info(f"Complete load data to {self._target['target']}")

    end_time = time.time()

    logger.info(f"ETL process done in {timedelta(seconds=end_time - start_time)}s")
