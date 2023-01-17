import numpy as np
import scipy
from sklearn.model_selection import train_test_split

class MatrixDataSet:
  def __init__(self, ds, xy_maker, opts):
    self.n_beats = opts["n_beats"]
    self.division = opts["division"]
    self.n_measures = opts["n_measures"]
    self.max_sects = opts["max_sects"]
    self.oct_shift = opts["oct_shift"]
    self.pitch_from = opts["pitch_from"]
    self.pitch_thru = opts["pitch_thru"]
    x_all = []
    y_all = []
    attr_all = []
    n_steps = int(self.n_measures * self.n_beats * self.division)
    for id in ds.melid_list:
      nn, chd = ds.zeropadding(ds.notenums[id], ds.chords[id], n_steps)
      for oct in range(-self.oct_shift, self.oct_shift+1):
        nn_oct = ds.move_octave(nn, oct)
        if ds.lowest_notenum(nn_oct) >= self.pitch_from and \
           ds.highest_notenum(nn_oct) < self.pitch_thru:
          x, y = xy_maker.make_xy(nn_oct, chd)
          for k in range(1, self.max_sects+1):
            if x.shape[0] >= k * n_steps:
              x_all.append(x[(k-1)*n_steps : k*n_steps, :])
              y_all.append(y[(k-1)*n_steps : k*n_steps, :])
              attr_all.append({"id": id, "k": k, "oct": oct})
    self.x_all = np.array(x_all)
    self.y_all = np.array(y_all)
    self.attr_all = attr_all
    self.x_train, self.x_test, self.y_train, self.y_test, \
      self.attr_train, self.attr_test = \
      self.split_train_test(self.x_all, self.y_all, self.attr_all)
    self.x_train4d = self.reshape3to4(self.x_train)
    self.x_test4d = self.reshape3to4(self.x_test)
    self.y_train4d = self.reshape3to4(self.y_train)
    self.y_test4d = self.reshape3to4(self.y_test)
  
  @staticmethod
  def split_train_test(x_all, y_all, attr_all):
    i_train, i_test = train_test_split(range(len(x_all)),
                                       test_size=int(len(x_all)/2),
                                       shuffle=False)
    x_train = x_all[i_train]
    x_test = x_all[i_test]
    y_train = y_all[i_train]
    y_test = y_all[i_test]
    attr_train = [attr_all[i] for i in i_train]
    attr_test = [attr_all[i] for i in i_test]
    return x_train, x_test, y_train, y_test, attr_train, attr_test

  @staticmethod
  def reshape3to4(x):
    x = np.array(x)
    return np.reshape(x, (x.shape[0], x.shape[1], x.shape[2], 1))
 
  @staticmethod
  def reshape4to3(x):
    x = np.array(x)
    return np.reshape(x, (x.shape[0], x.shape[1], x.shape[2]))