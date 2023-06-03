import matplotlib.pyplot as plt
import numpy as np
from .NoteNumMatrix import NoteNumMatrix
from .NoteNumChordVec import NoteNumChordVec

class OutlineAndMatrix(NoteNumMatrix):
  def __init__(self, opts):
    self.pitch_from = opts["pitch_from"]
    self.pitch_thru = opts["pitch_thru"]
    self.interp_level = opts["interp_level"]
    self.smooth_level = opts["smooth_level"]


  def make_xy(self, notenums, chords):
    melody_seq = np.array(self.notenums_to_onehot(notenums))
    outline = self.make_outline(notenums, self.interp_level, self.smooth_level)
#    outline[np.isnan(outline)] = 0.0
#   outline = np.expand_dims(outline, axis=1)
#    self.melody_dim = 1 
    outline_int = [int(nn) if not np.isnan(nn) else None for nn in outline]
    outline_onehot = self.notenums_to_onehot(outline_int)
    chords = np.array(chords)
    x = np.concatenate([outline_onehot, chords], axis=1)
    y = melody_seq
    return np.array(x), np.array(y)

  
  def interpolate_short_rests(self, curve, onsets, offsets, interp_level):
    if onsets[0] < offsets[0]:
      onsets = offsets[1:]
    L = min(len(onsets), len(offsets))
    onsets = onsets[0:L]
    offsets = offsets[0:L]
    rest_dur = onsets - offsets
    for i in range(len(rest_dur)):
      if rest_dur[i] < interp_level:
        self.interpolate(curve, offsets[i], onsets[i])

  def interpolate(self, x, i_from, i_thru):
    LT = i_thru+1 - i_from
    LX = x[i_thru+1] - x[i_from]
    for i in range(i_from+1, i_thru+1):
      dt = i - i_from
      x[i] = x[i_from] + LX * dt / LT

  def extend_values(self, curve, times, direction, length):
    for t in times:
      for i in range(1, length):
        if np.isnan(curve[t + direction * i]):
#          print(direction, curve[t])
          curve[t + direction * i] = curve[t]

  def nan_padding(self, seq, length):
    boundary = np.zeros(length) * np.nan
    return np.concatenate([boundary, seq, boundary])

  def none_to_nan(self, seq, max_num):
    return [x % max_num if x != None else np.nan for x in seq]

  def get_onsets_and_offsets(self, seq):
    seq_hasvalue = np.logical_not(np.isnan(seq)).astype(int)
    seq_hasvalue_diff = np.diff(seq_hasvalue)
    onsets = np.squeeze(np.array(np.where(seq_hasvalue_diff == 1)))
    offsets = np.squeeze(np.array(np.where(seq_hasvalue_diff == -1)))
    return onsets, offsets

  def make_outline(self, notenums, interp_level, smooth_level):
    curve = self.none_to_nan(notenums, NoteNumChordVec.MAX_NUM)
    #curve = [nn % NoteNumChordVec.MAX_NUM if nn != None else np.nan for nn in notenums]
    curve = self.nan_padding(curve, int((smooth_level-1)/2))
    onsets, offsets = self.get_onsets_and_offsets(curve)
    self.extend_values(curve, onsets+1, -1, int((smooth_level-1)/2))
    self.extend_values(curve, offsets, 1, int((smooth_level-1)/2))
    self.interpolate_short_rests(curve, onsets, offsets, interp_level)
    filter = np.ones(smooth_level) / smooth_level
    curve = np.convolve(curve, filter, mode="valid")
    return curve
