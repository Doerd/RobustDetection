
#!/usr/Anaconda3/python3

import numpy as np
from scipy import signal
import scipy
import wfdb
from matplotlib import pyplot
import random
#np.set_printoptions(threshold=np.nan)

path = "C:\\Users\\williamadriance\\My Documents\\RobustDetection\\entry\\challenge\\2014\\"

use_setp = True

if use_setp:
	path += "set-p\\"
	readfile = str(random.randint(100,199))
	readfile = "169"
else:
	path += "training\\"
	readfile = "1071"
	
	
filedir = path+readfile

print("Record number: " + readfile)


sig, fields = wfdb.rdsamp(filedir, channels=[0])
annsamp=wfdb.rdann(filedir, 'atr')[0]
#print("annsamp: ", annsamp)
print(fields)

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

def array_derivative(arr, order):
	if order==0:
		return arr
	else:
		ret = []
		for i in range(len(arr)-1):
			ret.append(arr[i+1]-arr[i])
		return array_derivative(ret, order-1)
	
def array_power(arr, power):
	return [n**power for n in arr]

def abs_array_power(arr, power):
	return [abs(n**power) for n in arr]

def normalize_array(arr, ran):
	m = max(arr) if max(arr) > abs(min(arr)) else abs(min(arr))
	return [n*(ran/m) for n in arr]

def ann_to_plot(sig, ann, height):
	annnew = []
	count = 0
	for i in range(len(sig)):
		if count < len(ann) and ann[count] == i:
			annnew.append(height)
			count += 1
		else:
			annnew.append(0)
	return annnew

sig = sig[:,0]





'''
sig_avg = sum(sig)/len(sig)
print("average: ", sig_avg)

sig = [n-sig_avg for n in sig]

avg_arr = [sig_avg for n in range(len(sig))]


threshold = (sum([abs(number) for number in sig])/len(sig))
my_guess = [0.3 if n > threshold or n < -1*threshold else 0 for n in sig]
'''

###########
#  Start  #
#   of    #
#  window #
###########

def max_index(arr):
	index = 0
	for i in range(len(arr)):
		if arr[i]>arr[index]:
			index = i
	return index

init_window_width = 200
window_width = init_window_width

windowing_result_plotform = [0]*len(sig)
windows_plotted = []

ann_guess = []
arrays_windows = []



arr = sig
#sig = [abs(n) for n in sig]
#sig = np.convolve(sig, h)

sigavg = sum(sig)/len(sig)

i=0
while i<len(sig):
	if window_width < 150:
		window_width = 150
	if window_width > 500:
		window_width = 270
	windows_plotted.append(0.1)
	for j in range(window_width-1):
		windows_plotted.append(0)
	temp = sig[i:i+window_width]
	ind = max_index(temp)
	
	
	sample_shift = 2
	shaving_off = 0.05
	maxx = temp[ind]
	for q in range(len(temp)):
		c = i+q+sample_shift
		if c<len(windowing_result_plotform):
			if temp[q] >= (1-shaving_off)*maxx and temp[q] > sigavg:
				windowing_result_plotform[c] = 2.9
				if len(ann_guess) > 1 and abs(ann_guess[len(ann_guess)-1]-c)>2:
					ann_guess.append(c)
			else:
				windowing_result_plotform[c] = 0
	
	
	window_width += (ind-window_width//2)
	i += window_width
	
###########
#  	End   #
#   of    #
#  window #
###########	


avg = [sigavg for n in range(len(sig))]

#print(signal.butter(4, 0.5, 'low'))

h = [
	0.01 for n in range(0,100)
]
transformed = np.convolve(sig,h)
print("FFT:\n", np.fft.fft(sig))
length = len(sig)
mx_sig = max(sig)
mx_trans = max(transformed)
#pyplot.plot([0 if n<length else sig[n-length] for n in range(2*length)], 'blue')
#pyplot.plot(transformed, 'red')
#pyplot.plot(arr)

#pyplot.plot(windowing_result_plotform, 'yellow')
#pyplot.plot(windows_plotted, 'red')
#pyplot.plot(ann_to_plot(sig, annsamp, 2), 'magenta')

#pyplot.plot(avg, 'green')

'''
Below is example of Fast Fourier Transform from scipy>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
'''

N = 600
# sample spacing
T = 1.0 / 800.0
x = np.linspace(0.0, N*T, N)
y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
yf = scipy.fftpack.fft(y)
xf = np.linspace(0.0, 1.0/(2.0*T), N/2)

fig, ax = pyplot.subplots()
ax.plot(xf, 2.0/N * np.abs(yf[:N//2]))

'''
End of example>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
'''

pyplot.show()


