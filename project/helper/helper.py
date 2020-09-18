import os

class Helper:

  __instance = None

  @staticmethod 
  def getHelper():
    if Helper.__instance == None:
      Helper()
    return Helper.__instance

  def __init__(self, keyspace=None):
    if Helper.__instance:
      raise Exception("This class is a singleton!")
    else:
      Helper.__instance = self

  def join_path(self, path1, path2):
    return os.path.join(path1, path2)

  def get_files_from_folder(self, folder):
    return [os.path.join(dirpath, filename) \
            for (dirpath, dirnames, filenames) in os.walk(folder) \
            for filename in filenames if filenames]

  def remove_files_from_folder(self, folder):
    files = self.get_files_from_folder(folder)

    for file in files:
      os.remove(file)
