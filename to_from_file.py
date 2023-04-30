import pickle

def write_to_file(file,frames):
    f = open(file,'wb')
    pickle.dump(frames,f)
    f.close()

def read_from_file(file):
    f = open(file,'rb')
    frames = pickle.load(f)
    f.close()
    return frames