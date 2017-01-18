
#!/usr/Anaconda3/python3

import numpy as np
from scipy import signal
import scipy
import wfdb
from matplotlib import pyplot
import random
#np.set_printoptions(threshold=np.nan)

path = "C:\\Users\\williamadriance\\My Documents\\RobustDetection\\entry\\challenge\\2014\\"

use_setp = False

if use_setp:
	path += "set-p\\"
else:
	path += "training\\"


import os
arr = os.listdir(path)
files = [arr[i] for i in range(1,len(arr),3)]
readfile = random.choice(files)
filedir = path + readfile

filedir = filedir[:len(filedir)-4]




print("Record number: " + readfile[:len(readfile)-4])


sig, fields = wfdb.rdsamp(filedir, channels=[0])

annsamp=wfdb.rdann(filedir, 'atr')[0]
#print("annsamp: ", annsamp)
#print(fields)

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
	ann = [a for a in ann if a > 0]
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

sigavg = np.mean(sig)

'''
highpass
h = [
    0.000000000000000000,
    0.000000688079373601,
    0.000002799557647008,
    0.000006390551560924,
    0.000011495910890062,
    0.000018126769350187,
    0.000026267561437421,
    0.000035872511549462,
    0.000046861621172260,
    0.000059116199713020,
    0.000072474004268640,
    0.000086724072775932,
    0.000101601353133805,
    0.000116781247565362,
    0.000131874206265455,
    0.000146420516850878,
    0.000159885445927178,
    0.000171654895884503,
    0.000181031743564161,
    0.000187233027486367,
    0.000189388146751443,
    0.000186538227444618,
    0.000177636801383594,
    0.000161551927417890,
    0.000137069867363280,
    0.000102900407250769,
    0.000057683890175337,
    0.000000000000000000,
    -0.000071621694078304,
    -0.000158689453091544,
    -0.000262735397209543,
    -0.000385299934112298,
    -0.000527914705930231,
    -0.000692084206327874,
    -0.000879266250649455,
    -0.001090851511652298,
    -0.001328142360632854,
    -0.001592331278134224,
    -0.001884479119383697,
    -0.002205493536662410,
    -0.002556107873532196,
    -0.002936860853878784,
    -0.003348077391791147,
    -0.003789850846180116,
    -0.004262027036626731,
    -0.004764190324213116,
    -0.005295652043088243,
    -0.005855441545411769,
    -0.006442300094346390,
    -0.007054677807265955,
    -0.007690733814729550,
    -0.008348339760535652,
    -0.009025086724880636,
    -0.009718295606928426,
    -0.010425030955632788,
    -0.011142118189159209,
    -0.011866164094479255,
    -0.012593580450421860,
    -0.013320610570433083,
    -0.014043358516278881,
    -0.014757820691663238,
    -0.015459919485929847,
    -0.016145538603326588,
    -0.016810559683336460,
    -0.017450899792844816,
    -0.018062549351871984,
    -0.018641610041614874,
    -0.019184332236881665,
    -0.019687151504839816,
    -0.020146723718398579,
    -0.020559958345475915,
    -0.020924049494716185,
    -0.021236504323685609,
    -0.021495168446835116,
    -0.021698248017147887,
    -0.021844328196858394,
    -0.021932387778338173,
    0.978038190234480798,
    -0.021932387778338173,
    -0.021844328196858394,
    -0.021698248017147887,
    -0.021495168446835120,
    -0.021236504323685613,
    -0.020924049494716185,
    -0.020559958345475915,
    -0.020146723718398579,
    -0.019687151504839819,
    -0.019184332236881669,
    -0.018641610041614881,
    -0.018062549351871991,
    -0.017450899792844816,
    -0.016810559683336460,
    -0.016145538603326591,
    -0.015459919485929849,
    -0.014757820691663238,
    -0.014043358516278880,
    -0.013320610570433083,
    -0.012593580450421865,
    -0.011866164094479258,
    -0.011142118189159210,
    -0.010425030955632787,
    -0.009718295606928426,
    -0.009025086724880638,
    -0.008348339760535652,
    -0.007690733814729546,
    -0.007054677807265956,
    -0.006442300094346392,
    -0.005855441545411768,
    -0.005295652043088247,
    -0.004764190324213121,
    -0.004262027036626734,
    -0.003789850846180116,
    -0.003348077391791147,
    -0.002936860853878787,
    -0.002556107873532196,
    -0.002205493536662408,
    -0.001884479119383697,
    -0.001592331278134225,
    -0.001328142360632854,
    -0.001090851511652299,
    -0.000879266250649456,
    -0.000692084206327874,
    -0.000527914705930231,
    -0.000385299934112298,
    -0.000262735397209543,
    -0.000158689453091545,
    -0.000071621694078304,
    0.000000000000000000,
    0.000057683890175337,
    0.000102900407250769,
    0.000137069867363281,
    0.000161551927417890,
    0.000177636801383594,
    0.000186538227444618,
    0.000189388146751443,
    0.000187233027486367,
    0.000181031743564161,
    0.000171654895884503,
    0.000159885445927178,
    0.000146420516850878,
    0.000131874206265456,
    0.000116781247565362,
    0.000101601353133805,
    0.000086724072775932,
    0.000072474004268640,
    0.000059116199713020,
    0.000046861621172260,
    0.000035872511549462,
    0.000026267561437421,
    0.000018126769350187,
    0.000011495910890062,
    0.000006390551560924,
    0.000002799557647008,
    0.000000688079373601,
    0.000000000000000000,
]
'''
#bandpass first try
h = [
	-0.000000000000000004,
    0.000000000000000006,
    0.000000000001797150,
    0.000000000029288704,
    0.000000000190634088,
    0.000000000773181814,
    0.000000002318789327,
    0.000000005597090258,
    0.000000011395199381,
    0.000000020088545403,
    0.000000031048419486,
    0.000000042056271477,
    0.000000048991687646,
    0.000000046088866380,
    0.000000026971261953,
    -0.000000013538914075,
    -0.000000077148377579,
    -0.000000159990424237,
    -0.000000251537292263,
    -0.000000335351729788,
    -0.000000392170404971,
    -0.000000405177299625,
    -0.000000366509856686,
    -0.000000283268949257,
    -0.000000180853556360,
    -0.000000101562925569,
    -0.000000097235965681,
    -0.000000216174231551,
    -0.000000486453823880,
    -0.000000899533830705,
    -0.000001399305466424,
    -0.000001881957190641,
    -0.000002211025471337,
    -0.000002249829831559,
    -0.000001910544150660,
    -0.000001216066221815,
    -0.000000368336347882,
    0.000000184555347944,
    -0.000000310102345058,
    -0.000002953800200907,
    -0.000009223819035383,
    -0.000020983491152616,
    -0.000040478938066300,
    -0.000070327239471426,
    -0.000113501224488192,
    -0.000173314812324166,
    -0.000253410441166769,
    -0.000359066398490777,
    -0.000505623444285444,
    -0.000705395709095397,
    -0.000954161077505681,
    -0.001227737488073425,
    -0.001488890960401580,
    -0.001704969926537052,
    -0.001872097865992825,
    -0.002037209693954834,
    -0.002306582519753216,
    -0.002830719808861126,
    -0.003761565655991918,
    -0.005188372193827253,
    -0.007070294662199777,
    -0.009192444176393347,
    -0.011172907360887260,
    -0.012538065856947243,
    -0.012862884894286813,
    -0.011946566689071580,
    -0.009970627702774099,
    -0.007575841201471001,
    -0.005804089340557301,
    -0.005882785277746301,
    -0.008877273719747208,
    -0.015287480081774316,
    -0.024702199131372796,
    -0.035632398617423344,
    -0.045615490605609710,
    -0.051618571801048660,
    -0.050684898951649737,
    -0.040687678880294939,
    -0.021003925893932150,
    0.007082064096143736,
    0.040384785870624343,
    0.074276309989355860,
    0.103524450406299873,
    0.123332139181715025,
    0.130337310755906405,
    0.123332139181714151,
    0.103524450406299651,
    0.074276309989356443,
    0.040384785870624294,
    0.007082064096143519,
    -0.021003925893932171,
    -0.040687678880295022,
    -0.050684898951649737,
    -0.051618571801048493,
    -0.045615490605609654,
    -0.035632398617423428,
    -0.024702199131372803,
    -0.015287480081774347,
    -0.008877273719747213,
    -0.005882785277746256,
    -0.005804089340557315,
    -0.007575841201471037,
    -0.009970627702774099,
    -0.011946566689071590,
    -0.012862884894286813,
    -0.012538065856947203,
    -0.011172907360887246,
    -0.009192444176393340,
    -0.007070294662199762,
    -0.005188372193827235,
    -0.003761565655991908,
    -0.002830719808861123,
    -0.002306582519753225,
    -0.002037209693954839,
    -0.001872097865992830,
    -0.001704969926537065,
    -0.001488890960401599,
    -0.001227737488073427,
    -0.000954161077505687,
    -0.000705395709095405,
    -0.000505623444285442,
    -0.000359066398490770,
    -0.000253410441166763,
    -0.000173314812324166,
    -0.000113501224488186,
    -0.000070327239471416,
    -0.000040478938066294,
    -0.000020983491152622,
    -0.000009223819035388,
    -0.000002953800200903,
    -0.000000310102345064,
    0.000000184555347935,
    -0.000000368336347881,
    -0.000001216066221805,
    -0.000001910544150655,
    -0.000002249829831568,
    -0.000002211025471342,
    -0.000001881957190641,
    -0.000001399305466427,
    -0.000000899533830712,
    -0.000000486453823883,
    -0.000000216174231545,
    -0.000000097235965682,
    -0.000000101562925578,
    -0.000000180853556364,
    -0.000000283268949256,
    -0.000000366509856688,
    -0.000000405177299636,
    -0.000000392170404987,
    -0.000000335351729787,
    -0.000000251537292264,
    -0.000000159990424251,
    -0.000000077148377585,
    -0.000000013538914072,
    0.000000026971261951,
    0.000000046088866375,
    0.000000048991687648,
    0.000000042056271483,
    0.000000031048419485,
    0.000000020088545398,
    0.000000011395199378,
    0.000000005597090263,
    0.000000002318789325,
    0.000000000773181808,
    0.000000000190634088,
    0.000000000029288708,
    0.000000000001797154,
    -0.000000000000000002,
    -0.000000000000000002,
]

