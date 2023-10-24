from astropy.io import fits
import scipy.io
import numpy as np
import os
import sys

def get_fits_file(file_path):
    return fits.open(file_path)

def get_info_struct(fits_file, name = None, channel = None):
    header = fits_file[1].header
    S = {}
    if name is None:
        S['Name'] = 'Name'
    else:
        S['Name'] = name
    S['filebase'] = 'filebase'
    if channel is None:
        S['Channel'] = '0'
    else:
        S['Channel'] = channel

    wave0 = header["CRVAL3"]
    dwave = header["CDELT3"]

    data_shape = fits_file[1].data.shape

    S['N'] = data_shape[0]
    S['size'] = data_shape[1:]
    S['lambda_st'] = wave0
    S['dlambda'] = dwave

    return S

def generate_spectrum(S, fits_file, p=0.5, M=None):
    if M is None:
        mask = False
    else:
        mask = True
        X, Y = np.meshgrid(np.arange(1, S.shape[1] + 1), np.arange(1, S.shape[0] + 1))
        x0, y0 = M['center'][0], M['center'][1]
        rad2 = (X - x0)**2 + (Y - y0)**2
        erad2 = M['rad']**2

    # Read data
    data = fits_file[1].data
    data = np.nan_to_num(data)
    N = S['N']
    ymed = np.zeros(S['N'])
    ymean = np.zeros(S['N'])
    imgstack = np.zeros(S['size'])

    not_all_nan = []
    for j in range(N):
        ind = j - 1
        A = data[ind, :, :]

        if mask:
            A[rad2 < erad2] = 0

        imgstack = A + imgstack

        A = A[A != 0]  # Remove zero values
        if len(A) == 0:
            not_all_nan.append(False)
            ymed[j] = 0.
            ymean[j] = 0.
            continue
        ymed[j] = np.quantile(A, p)
        ymean[j] = np.mean(A)
        not_all_nan.append(True)

    imgstack = imgstack / N
    lambda_vals = S['lambda_st'] + S['dlambda'] * np.arange(S['N'])

    return ymed[not_all_nan], ymean[not_all_nan], imgstack, lambda_vals[not_all_nan]

def create_mat(indir, infile, outdir, name):
    # str before '_s3d'
    file_name = infile.split('_s3d')[0]
    file_path = os.path.join(indir, infile)
    fits_file = get_fits_file(file_path)

    outdir = outdir + name + '/'
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    # get channel from infile name
    channels = np.array(['Ch1', 'Ch2', 'Ch3', 'Ch4'])
    channel = channels[[ch.lower() in infile for ch in channels]][0]
    # get band from infile name
    # after the '-' following 'ch' and before the next '_'
    band = infile.split(channel.lower() + '-')[1].split('_')[0]
    # remove 'ch' in channel
    channel = channel[2:] + '_' + band
    S = get_info_struct(fits_file, name, channel)
    p = 0.5 # median
    ymed, ymean, imgstack, lambda_vals = generate_spectrum(S, fits_file, p=p)
    # save as .mat file
    scipy.io.savemat(outdir + file_name + '.mat', {'S':S, 'imgstack': imgstack, 'lambda': lambda_vals, 'ymean': ymean, 'ymed': ymed})

if __name__ == '__main__':
    indir = "data/try_files"
    infile = "jw02151-o007_t007_miri_ch3-shortmediumlong_s3d.fits"
    outdir = 'output/Neon/'
    name = 'MIRI-iras15398-bkg'
    create_mat(indir, infile, outdir, name)
    
