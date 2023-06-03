import sqlite3
import pandas as pd

class DBReader:
  def __init__(self, dbfile):
    print(dbfile)
    conn = sqlite3.connect(dbfile)
    self.melid_list = self.get_list("melid", "solo_info", conn)
    self.keys = self.get_dict("melid", "key", "solo_info", conn)
    self.styles = self.get_dict("melid", "style", "solo_info", conn)
    self.comp_ids = self.get_dict("melid", "compid", "solo_info", conn)
    self.genres = self.get_dict("compid", "genre", "composition_info", conn)
    self.tonality_types = \
      self.get_dict("compid", "tonalitytype", "composition_info", conn)
    self.signature_dict = self.get_dict("melid", "signature", "solo_info", conn)
    self.eventid_dict = self.get_list_dict("melid", "eventid", "melody", conn)
    self.first_eventid = self.get_first_eventid(self.melid_list, self.eventid_dict)
    self.melody_data = \
      self.get_dict_list_dict("melid", ["eventid", "pitch", "duration", "division", 
                                        "bar", "beat", "tatum", "beatdur"],
                                        "melody", conn)
    self.sect_data = \
      self.get_dict_list_dict("melid", ["type", "start", "end", "value"],
                              "sections", conn)
    self.chords = self.get_chords(self.melid_list, self.sect_data)

  def get_first_eventid(self, melid_list, eventid_dict):
    first_eventid = {}
    for id in melid_list:
      first_eventid[id] = min(eventid_dict[id])
    return first_eventid

  def get_chords(self, melid_list, sect_data):
    chords = {}
    for id in melid_list:
      chords[id] = []
      for e in sect_data[id]:
        if e["type"] == "CHORD" and e["value"] != "NC":
          chords[id].append(e)
    return chords

  def get_list(self, key, table, conn):
    data = pd.read_sql("SELECT " + key + " FROM " + table, conn)
    list = []
    for i in range(len(data)):
      list.append(data[key][i])
    return list

  def get_dict(self, key, value, table, conn):
    data = pd.read_sql("SELECT " + key + "," + value + " FROM " + table, conn)
    dict = {}
    for i in range(len(data)):
      dict[data[key][i]] = data[value][i]
    return dict

  def get_list_dict(self, key, value, table, conn):
    data = pd.read_sql("SELECT " + key + "," + value + " FROM " + table, conn)
    dict = {}
    for i in range(len(data)):
      keydata = data[key][i]
      if not keydata in dict:
        dict[keydata] = []
      dict[keydata].append(data[value][i])
    return dict

  def get_dict_list_dict(self, key, values, table, conn):
    data = pd.read_sql("SELECT " + key + ", " + ",".join(values) + 
                       " FROM " + table, conn)
    dict = {}
    for i in range(len(data)):
      keydata = data[key][i]
      if not keydata in dict:
        dict[keydata] = []
      e = {}
      for vk in values:
        e[vk] = data[vk][i]
      dict[keydata].append(e)
    return dict
