import csv
import sys
from config import config
from logger import Logger
from helper import Helper
from etl import ETL
from db import DB


TEMP_DIR   = config['DATA']['TEMP_DIR']
RESULT_DIR = config['RESULT']['RESULT_DIR']

logger = Logger('TASK')
helper = Helper.getHelper()
db     = DB.getDB()

csv.register_dialect('Dialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)


class Task:

  def __init__(self, name, question, db_table, row_handler, answer_cql):
    self._name       = name
    self._question   = question
    self._db_table   = db_table
    self._answer_cql = answer_cql
    self._etl        = ETL(
      f"{name} ETL",
      [helper.join_path(TEMP_DIR, 'staging.csv')],
      {
        "target"  : 'Cassandra',
        "table"   : db_table["table_name"],
        "is_file" : False
      },
      [i[0] for i in db_table["cols"]],
      row_handler,
    )

    logger.info(f"{self._name} - Question: {self._question}")

  def _create_table(self):
    table_name, cols, key = self._db_table.values()
    cql_col_types = ', '.join([f"{col[0]} {col[1]}" for col in cols])
    
    db.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({cql_col_types}, PRIMARY KEY({key}))")

    logger.info(f"{self._name} - Create '{table_name}' table")

  def _get_result(self):
    result = db.fetch(self._answer_cql)

    result_col_name = helper.get_str_between(self._answer_cql, 'SELECT', 'FROM')[0].strip().split(', ')

    try:
      with open(helper.join_path(RESULT_DIR, f'{self._name}.csv'), 'a') as target_file:
        writer = csv.writer(target_file, dialect='Dialect')
        writer.writerow(result_col_name)

        for row in result:
          writer.writerow(row)
    except IOError as e:
      logger.error(e)
    except:
      logger.error(f"Unexpected error: {sys.exc_info()[0]}")

    logger.info(f"{self._name} - Complete generate '{self._name}.csv' file")

  def run(self):
    self._create_table()

    self._etl.run()
    logger.info(f"{self._name} - Complete ETL process")

    self._get_result()
