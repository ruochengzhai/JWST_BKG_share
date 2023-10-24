import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from analyze_single_fits import create_mat
from plot_spectra_and_image import plot_spectra_image

dir_name = 'M83'

csv_file = pd.read_csv('output/%s_info.csv'%dir_name)
infiles = csv_file['filename']
filenames = np.array([f.split('_s3d')[0] for f in infiles])
names = csv_file['targname']
# for elements not having targname, use obslabel
names = np.where(names == 'nan', csv_file['obslabel'], names)

datadir = 'data/%s_files/'%dir_name
args = [os.path.exists(os.path.join(datadir, f)) for f in infiles]
infiles = infiles[args]
filenames = filenames[args]
names = names[args]
# use '_' to replace ' ' in names
names = [obs.replace(' ', '_') for obs in names]

for i in range(len(filenames)):
    outdir = 'output/%s/'%dir_name
    create_mat(datadir, infiles[i], outdir, names[i])
    plot_spectra_image(outdir, filenames[i] + '.mat', names[i])
    plt.close()
    print('Done with ' + filenames[i])
