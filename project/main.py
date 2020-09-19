from config import config
from logger import Logger
from helper import Helper
from task import Task
from db import DB
from etl import ETL


DATA_EVENT = config['DATA']['DATA_EVENT']
TEMP_DIR   = config['DATA']['TEMP_DIR']
RESULT_DIR = config['RESULT']['RESULT_DIR']
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
  helper.remove_files_from_folder(RESULT_DIR)


  staging_etl = ETL(
    'Staging',
    helper.get_files_from_folder(DATA_EVENT), 
    {
      "target"  : helper.join_path(TEMP_DIR, 'staging.csv'),
      "is_file" : True
    },
    [
      'artist','firstName','gender','itemInSession',\
      'lastName','length', 'level','location',\
      'sessionId','song','userId'
    ],
    lambda row : [
      row[0], row[2], row[3], row[4], \
      row[5], row[6], row[7], row[8], \
      row[12], row[13], row[16]
    ],
  )

  staging_etl.run()

  tasks = [
    Task(
      'Task_01',
      f"Find the artist, song title and song's length in the music app history that was heard during sessionId = 338, and itemInSession = 4",
      {
        "table_name" : "session_songs",
        "cols"       : [
          ('sessionId', 'int'), ('itemInSession', 'int'), ('artist', 'text'), \
          ('song_title', 'text'), ('song_length', 'float')
        ],
        "key"        : 'sessionId, itemInSession'
      },
      lambda row : [int(row[8]), int(row[3]), row[0], row[9], float(row[5])],
      "SELECT artist, song_title, song_length FROM session_songs WHERE sessionId = 338 AND itemInSession = 4"
    ),
    Task(
      'Task_02',
      f"Find only the following: name of artist, song (sorted by itemInSession) and user (first and last name) for userid = 10, sessionid = 182",
      {
        "table_name" : "user_songs",
        "cols"       : [
          ('userId', 'int'), ('sessionId', 'int'), ('artist', 'text'), ('song', 'text'), \
          ('firstName', 'text'), ('lastName', 'text'), ('itemInSession', 'int')
        ],
        "key"        : '(userId, sessionId), itemInSession'
      },
      lambda row : [int(row[10]), int(row[8]), row[0], row[9], row[1], row[4], int(row[3])],
      "SELECT itemInSession, artist, song, firstName, lastName FROM user_songs WHERE userId = 10 AND sessionId = 182"
    ),
    Task(
      'Task_03',
      f"Find every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'",
      {
        "table_name" : "app_history",
        "cols"       : [
          ('song', 'text'), ('firstName', 'text'), ('lastName', 'text'), ('userId', 'int')
        ],
        "key"        : 'song, userId'
      },
      lambda row : [row[9], row[1], row[4], int(row[10])],
      "SELECT firstName, lastName FROM app_history WHERE song = 'All Hands Against His Own'"
    )
  ]

  for task in tasks:
    task.run()


if __name__ == "__main__":
  setup_db()
  main()
  shutdown_db()