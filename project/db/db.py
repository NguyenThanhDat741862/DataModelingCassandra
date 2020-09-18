# import os.path
# import sys
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from config import config
from logger import Logger


CLUSTER_NAME     = config['CLUSTER']['CLUSTER_NAME']
CLUSTER_KEYSPACE = config['CLUSTER']['CLUSTER_KEYSPACE']
CLUSTER_USERNAME = config['CLUSTER']['CLUSTER_USERNAME']
CLUSTER_PASSWORD = config['CLUSTER']['CLUSTER_PASSWORD']
CLUSTER_HOST     = config['CLUSTER']['CLUSTER_HOST']
CLUSTER_PORT     = config['CLUSTER']['CLUSTER_PORT']

auth_provider = PlainTextAuthProvider(username=CLUSTER_USERNAME, password=CLUSTER_PASSWORD)
contact_points = [CLUSTER_HOST]

logger = Logger('DB')


class DB:

  __instance = None

  @staticmethod 
  def getDB():
    if DB.__instance == None:
      DB()
    return DB.__instance

  def __init__(self, keyspace=None):
    if DB.__instance:
      raise Exception("This class is a singleton!")
    else:
      DB.__instance = self

    try:
      self._cluster  = Cluster(contact_points, port=CLUSTER_PORT, auth_provider=auth_provider)
      logger.info(f"Setup cluster {CLUSTER_NAME}")

      self._keyspace = keyspace

    except Exception as e:
      logger.error(e)
  
  def __connect__(self):
    try:
      self._session = self._cluster.connect()
      if self._keyspace:
        self._session.set_keyspace(self._keyspace)
      logger.info(f"Open session to '{CLUSTER_NAME}' with keyspace '{self._keyspace}'")
    except Exception as e:
      logger.error(e)

  def __disconnect__(self):
    try:
      self._session.shutdown()
      logger.info(f"Close session to {CLUSTER_NAME}")
    except Exception as e:
      logger.error(e)

  def shutdown(self):
    try:
      self._cluster.shutdown()
      logger.info(f"Shutdown connect to cluster {CLUSTER_NAME}")
    except Exception as e:
      logger.error(e)

  def create_keyspace(self, keyspace=CLUSTER_KEYSPACE):
    cql = "CREATE KEYSPACE IF NOT EXISTS %s WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 2 }" % (keyspace)

    try:
      self.execute(cql)
      self._keyspace = keyspace
      logger.info(f"Create keyspace {keyspace}")
      
    except Exception as e:
      logger.error(e)

  def set_keyspace(self, keyspace):
    self._keyspace = keyspace

  def fetch(self, cql):
    self.__connect__()

    try:
      rows = self._session.execute(cql)
      logger.info(f"Executing: {cql}")
    except Exception as e:
      logger.error(e)
      
    self.__disconnect__()
    return rows 

  def execute(self, cql):
    self.__connect__()
    
    try:
      self._session.execute(cql)
      logger.info(f"Executing: {cql}")
    except Exception as e:
      logger.error(e)
    
    self.__disconnect__()
