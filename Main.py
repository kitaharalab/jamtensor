from wjazz_training_classes import *
import os
import pickle

def run():

    opts = {"n_beats": 4, "division": 4, "n_measures": 24, "max_sects" : 16, 
        "oct_shift": 1, "pitch_from": 36, "pitch_thru": 96, "noise_level": 0}

    dir = "./"

    db = DBReader(dir + "wjazzd.db")
    mel_chd = FramewiseMelodyChordSet(db, ["BLUES"], opts)
    nn_chd = NoteNumChordVec(mel_chd)
    with open(dir + "wjazzd_data_div4.bin", "wb") as p:
        pickle.dump({"db": db, "mel_chd": mel_chd, "nn_chd": nn_chd}, p)


    #smooth_levelは奇数
    opts.update({"interp_level": 0, "smooth_level": opts["division"]*2+1})
    with open(dir + "wjazzd_data_div4.bin", "rb") as p:
        data = pickle.load(p)
        db = data["db"]
        mel_chd = data["mel_chd"]
        nn_chd = data["nn_chd"]
    outline_maker = OutlineAndMatrix(opts)
    mat = MatrixDataSet(nn_chd, outline_maker, opts)

    def dump_data(data, filename):
        with open(filename, "wb") as p:
            pickle.dump(data, p)

    def start_experiment(mat, opts, result_dir):
        os.makedirs(result_dir, exist_ok=True)
        with open(result_dir + "/config.txt", "w") as f:
            f.write(str(opts))
        model = MyModel(mat.x_train4d[0].shape, mat.y_train4d[0].shape, opts)
        model.fit(mat.x_train4d, mat.y_train4d, mat.x_test4d, mat.y_test4d)
        model.save(result_dir + "mymodel")
        y_pred = model.predict(mat.x_test4d)
        dump_data(mat, result_dir + "/mat.dat")
        dump_data(mat.x_train, result_dir + "/x_train.dat")
        dump_data(mat.x_test, result_dir + "/x_test.dat")
        dump_data(mat.y_train, result_dir + "/y_train.dat")
        dump_data(mat.y_test, result_dir + "/y_test.dat")
        dump_data(y_pred, result_dir + "/y_pred.dat")
        dump_data(mat.attr_train, result_dir + "/attr_train.dat")
        dump_data(mat.attr_test, result_dir + "/attr_test.dat")

        os.makedirs(result_dir + "/mid/", exist_ok=True)
        midimaker = MidiMaker(outline_maker, opts)
        for i in range(len(mat.x_test)):
            melody, chords = midimaker.make_midi(mat.y_test[i], mat.x_test[i], result_dir + ("/mid/test%04d_corr.mid" % i))
            melody, chords = midimaker.make_midi(y_pred[i], mat.x_test[i], result_dir + ("/mid/test%04d_pred.mid" % i))

    opts.update({"hidden_dim": 512, "winsize": 4})
    start_experiment(mat, opts, dir + "/20221206/data/")


if __name__ == "__main__":
    run()


