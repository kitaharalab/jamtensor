from numpy.lib.type_check import mintypecode
import music21
import numpy as np

class NoteNumChordVec:
  MAX_NUM = 256
  KEY_ROOT_LIST = {"C":0, "C#": 1, "Db":1, "D":2, "D#": 3, "Eb":3, "E":4, 
                   "F":5, "F#": 6, "Gb":6, "G":7, "G#":8, "Ab":8, "A":9, 
                   "A#":10, "Bb":10, "B":11}
  CHORD_CONVERSION_LIST = [("-", "m"), 
                           ("b", "-"),
                           ("-5", "b5"),
                           ("9#", "#9"),
                           ("911#", "9"),     #修正
                           ("9-", "b9"),
                           ("911-", "9"),     #修正
                           ("913-", "9"),     #修正
                           ("91113-", "9"),   #修正
                           ("j7", "maj7"),
                           ("sus713", "7sus4"),
                           ("sus71113", "7sus4"),
                           ("sus711", "7sus4"),
                           ("sus7911", "7sus4"),
                           ("sus7913", "7sus4"),
                           ("sus791113", "7sus4"),
                           ("sus79", "7sus4"),
                           ("sus7", "7sus4"),
                           ("69", "6"),
                           ("alt", ""),
                           ("mmaj7", "m"),
                           ("maj79", "maj7"),
                           ("m79", "m7")]

  def __init__(self, melchords): 
    self.notenums = {}
    self.chords = {}
    self.melid_list = []
    for id in melchords.melid_list:
      if melchords.keys[id] == "":
        continue
      self.melid_list.append(id)
      self.notenums[id] = self.transpose_to_c(
          self.noteobj_to_notenums(melchords.melodies[id]), 
          melchords.keys[id], True)
      self.chords[id] = self.chords_to_vec(melchords.chords[id], melchords.keys[id])

  def noteobj_to_notenums(self, melody):
#    return [e["pitch"] if e != None else None for e in melody]
    notenums = [None] * len(melody)
    for i in range(len(melody)):
      if melody[i] != None:
        notenums[i] = melody[i]["pitch"]
        if i > 0 and melody[i-1] != None:
          if melody[i-1]["eventid"] == melody[i]["eventid"]:
            notenums[i] = notenums[i] + self.MAX_NUM
    return notenums

  def transpose_to_c(self, melody, key, rotate):
    root = key[0 : (key.index("-"))]
    k = self.KEY_ROOT_LIST[root]
    if rotate:
      k = k - 12 if k >= 6 else k
#    return [np.sign(n) * (abs(n) - k) if n != None else None for n in melody]
    return [n - k if n != None else None for n in melody]

  def chords_to_vec(self, chords, key):
    list = []
    for c in chords:
      vec = np.zeros(12)
      if c != None:
        chord = c["value"]
        chord = chord[0 : chord.index("/")] if "/" in chord else chord
        for conv in self.CHORD_CONVERSION_LIST:
          chord = chord.replace(conv[0], conv[1])
        cs = music21.harmony.ChordSymbol(chord)
        notes = self.transpose_to_c([n.pitch.pitchClass for n in cs._notes], key, False)
        for n in notes:
          vec[n % 12] = 1
      list.append(vec)
    return list
  
  def zeropadding(self, notenums, chords, length):
    if len(notenums) < length:
      notenums = notenums + [None] * (length - len(notenums))
    if len(chords) < length:
      chords = chords + [np.zeros(len(chords[0]))] * (length - len(chords))
    return notenums, chords

  def move_octave(self, notenums, oct):
    return [np.sign(n) * (abs(n)+ oct * 12) if n != None else None for n in notenums]

  def highest_notenum(self, notenums):
    return max([n % self.MAX_NUM for n in filter(None, notenums)])

  def lowest_notenum(self, notenums):
    return min([n % self.MAX_NUM for n in filter(None, notenums)])
