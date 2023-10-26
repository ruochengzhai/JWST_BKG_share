# Some scripts analyzing JWST background field

## Data Storation

In "data/" directory, there is a directory of fits files, a information csv file, and a file names txt file.

In "output/" directory, there is a info csv file, and output directory store data produced and collected in the target name based directories.

## Add Information

Use **add_info.py**(https://github.com/ruochengzhai/JWST_BKG_share/blob/main/add_info.py) to add Galactic coordinates to csv files.

## Analysis

### Analyze fits Files

**analyze_single_fits.py** read a fits file, store name, channel information, etc. to a ".mat" file, along with a stacked image, a wavelength vector, a mean flux vector, and a median flux vector.

**plot_spectra_and_image.py** plot data in the ".mat" file created.

**analyze_fits.py** read in a list of fits files, produce ".mat" files, and plot figures.

When analyzing a single fits file, please use **analyze_single_fits.py** and **plot_spectra_and_image.py**. If many fits files need to be analyzed, please first store their information in a csv file. Then use **analyze_fits.py** to analyze them together. Output files will be classified by the target names automatically.

### Fourier Filtration

**filter_single_mat.py** use fast Fourier transformation to filter the median flux vector around emission lines to remove periodical signals in spetra. Users can change the filtration windows on the frequencies to reach the best perfomance.

**filter_mats.py** filters a list of ".mat" files.

## Cubeviz Preview

**Cubeviz** is a visualization and analysis toolbox for data cubes from integral field units (IFUs). Please refer to https://jdaviz.readthedocs.io/en/latest/cubeviz/index.html.

**try.ipynb** can interactively use Cubeviz to show the spectra from fits files in a certain directory.

