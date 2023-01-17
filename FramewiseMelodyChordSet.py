class FramewiseMelodyChordSet:
  def __init__(self, db, tonality_types, opts):
    self.n_beats = opts["n_beats"]
    self.division = opts["division"]
    self.melid_list = []
    self.keys = {}
    self.tonality_types = {}
    self.melodies = {}
    self.chords = {}
    for id in db.melid_list:
      this_tonality_type = db.tonality_types[db.comp_ids[id]]
      if this_tonality_type in tonality_types:
        self.tonality_types[id] = this_tonality_type
        self.melid_list.append(id)
        self.keys[id] = db.keys[id]
        self.melodies[id] = self.melody_to_framewise(db.melody_data[id])
        self.chords[id] = self.chords_to_framewise(db.chords[id], db.melody_data[id])

  def melody_to_framewise(self, melody): 
    lastbar = max([e["bar"] for e in melody])
    list = [None] * int((lastbar + 1) * (self.n_beats * self.division))
    for e in melody:
      index = int(0.5 + ((e["bar"]-1) * self.n_beats + (e["beat"]-1)) * self.division
                   + self.division * (e["tatum"]-1) / e["division"])
      dur = int(0.5+self.division * e["duration"] / e["beatdur"])
      for d in range(dur+1):
        if 0 <= index+d and index+d < len(list):
          list[index+d] = e
    return list

  def chords_to_framewise(self, chords, melody):
    lastbar = max([e["bar"] for e in melody])
    list = [None] * int((lastbar + 1) * (self.n_beats * self.division))
    for c in chords:
      notes = melody[c["start"] : (c["end"] + 1)]
      n0 = notes[0]
      i0 = int(0.5+((n0["bar"]-1) * self.n_beats + (n0["beat"]-1)) * self.division 
                + self.division * (n0["tatum"]-1) / n0["division"])
      n1 = notes[-1]
      i1 = int(0.5+((n1["bar"]-1) * self.n_beats + (n1["beat"]-1)) * self.division 
                + self.division * (n1["tatum"]-1) / n1["division"])
      dur = int(0.5+self.division * n1["duration"] / n1["beatdur"])
      for i in range(i0, i1+dur+1):
        if 0 <= i and i < len(list):
          list[i] = c
    return list