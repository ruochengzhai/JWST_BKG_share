import matplotlib.pyplot as plt
import numpy as np
import scipy.io
import os

# read .mat file
def read_mat_file(file_path):
    mat_file = scipy.io.loadmat(file_path)
    S = mat_file['S']
    # S to dict
    S = {field: S[field][0, 0] for field in S.dtype.names}
    S['Name'] = S['Name'][0]
    S['filebase'] = S['filebase'][0]
    S['Channel'] = S['Channel'][0]
    S['size'] = S['size'][0]
    S['N'] = S['N'][0]
    S['lambda_st'] = S['lambda_st'][0]
    S['dlambda'] = S['dlambda'][0]
    return S, mat_file['ymed'].flatten(), mat_file['ymean'].flatten(), mat_file['imgstack'], mat_file['lambda'].flatten()

def get_lines(lambda_vals):
    wavelengths = np.array([12.813548, 15.5551, 6.985274, 8.99138, 21.8302, 18.713, 10.5105])
    lines = np.array(['NeII', 'NeIII', 'ArII', 'ArIIIa', 'ArIIIb', 'SIII', 'SIV'])
    lamwidth = np.array([0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05])
    # choose lines in lambda_vals range
    args = (wavelengths > lambda_vals[0]) & (wavelengths < lambda_vals[-1])
    return wavelengths[args], lines[args], lamwidth[args]

def display_spectra(lambda_vals, ymed, ymean, S, outdir, pltflag=True):
    wavelengths, lines, lamwidth = get_lines(lambda_vals)
    if len(wavelengths) == 0:
        print('No lines in range')
        return False

    # Create figure 1
    plt.figure(1)
    plt.clf()
    if pltflag:
        plt.semilogy(lambda_vals, ymed, '-k', linewidth=1.5)
    else:
        plt.plot(lambda_vals, ymed, '-k', linewidth=1.5)
    
    for i in range(len(wavelengths)):
        plt.axvline(x=wavelengths[i], linestyle=':', color='k')

    plt.xlim([lambda_vals[0], lambda_vals[-1]])
    # yl = plt.ylim()
    # l = 13.67
    # r = 13.25
    # plt.fill_betweenx([yl[0], yl[1]], r, l, color='0.8', alpha=0.1)

    # l = 15.8
    # r = 15.3
    # plt.fill_betweenx([yl[0], yl[1]], r, l, color='0.8', alpha=0.1)

    plt.xlabel(r'$\lambda\,(\mu)$m', fontsize=16)
    plt.ylabel(r'$B_\nu\,(\mathrm{MJy\,sr^{-1}})$', fontsize=16)
    #plt.gca().set_aspect('equal', adjustable='box')
    #plt.title('Channel 3')
    plt.tick_params(axis='both', labelsize=16, width=2)
    plt.tight_layout()
    plt.savefig(outdir + S['Name'] + '_Ch' + S['Channel'] + '_FullSpectrum.png', bbox_inches='tight')

    for i in range(len(wavelengths)):
        plt.figure(2 + i)
        plt.clf()
        plt.plot(lambda_vals, ymed, '-k', linewidth=1.5)
        plt.plot(lambda_vals, ymean, '--r')

        plt.xlim(wavelengths[i] + lamwidth[i] * np.array([-3, 3]))
        # ylim based on ymean and ymed in x range
        # enlarge by 5% on both sides
        args = (lambda_vals > plt.xlim()[0]) & (lambda_vals < plt.xlim()[1])
        ymin = min(np.min(ymed[args]), np.min(ymean[args]))
        ymax = max(np.max(ymed[args]), np.max(ymean[args]))
        yl = (ymin - 0.05 * (ymax - ymin), ymax + 0.05 * (ymax - ymin))
        plt.ylim(yl)

        plt.axvline(x=wavelengths[i], linestyle=':', color='k')
        plt.xlabel(r'$\lambda\,(\mu)$m', fontsize=16)
        plt.ylabel(r'$B_\nu\,(\mathrm{MJy\,sr^{-1}})$', fontsize=16)
        plt.legend(['median', 'mean'], frameon=False, loc='upper left')
        plt.title('[' + lines[i] + ']')
        plt.tick_params(axis='both', labelsize=16, width=2)
        #plt.gca().set_aspect('equal', adjustable='box')
        plt.tight_layout()
        plt.savefig(outdir + S['Name'] + '_Ch' + S['Channel'] + '_' + lines[i] +'.png', bbox_inches='tight')
    return True

def display_image(imgstack, S, outdir):
    try:
        plt.figure(plt.gcf().number + 1)
    except:
        plt.figure(1)
    plt.clf()

    plt.imshow(imgstack, cmap='bone', aspect='auto', interpolation='none')
    plt.clim()  # Adjust the color limits as needed

    plt.colorbar()

    plt.title('Channel ' + S['Channel'])

    plt.tight_layout()
    plt.savefig(outdir + S['Name'] + '_Ch' + S['Channel'] + '_Stack.png', bbox_inches='tight')

def plot_spectra_image(dir_path, infile, name):
    dir_path = dir_path + name + '/'
    file_path = os.path.join(dir_path, infile)
    filename = (file_path.split('/')[-1]).split('.')[0]
    S, ymed, ymean, imgstack, lambda_vals = read_mat_file(file_path)
    if not display_spectra(lambda_vals, ymed, ymean, S, dir_path):
        return
    display_image(imgstack, S, dir_path)

if __name__ == '__main__':
    dir_path = 'output/M83/'
    name = 'M-83-Background'
    infile = 'jw02219-o005_t006_miri_ch3-short_s3d.mat'
    plot_spectra_image(dir_path, infile, name)
    plt.show()
