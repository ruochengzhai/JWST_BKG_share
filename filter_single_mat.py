import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter, filtfilt
from scipy.io import loadmat
import sys
import os
from plot_spectra_and_image import get_lines

def Ffilter(h, filters, outdir, Name, Channel, line, diagnostic):
    n = len(h)
    x = np.arange(1, n + 1)

    # Remove mean (2nd order polynomial)
    p = np.polyfit(x, h, 2)
    hq = np.polyval(p, x)
    hp = h - hq

    plt.figure(10)
    plt.subplot(2, 1, 1)
    plt.plot(x, h, '-k', label='data')
    # if not plt.gca().get_children():
    #     plt.hold(True)
    plt.plot(x, hq, '-r', label='baseline')
    # plt.hold(False)
    plt.xlabel('bin')
    plt.legend()
    plt.title(line)

    plt.subplot(2, 1, 2)
    plt.plot(x, hp, '-k', label='baseline subtracted')
    plt.xlabel('bin')
    plt.legend(loc = 'upper right')

    if diagnostic:
        plt.savefig(outdir + Name + '_Ch' + Channel + '_' + line + '_FourierFiltering_Fig1.png')

    # Fourier filtering
    plt.figure(11)
    H = np.fft.fft(hp)
    plt.plot(x, np.abs(H))
    for filter in filters:
        filter_low, filter_high = filter
        if filter_low < 1:
            filter_low = 1
        if filter_high > n//2 + 1:
            filter_high = n//2 + 1
        H[filter_low:filter_high] = 0
    # plt.hold(True)
    plt.plot(x, np.abs(H), '-r')
    plt.xlim([1, n//2 + 1])
    # plt.hold(False)
    plt.xlabel('frequency')
    plt.title(line)

    if diagnostic:
        plt.savefig(outdir + Name + '_Ch' + Channel + '_' + line + '_FourierFiltering_Fig2.png')

    # Inverse transform
    H[n - 1:n//2-1:-1] = np.conj(H[1:n//2+1])
    hf = np.real(np.fft.ifft(H))

    # Dirty beam
    x = np.ones_like(hf)
    for filter in filters:
        filter_low, filter_high = filter
        if filter_low < 1:
            filter_low = 1
        if filter_high > n//2 + 1:
            filter_high = n//2 + 1
        x[filter_low:filter_high] = 0
    x[n - 1:n//2:-1] = np.conj(x[1:n//2])

    X = np.fft.ifft(x)
    nshift = 20
    X = np.roll(X, nshift) / np.sum(X * X.conj())

    #str = f'nlow={nlow} nhigh={nhigh}'
    str = f'filters = {filters}'

    if diagnostic:
        plt.figure(13)
        plt.plot(X, '-k', linewidth=1.5)
        plt.title(f'dirty beam: {line}')
        plt.ylim(-0.3, 0.9)
        plt.grid(True, which='minor')
        plt.ylabel('Amplitude')
        plt.xlabel('bin')
        plt.legend([str])
        plt.savefig(outdir + Name + '_Ch' + Channel + '_' + line + '_FourierFiltering_Fig3.png')

    return hq, hp, hf, X, nshift

def filter_mat(dir_path, infile):
    file_path = os.path.join(dir_path, infile)
    filename = (file_path.split('/')[-1]).split('.')[0]
    data = loadmat(file_path)
    Name = data['S']['Name'][0][0][0]
    Channel = data['S']['Channel'][0][0][0]
    lambda_vals = data['lambda'].flatten()
    ymed_values = data['ymed'].flatten()

    diagnostic = False

    # Create and open a file for writing
    with open(dir_path + filename + '.dat', 'w') as fid:
        wavelengths, lines, _ = get_lines(lambda_vals)
        if len(wavelengths) == 0:
            print('No lines in range.')
            return False
        for i in range(len(wavelengths)):

            # Load data (replace this with your data loading mechanism)
            # Load data from .mat file

            ind = np.where(lambda_vals > wavelengths[i])[0]
            if len(ind) == 0:
                print('species not in channel')
                continue

            ind = ind[0]
            hwidth = 100
            filters = [[1,3], [hwidth - 4, hwidth + 1]]
            print('hwidth = ', hwidth)
            while True:
                hwindow_low = ind - hwidth - 1
                hwindow_high = ind + hwidth - 1
                if ind - hwidth - 1 < 0:
                    hwindow_low = 0
                if ind + hwidth - 1 > len(ymed_values):
                    hwindow_high = len(ymed_values)    
                h = ymed_values[hwindow_low : hwindow_high]
                n = len(h)
                lam = lambda_vals[hwindow_low : hwindow_high]
                # if n is odd, remove the last element
                if n % 2 == 1:
                    h = h[:-1]
                    lam = lam[:-1]
                    n -= 1
                hq, hp, hf, Xp, nshift = Ffilter(h, filters, dir_path, Name, Channel, lines[i], diagnostic)

                # Create a figure for plotting (simplified saving)
                plt.figure(4)
                xl = [min(lam), max(lam)]
                plt.plot(lam, hf, '-k', linewidth=1.5)
                plt.xlim(xl)
                plt.title(lines[i])
                plt.axvline(wavelengths[i], linestyle=':', color='r', linewidth=2)
                plt.ylabel('$I_\\nu\\,({\\rm MJy\\,sr^{-1}}$)', fontsize=16)
                plt.xlabel('$\\lambda\\,(\\mu$m)', fontsize=16)
                #plt.gca().set_aspect('equal', adjustable='box')
                plt.gca().tick_params(width=2)
                plt.legend([f'filters = {filters}'], frameon=False)
                plt.savefig(dir_path + Name + '_Ch' + Channel + '_filtered_' + lines[i] + '.png')

                # Continue with calculations
                y = lfilter(np.roll(Xp, -nshift), 1, hf)
                maxy = np.real(np.max(y[n // 2 - 3 : n // 2 + 3]))
                y = np.delete(y, np.s_[n // 2 - 3 : n // 2 + 3])
                yrms = np.real(np.sqrt(np.mean(y ** 2)))

                print(f'{lines[i]} {maxy:.2f} {yrms:.2f}')

                if diagnostic:
                    plt.figure(5)
                    plt.plot(y, '-k', linewidth=1.5)
                    plt.ylabel('$I_\\nu\\,({\\rm MJy\\,sr^{-1}}$)', fontsize=16)
                    plt.xlabel('$\\lambda\\,(\\mu$m)', fontsize=16)
                    plt.gca().set_aspect('equal', adjustable='box')
                    plt.gca().tick_params(width=2)
                    plt.title(f'convolved with dirty beam: {lines[i]}')
                    plt.legend([f'rms={yrms:.2f}'], frameon=False)
                    plt.savefig(dir_path + Name + '_Ch' + Channel + lines[i] + '_conv' + '.png')
            
                plt.show()

                # User input for nlow and nhigh
                # input [filter_low_1 filter_high_1], [filter_low_2 filter_high_2], ...
                user_input = input('Enter filter pairs in the format "[filter_low_1 filter_high_1], [filter_low_2 filter_high_2], ...": ')

                if not user_input:
                    break

                while True:
                    try:
                        # Split the input into individual filter pairs
                        filter_pairs = user_input.split(', ')
                        filters = []

                        for pair in filter_pairs:
                            low, high = map(int, pair.strip('[]').split())
                            filters.append([low, high])
                    except:
                        print('Format Error, please try again.')
                        user_input = input('Enter filter pairs in the format "[filter_low_1 filter_high_1], [filter_low_2 filter_high_2], ...": ')
                        continue
                    break

            # Write data to the file
            fid.write(f'{lines[i]} ${maxy:.2f} \\pm {yrms:.2f}$\n')

    open(dir_path + 'Done_files.txt', 'a').write(infile + '\n')
    return True

if __name__ == '__main__':
    dir_path = 'output/M83/M-83-Background/'
    infile = 'jw02219-o005_t006_miri_ch3-short_s3d.mat'
    filter_mat(dir_path, infile)

