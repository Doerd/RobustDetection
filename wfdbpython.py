
#!/usr/Anaconda3/python3

import numpy as np
import scipy
import wfdb
#np.set_printoptions(threshold=np.nan)

path = "C:\\Users\\williamadriance\\My Documents\\RobustDetection\\entry\\challenge\\2014\\set-p\\"
readfile = "122"

filedir = path+readfile



sig, fields = wfdb.rdsamp(filedir, channels=[0])
annsamp=wfdb.rdann(filedir, 'atr')[0]
#print("annsamp: ", annsamp)

sig_train = []
sig_test = []
ann_train = []
ann_test = []

from time import time
'''
t0 = time()
for i in range(0, 80):
	sig_train.append(wfdb.rdsamp(path+str(100+i), channels=[0])[0])
	ann_train.append(wfdb.rdann(path+str(100+i), 'atr')[0])[0]
for i in range(80, 100):
	sig_test.append(wfdb.rdsamp(path+str(100+i), channels=[0])[0])
	ann_test.append(wfdb.rdann(path+str(100+i), 'atr')[0])
t1 = time()
print("time taken for array creation: ", str(t1-t0)[:5], "seconds")'''

#print("train: ", trainann)
#print("test: ", testann)

def array_derivative(arr):
	ret = []
	for i in range(len(arr)):
		


#print(fields)
arr = np.fft.fft(sig)
wfdb.plotwfdb(sig, fields, annsamp = annsamp)
wfdb.plotwfdb(arr, fields)
#wfdb.plotwfdb(sig, fields, annsamp = trainann[3])

