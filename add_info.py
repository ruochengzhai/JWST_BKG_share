import numpy as np
import pandas as pd
from astropy import units as u
from astropy.coordinates import SkyCoord

all_csv = pd.read_csv('data/JWST_M83_useful_s3d.csv', comment='#')
chain_csv = all_csv[['filename', 'obslabel', 'targname', 'targprop']].copy()[all_csv['bkg'] ==True]
#chain_csv = pd.read_csv('output/M83.csv', comment='#')

# get 'dyration' from all_csv
duration = []
for i in range(len(chain_csv)):
    filename = chain_csv['filename'][i]
    duration.append(all_csv[all_csv['filename'] == filename]['duration'].values[0])

# prop_ra, prop_dec for chain_csv filename correspongding to all_csv
targ_ra, targ_dec, targ_l, targ_b = [], [], [], []
for i in range(len(chain_csv)):
    filename = chain_csv['filename'][i]
    ra = all_csv[all_csv['filename'] == filename]['targ_ra'].values[0]
    dec = all_csv[all_csv['filename'] == filename]['targ_dec'].values[0]
    # convert ra, dec to l, b
    c = SkyCoord(ra=ra*u.degree, dec=dec*u.degree, frame='icrs')
    l = c.galactic.l.degree
    b = c.galactic.b.degree
    targ_ra.append(ra)
    targ_dec.append(dec)
    targ_l.append(l)
    targ_b.append(b)

# add prop_ra, prop_dec, prop_l, prop_b to chain_csv
# in front of 'NeII', get the index of 'NeII'
index = chain_csv.columns.get_loc('targprop') + 1
chain_csv.insert(index, 'duration', duration)
chain_csv.insert(index+1, 'targ_ra', targ_ra)
chain_csv.insert(index+2, 'targ_dec', targ_dec)
chain_csv.insert(index+3, 'targ_l', targ_l)
chain_csv.insert(index+4, 'targ_b', targ_b)

# save chain_csv
chain_csv.to_csv('output/M83_info.csv', index=False)
