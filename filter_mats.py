import numpy as np
import os
import glob
from filter_single_mat import filter_mat

def get_names(dir_path):
    # read directory names in dir_path
    names = os.listdir(dir_path)
    names = [os.path.basename(obs) for obs in names]
    return names

def get_infiles(dir_path):
    # read filenames in dir_path ending with *.mat
    infiles = glob.glob(dir_path + '*.mat')
    infiles = [os.path.basename(infile) for infile in infiles]

    try:
        done_files = np.loadtxt(dir_path + 'Done_files.txt', dtype=str)
    except:
        done_files = []

    infiles = [f for f in infiles if f not in done_files]
    return infiles

if __name__ == '__main__':
    dir_path = 'output/M83/'
    names = get_names(dir_path)
    for name in names:
        print('----- Working on ' + name + ' -----')
        infiles = get_infiles(dir_path + name + '/')
        for infile in infiles:
            if not filter_mat(dir_path + name + '/', infile):
                continue
