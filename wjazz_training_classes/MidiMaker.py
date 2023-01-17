import pretty_midi
import numpy as np

class MidiMaker: 
  def __init__(self, xy_maker, opts):
    self.xy_maker = xy_maker
    self.div = opts["division"]
    self.pitch_from = opts["pitch_from"]

  def make_midi(self, y, x, filename):
    melody = self.xy_maker.get_melody_elements(y)
    melody1 = melody[:, 0:self.xy_maker.pitch_range]
    melody2 = melody[:, self.xy_maker.pitch_range:2*self.xy_maker.pitch_range]
    chords = self.xy_maker.get_chord_elements(x)
    midi = pretty_midi.PrettyMIDI(resolution=480)
    midi.instruments.append(
        self.make_note_msgs(melody1, melody2, 1, self.pitch_from, 100))
    midi.instruments.append(
        self.make_note_msgs(chords, np.zeros(chords.shape), self.div, 48, 60))
    midi.write(filename)
    return melody, chords

  def make_note_msgs(self, pianoroll, pianoroll2, reso, pitch_from, velocity):
    instr = pretty_midi.Instrument(program=1)
    for i in range(pianoroll.shape[0]):
      if (i % reso == 0):
        for j in range(pianoroll.shape[1]):
          if pianoroll[i, j] <= 0.5 and pianoroll2[i, j] > 0.5:
            if i >= 1 and pianoroll2[i-1, j] < 0.5 and pianoroll[i-1, j] < 0.5:
              pianoroll[i, j] += pianoroll2[i, j]
              pianoroll2[i, j] = 0
          if pianoroll[i, j] > 0.5:
            dur = 1
            for k in range(i+1, pianoroll.shape[0]):
              if pianoroll2[k, j] > 0.5:
                dur += 1
#                pianoroll2[k, j] = 0
              else:
                break
            instr.notes.append(pretty_midi.Note(start=i / self.div / 2, 
                                                end=(i+dur) / self.div / 2, 
                                                pitch=pitch_from+j, 
                                                velocity=velocity))
    return instr