'''
h = [
    0.000000000000000009,
    -0.000000000000000007,
    0.000000000000824876,
    0.000000000007516328,
    0.000000000034646442,
    0.000000000109987953,
    0.000000000272611191,
    0.000000000562224803,
    0.000000000998608491,
    0.000000001553036020,
    0.000000002117102018,
    0.000000002477538398,
    0.000000002307519565,
    0.000000001184740788,
    -0.000000001356375303,
    -0.000000005736756948,
    -0.000000012215550227,
    -0.000000020759507847,
    -0.000000030923214130,
    -0.000000041770267735,
    -0.000000051866475329,
    -0.000000059370579488,
    -0.000000062235436596,
    -0.000000058513626669,
    -0.000000046738489400,
    -0.000000026328233428,
    0.000000002058277897,
    0.000000036295295976,
    0.000000072771180354,
    0.000000106634833295,
    0.000000132330532714,
    0.000000144396196708,
    0.000000138445759700,
    0.000000112204275173,
    0.000000066424628330,
    0.000000005497076121,
    -0.000000062425170391,
    -0.000000125915738806,
    -0.000000171434412764,
    -0.000000185108181389,
    -0.000000154972204375,
    -0.000000073399373658,
    0.000000060639473027,
    0.000000239889078202,
    0.000000448094434307,
    0.000000660586984875,
    0.000000846377589967,
    0.000000971789141210,
    0.000001005461371602,
    0.000000924357284233,
    0.000000720222609667,
    0.000000405823312289,
    0.000000020232490608,
    -0.000000367530786588,
    -0.000000657091143045,
    -0.000000717923591913,
    -0.000000393320760625,
    0.000000493004291264,
    0.000002128062725535,
    0.000004699080068659,
    0.000008382074314880,
    0.000013330320561199,
    0.000019663462715455,
    0.000027457907691584,
    0.000036738944031515,
    0.000047474792675039,
    0.000059572555010513,
    0.000072875804796233,
    0.000087163403927670,
    0.000102149026900684,
    0.000117480864034273,
    0.000132741036458497,
    0.000147444383478882,
    0.000161036454134247,
    0.000172890724018576,
    0.000182305239615103,
    0.000188499042543709,
    0.000190608828442547,
    0.000188885138851698,
    0.000184743134675090,
    0.000177138952024997,
    0.000162137729395384,
    0.000133123344955533,
    0.000081919013316255,
    0.000000700160605005,
    -0.000115627397939504,
    -0.000267090230112167,
    -0.000446965131144902,
    -0.000641363316092335,
    -0.000830551827811997,
    -0.000992200647745617,
    -0.001106345489741991,
    -0.001161400555392344,
    -0.001160130194700163,
    -0.001124196966931124,
    -0.001095845627339811,
    -0.001135529780140631,
    -0.001314860976059344,
    -0.001705111832694377,
    -0.002362515811515092,
    -0.003312595371492050,
    -0.004536501207973744,
    -0.005962647054256441,
    -0.007466617438203977,
    -0.008881345646024608,
    -0.010017968550062064,
    -0.010695763241539608,
    -0.010777476586767441,
    -0.010204566978684118,
    -0.009025789869753689,
    -0.007412506728155509,
    -0.005655265838719181,
    -0.004138573699925086,
    -0.003294099092232481,
    -0.003536366361746320,
    -0.005188684078762423,
    -0.008409945430065853,
    -0.013134411915215288,
    -0.019036214915258545,
    -0.025527920303000679,
    -0.031798273858696414,
    -0.036888690775267782,
    -0.039801959723407346,
    -0.039630953830423366,
    -0.035690843070887990,
    -0.027636197827157722,
    -0.015544972012315467,
    0.000045242958048204,
    0.018157445599129907,
    0.037453144439584682,
    0.056361037239039576,
    0.073241995481018646,
    0.086570183884070340,
    0.095107168398225014,
    0.098046162967344364,
    0.095107168398224376,
    0.086570183884070201,
    0.073241995481019229,
    0.056361037239039624,
    0.037453144439584377,
    0.018157445599130011,
    0.000045242958048306,
    -0.015544972012315403,
    -0.027636197827157594,
    -0.035690843070887858,
    -0.039630953830423379,
    -0.039801959723407235,
    -0.036888690775267574,
    -0.031798273858696352,
    -0.025527920303000672,
    -0.019036214915258497,
    -0.013134411915215256,
    -0.008409945430065832,
    -0.005188684078762355,
    -0.003536366361746289,
    -0.003294099092232495,
    -0.004138573699925055,
    -0.005655265838719128,
    -0.007412506728155473,
    -0.009025789869753654,
    -0.010204566978684073,
    -0.010777476586767420,
    -0.010695763241539563,
    -0.010017968550062000,
    -0.008881345646024583,
    -0.007466617438203958,
    -0.005962647054256413,
    -0.004536501207973715,
    -0.003312595371492035,
    -0.002362515811515077,
    -0.001705111832694364,
    -0.001314860976059343,
    -0.001135529780140624,
    -0.001095845627339810,
    -0.001124196966931116,
    -0.001160130194700151,
    -0.001161400555392332,
    -0.001106345489741990,
    -0.000992200647745609,
    -0.000830551827811984,
    -0.000641363316092331,
    -0.000446965131144905,
    -0.000267090230112163,
    -0.000115627397939494,
    0.000000700160605009,
    0.000081919013316256,
    0.000133123344955539,
    0.000162137729395395,
    0.000177138952024995,
    0.000184743134675084,
    0.000188885138851701,
    0.000190608828442551,
    0.000188499042543711,
    0.000182305239615100,
    0.000172890724018584,
    0.000161036454134260,
    0.000147444383478878,
    0.000132741036458491,
    0.000117480864034277,
    0.000102149026900686,
    0.000087163403927676,
    0.000072875804796227,
    0.000059572555010515,
    0.000047474792675048,
    0.000036738944031513,
    0.000027457907691577,
    0.000019663462715455,
    0.000013330320561205,
    0.000008382074314879,
    0.000004699080068656,
    0.000002128062725537,
    0.000000493004291269,
    -0.000000393320760627,
    -0.000000717923591919,
    -0.000000657091143043,
    -0.000000367530786585,
    0.000000020232490609,
    0.000000405823312283,
    0.000000720222609670,
    0.000000924357284244,
    0.000001005461371602,
    0.000000971789141206,
    0.000000846377589970,
    0.000000660586984883,
    0.000000448094434311,
    0.000000239889078200,
    0.000000060639473038,
    -0.000000073399373646,
    -0.000000154972204367,
    -0.000000185108181385,
    -0.000000171434412757,
    -0.000000125915738798,
    -0.000000062425170385,
    0.000000005497076123,
    0.000000066424628338,
    0.000000112204275182,
    0.000000138445759701,
    0.000000144396196707,
    0.000000132330532719,
    0.000000106634833302,
    0.000000072771180361,
    0.000000036295295973,
    0.000000002058277898,
    -0.000000026328233421,
    -0.000000046738489396,
    -0.000000058513626668,
    -0.000000062235436585,
    -0.000000059370579472,
    -0.000000051866475309,
    -0.000000041770267721,
    -0.000000030923214110,
    -0.000000020759507821,
    -0.000000012215550209,
    -0.000000005736756939,
    -0.000000001356375292,
    0.000000001184740794,
    0.000000002307519567,
    0.000000002477538390,
    0.000000002117102018,
    0.000000001553036031,
    0.000000000998608482,
    0.000000000562224786,
    0.000000000272611182,
    0.000000000109987952,
    0.000000000034646436,
    0.000000000007516317,
    0.000000000000824871,
    -0.000000000000000003,
    0.000000000000000009,
]
'''
SLICES = 10
sig = np.convolve(sig, h)[(len(h)-1)//2:]
#sig = [abs(n) for n in sig]
#slices = [[]]

for i in range(SLICES):
	#sig = 
	i=0
	#tempc is used to prevent two predictions from being too close
	tempc = -999
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


		sample_shift = 0
		shaving_off = 0.05
		maxx = temp[ind]
		for q in range(len(temp)):
			c = i+q+sample_shift
			if c<len(windowing_result_plotform):
				#here I shave off a certain number of samples that are within range of the max and see if the difference from the last beat is greater than a specified number
				if temp[q] >= (1-shaving_off)*maxx and c-tempc>0:
					windowing_result_plotform[c] = 2.9

					tempc = c


					#The actual predictions:
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


avg = [2*sigavg for n in range(len(sig))]

#print(signal.butter(4, 0.5, 'low'))



'''
transformed = sig
#print("FFT:\n", np.fft.fft(sig))
length = len(sig)
mx_sig = max(sig)
mx_trans = max(transformed)
pyplot.plot([0 if n<length else sig[n-length] for n in range(2*length)], 'blue')
pyplot.plot(transformed, 'red')

'''
pyplot.plot(windowing_result_plotform, 'yellow')
pyplot.plot(windows_plotted, 'red')
pyplot.plot(ann_to_plot(sig, annsamp, 2), 'magenta')
pyplot.plot(arr)
pyplot.plot(sig)
#pyplot.plot(avg, 'green')

'''
Below is example of Fast Fourier Transform from scipy>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
'''
'''
N = 600
# sample spacing
T = 1.0 / 800.0
x = np.linspace(0.0, N*T, N)
y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(200.0 * 2.0*np.pi*x)
yf = scipy.fftpack.fft(y)
print(yf)
xf = np.linspace(0.0, 1.0/(2.0*T), N/2)

fig, ax = pyplot.subplots()
ax.plot(xf, 2.0/N * np.abs(yf[:N//2]))
'''
'''
End of example>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
'''

pyplot.show()


