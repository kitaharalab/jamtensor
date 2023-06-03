import numpy as np
import scipy
from sklearn.model_selection import train_test_split
from .NoteNumChordVec import NoteNumChordVec

class NoteNumMatrix:

  def notenums_to_onehot(self, noteseq):
    MAX_NUM = NoteNumChordVec.MAX_NUM
    self.pitch_range = self.pitch_thru - self.pitch_from 
    self.melody_dim = self.pitch_range * 2 + 1
    seq = []
    for nn in noteseq:
      vec = np.zeros(self.melody_dim)    #「継続」要素を追加
      if nn == None:
        vec[-1] = 1
      elif nn >= MAX_NUM:                #「継続」要素処理
        nn_ = nn - MAX_NUM  
        if self.pitch_from <= nn_ and nn_ < self.pitch_thru:
          vec[int(nn_ - self.pitch_from + self.pitch_range)] = 1
        else:
          print("Warning: pitch " + str(nn_) + " is out of range")
      else:
        if self.pitch_from <= nn and nn < self.pitch_thru:
          vec[int(nn - self.pitch_from)] = 1
        else:
          print("Warning: pitch " + str(nn) + " is out of range")
      seq.append(vec)
    return seq

  def get_melody_elements(self, x):
    return x[:, 0:self.melody_dim]

  def get_chord_elements(self, x):
    return x[:, self.melody_dim:]


class NoisyNoteNumMatrix(NoteNumMatrix):
  def __init__(self, opts):
    self.pitch_from = opts["pitch_from"]
    self.pitch_thru = opts["pitch_thru"]
    self.noise_level = opts["noise_level"]
  
  def make_xy(self, notenums, chords):
    melody_seq = np.array(self.notenums_to_onehot(notenums))
    melody_seq_with_noise = \
      np.array(self.notenums_to_onehot(self.add_noise(notenums, 2)))
    x = np.concatenate([melody_seq_with_noise, chords], axis=1)
    y = melody_seq
    return np.array(x), np.array(y)

  def add_noise(self, notenums, noiselevel):
    noise_value = scipy.stats.norm.rvs(0, noiselevel, size=len(notenums))
    return [notenums[i] + int(noise_value[i]) if notenums[i] != None 
            else None for i in range(len(notenums))]