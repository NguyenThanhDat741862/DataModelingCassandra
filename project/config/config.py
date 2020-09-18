import os
import configparser
from helper import Helper

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

helper = Helper.getHelper()

parser = configparser.ConfigParser()
parser.read_file(open(helper.join_path(ROOT_DIR, './config.ini')))

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
    "DATA_EVENT" : helper.join_path(ROOT_DIR, f"./{parser.get('DATA', 'DATA_EVENT')}"),
    "TEMP_DIR"   : helper.join_path(ROOT_DIR, f"./{parser.get('DATA', 'TEMP_DIR')}"),
  },

  "LOG": {
    "LOG_DIR" : helper.join_path(ROOT_DIR, f"./{parser.get('LOG','LOG_DIR')}")
  },
}