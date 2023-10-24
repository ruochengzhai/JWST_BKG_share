# Some scripts analyzing JWST background field

## data storation

In "data/" directory, there is a directory of fits files, a information csv file, and a file names txt file.

In "output/" directory, there is a info csv file, and output directory store data produced and collected in the target name based directories.

## Add information

Use *add_info.py* to add Galactic coordinates to csv files.

## Analysis

### Analyze fits files

*analyze_single_fits* read a fits file, store name, channel information, etc. to a ".mat" file, along with a stacked image, a wavelength vector, a mean flux vector, and a median flux vector.

*plot_spectra_and_image* plot data in the ".mat" file created.

*analyze_fits* read in a list of fits files, produce ".mat" files, and plot figures.

