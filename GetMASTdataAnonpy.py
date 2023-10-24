import numpy as np
import ftplib
import os
import sys

ftps = ftplib.FTP_TLS('archive.stsci.edu')
ftps.login(user='anonymous',passwd='anonymous')
ftps.prot_p() # This is a really good idea :)
ftps.cwd('stage')
dir='anonymous/anonymous_20231012Z_0d17d268'
# stagedir is something like 'anonymous/anonyumous12345'
ftps.cwd(dir)
#filenames = ftps.nlst()
filenames = np.loadtxt('data/NGC6720_filenames.txt', dtype=str)
# filenames with 'ch' in the name
filenames = filenames[['ch' in f for f in filenames]]

out_path='data/NGC6720_files/'
#localdir='C:\\Users\\Chas\\Documents\\ngst\\Fomalhaut\\'
#localdir='D:\\JWSTData\\WISE1828\\'
#os.chdir(localdir) #chdir used for change direcotry

i = 0
num_files = len(filenames)
for filename in filenames:
    i += 1 
    if os.path.exists(out_path + filename):
        print("skipping " + filename)
        continue
    print("getting " + filename)
    with open(out_path + filename, 'wb') as fp: 
        ftps.retrbinary('RETR {}'.format(filename), fp.write)
    print("file " + str(i) + " of " + str(num_files) + " done")