import os
import configparser

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

parser = configparser.ConfigParser()
parser.read_file(open(os.path.join(ROOT_DIR, './config.ini')))

config = {
  "ROOT_DIR": ROOT_DIR,

  "CLUSTER": {
    "CLUSTER_NAME"     : parser.get('CLUSTER', 'CLUSTER_NAME'),
    "CLUSTER_KEYSPACE" : parser.get('CLUSTER', 'CLUSTER_KEYSPACE'),
    "CLUSTER_USERNAME" : parser.get('CLUSTER', 'CLUSTER_USERNAME'),
    "CLUSTER_PASSWORD" : parser.get('CLUSTER', 'CLUSTER_PASSWORD'),
    "CLUSTER_HOST"     : parser.get('CLUSTER', 'CLUSTER_HOST'),
    "CLUSTER_PORT"     : parser.getint('CLUSTER','CLUSTER_PORT')
  },

  "DATA": {
    "DATA_EVENT" : os.path.join(ROOT_DIR, f"./{parser.get('DATA', 'DATA_EVENT')}")
  },

  "LOG": {
    "LOG_DIR" : os.path.join(ROOT_DIR, f"./{parser.get('LOG','LOG_DIR')}")
  },
}