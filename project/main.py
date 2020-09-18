from config import config
from logger import Logger
from db import DB


def setup_db():
  db = DB()
  db.create_keyspace()

def shutdown_db():
  db = DB.getDB()
  db.shutdown()

def main():
  print('Hello world')


if __name__ == "__main__":
  setup_db()
  main()
  shutdown_db()