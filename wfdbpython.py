
#!/usr/Anaconda3/python3

import numpy as np
import scipy
import wfdb
from matplotlib import pyplot
#np.set_printoptions(threshold=np.nan)

path = "C:\\Users\\williamadriance\\My Documents\\RobustDetection\\entry\\challenge\\2014\\set-p\\"
import random
readfile = str(random.randint(100,199))

filedir = path+readfile

print("Record number: " + readfile)


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
	m = max(arr)
	return [n*(ran/m) for n in arr]
		
#print(fields)
#arr = np.fft.fft(sig)
#wfdb.plotwfdb(sig, fields, annsamp = annsamp)
sig = sig[:,0]

h = [
    0.000000000000000000,
    -0.000000011245324186,
    -0.000000034529485211,
    -0.000000052734048791,
    -0.000000047478674302,
    0.000000000000000000,
    0.000000107925625857,
    0.000000293042962342,
    0.000000569690731633,
    0.000000948915441402,
    0.000001437654858541,
    0.000002038018882517,
    0.000002746693939173,
    0.000003554494713110,
    0.000004446084088351,
    0.000005399878616277,
    0.000006388152733587,
    0.000007377350381167,
    0.000008328607709128,
    0.000009198485287018,
    0.000009939902774182,
    0.000010503263454775,
    0.000010837750522702,
    0.000010892771636295,
    0.000010619523175670,
    0.000009972640952454,
    0.000008911899964597,
    0.000007403922276185,
    0.000005423849343747,
    0.000002956933206939,
    0.000000000000000000,
    -0.000003437260706241,
    -0.000007331226099166,
    -0.000011643532995295,
    -0.000016320573179747,
    -0.000021293326549746,
    -0.000026477561863906,
    -0.000031774428346415,
    -0.000037071453906663,
    -0.000042243957418221,
    -0.000047156873488270,
    -0.000051666978594010,
    -0.000055625497541764,
    -0.000058881059110905,
    -0.000061282959687534,
    -0.000062684683892679,
    -0.000062947621895446,
    -0.000061944914505111,
    -0.000059565349488373,
    -0.000055717226083616,
    -0.000050332099596059,
    -0.000043368314452681,
    -0.000034814232348420,
    -0.000024691062273079,
    -0.000013055201387705,
    0.000000000000000000,
    0.000014343129689318,
    0.000029804332836321,
    0.000046175720316148,
    0.000063212614669226,
    0.000080635667608300,
    0.000098133866910573,
    0.000115368432947368,
    0.000131977586395364,
    0.000147582149152330,
    0.000161791920506623,
    0.000174212750574550,
    0.000184454213338623,
    0.000192137762725383,
    0.000196905237495444,
    0.000198427564722564,
    0.000196413497745654,
    0.000190618213101742,
    0.000180851582474859,
    0.000166985930473317,
    0.000148963087376258,
    0.000126800548113774,
    0.000100596554843032,
    0.000070533930663553,
    0.000036882506308216,
    0.000000000000000000,
    -0.000039668767060758,
    -0.000081594411144424,
    -0.000125167344591775,
    -0.000169703982452710,
    -0.000214454792226085,
    -0.000258614145001311,
    -0.000301331888234236,
    -0.000341726521704976,
    -0.000378899819642991,
    -0.000411952704341031,
    -0.000440002140613816,
    -0.000462198786996833,
    -0.000477745109424849,
    -0.000485913637053920,
    -0.000486065018628845,
    -0.000477665522026360,
    -0.000460303609924725,
    -0.000433705221474765,
    -0.000397747393782995,
    -0.000352469868254060,
    -0.000298084345537450,
    -0.000234981079004511,
    -0.000163732530222123,
    -0.000085093850515615,
    0.000000000000000000,
    0.000090440631170238,
    0.000184956175848612,
    0.000282124830520872,
    0.000380391930035459,
    0.000478090433809143,
    0.000573464630507758,
    0.000664696797905361,
    0.000749936485740792,
    0.000827332023292406,
    0.000895063791464216,
    0.000951378742787279,
    0.000994625603213457,
    0.001023290148168246,
    0.001036029913191144,
    0.001031707677658084,
    0.001009423049433856,
    0.000968541479554342,
    0.000908720049707534,
    0.000829929401676822,
    0.000732471217113502,
    0.000616990707865768,
    0.000484483641214358,
    0.000336297500111958,
    0.000174126465013312,
    -0.000000000000000001,
    -0.000183735069692312,
    -0.000374438990492098,
    -0.000569209909253271,
    -0.000764920864295362,
    -0.000958262584712915,
    -0.001145791624643203,
    -0.001323983243115866,
    -0.001489288329497687,
    -0.001638193571595051,
    -0.001767283970337369,
    -0.001873306723692067,
    -0.001953235434975247,
    -0.002004333548764209,
    -0.002024215882718083,
    -0.002010907107049783,
    -0.001962896026165342,
    -0.001879184539784815,
    -0.001759330204040926,
    -0.001603481376626673,
    -0.001412404013679447,
    -0.001187499289029564,
    -0.000930811327621779,
    -0.000645024482899086,
    -0.000333449740934257,
    0.000000000000000001,
    0.000350845849318972,
    0.000714089934111828,
    0.001084273200650643,
    0.001455543517738634,
    0.001821733402403889,
    0.002176446503205735,
    0.002513151799044555,
    0.002825284305111426,
    0.003106350925645930,
    0.003350039958504192,
    0.003550332641981533,
    0.003701615042431623,
    0.003798788514208650,
    0.003837376923204856,
    0.003813628813233466,
    0.003724612711751282,
    0.003568303818493447,
    0.003343660397585290,
    0.003050688300181596,
    0.002690492179734741,
    0.002265312124179978,
    0.001778544616729060,
    0.001234746947194005,
    0.000639624425993713,
    -0.000000000000000001,
    -0.000676233870426384,
    -0.001380180944359070,
    -0.002102024139658985,
    -0.002831124999673875,
    -0.003556138736188463,
    -0.004265143633508262,
    -0.004945783346945240,
    -0.005585420394068823,
    -0.006171298923008284,
    -0.006690714652702190,
    -0.007131189718819699,
    -0.007480650029268112,
    -0.007727602637440358,
    -0.007861310581831951,
    -0.007871962619007253,
    -0.007750835294173652,
    -0.007490444850272807,
    -0.007084686572335415,
    -0.006528959298051271,
    -0.005820272996630659,
    -0.004957337524012029,
    -0.003940630900650587,
    -0.002772445725294228,
    -0.001456912630600628,
    0.000000000000000001,
    0.001590510504700172,
    0.003305072713724602,
    0.005132448778236994,
    0.007059805468722887,
    0.009072833008467123,
    0.011155885171895313,
    0.013292139056484348,
    0.015463772635760127,
    0.017652157924417346,
    0.019838067339298156,
    0.022001890625912381,
    0.024123859542940333,
    0.026184277359745978,
    0.028163750126755406,
    0.030043416627384974,
    0.031805173914119626,
    0.033431895370724579,
    0.034907638327092275,
    0.036217838381840575,
    0.037349487758749966,
    0.038291295234049019,
    0.039033825419383772,
    0.039569615466408289,
    0.039893267569145192,
    0.040001515974959490,
    0.039893267569145192,
    0.039569615466408289,
    0.039033825419383772,
    0.038291295234049019,
    0.037349487758749966,
    0.036217838381840575,
    0.034907638327092275,
    0.033431895370724586,
    0.031805173914119626,
    0.030043416627384974,
    0.028163750126755413,
    0.026184277359745989,
    0.024123859542940339,
    0.022001890625912384,
    0.019838067339298160,
    0.017652157924417346,
    0.015463772635760127,
    0.013292139056484348,
    0.011155885171895313,
    0.009072833008467123,
    0.007059805468722885,
    0.005132448778236994,
    0.003305072713724602,
    0.001590510504700172,
    0.000000000000000001,
    -0.001456912630600628,
    -0.002772445725294228,
    -0.003940630900650588,
    -0.004957337524012030,
    -0.005820272996630660,
    -0.006528959298051271,
    -0.007084686572335415,
    -0.007490444850272807,
    -0.007750835294173654,
    -0.007871962619007253,
    -0.007861310581831952,
    -0.007727602637440358,
    -0.007480650029268112,
    -0.007131189718819700,
    -0.006690714652702190,
    -0.006171298923008285,
    -0.005585420394068823,
    -0.004945783346945240,
    -0.004265143633508262,
    -0.003556138736188464,
    -0.002831124999673875,
    -0.002102024139658986,
    -0.001380180944359070,
    -0.000676233870426384,
    -0.000000000000000001,
    0.000639624425993714,
    0.001234746947194005,
    0.001778544616729060,
    0.002265312124179978,
    0.002690492179734741,
    0.003050688300181596,
    0.003343660397585290,
    0.003568303818493447,
    0.003724612711751282,
    0.003813628813233467,
    0.003837376923204858,
    0.003798788514208650,
    0.003701615042431623,
    0.003550332641981533,
    0.003350039958504194,
    0.003106350925645931,
    0.002825284305111426,
    0.002513151799044555,
    0.002176446503205735,
    0.001821733402403889,
    0.001455543517738634,
    0.001084273200650643,
    0.000714089934111828,
    0.000350845849318972,
    0.000000000000000001,
    -0.000333449740934257,
    -0.000645024482899086,
    -0.000930811327621779,
    -0.001187499289029564,
    -0.001412404013679448,
    -0.001603481376626674,
    -0.001759330204040927,
    -0.001879184539784816,
    -0.001962896026165343,
    -0.002010907107049782,
    -0.002024215882718084,
    -0.002004333548764211,
    -0.001953235434975248,
    -0.001873306723692068,
    -0.001767283970337369,
    -0.001638193571595052,
    -0.001489288329497687,
    -0.001323983243115866,
    -0.001145791624643203,
    -0.000958262584712915,
    -0.000764920864295362,
    -0.000569209909253271,
    -0.000374438990492098,
    -0.000183735069692312,
    -0.000000000000000001,
    0.000174126465013312,
    0.000336297500111958,
    0.000484483641214359,
    0.000616990707865768,
    0.000732471217113503,
    0.000829929401676822,
    0.000908720049707534,
    0.000968541479554342,
    0.001009423049433856,
    0.001031707677658085,
    0.001036029913191144,
    0.001023290148168247,
    0.000994625603213456,
    0.000951378742787280,
    0.000895063791464217,
    0.000827332023292406,
    0.000749936485740792,
    0.000664696797905361,
    0.000573464630507758,
    0.000478090433809144,
    0.000380391930035459,
    0.000282124830520872,
    0.000184956175848612,
    0.000090440631170238,
    0.000000000000000000,
    -0.000085093850515615,
    -0.000163732530222123,
    -0.000234981079004511,
    -0.000298084345537450,
    -0.000352469868254060,
    -0.000397747393782995,
    -0.000433705221474765,
    -0.000460303609924725,
    -0.000477665522026360,
    -0.000486065018628845,
    -0.000485913637053920,
    -0.000477745109424849,
    -0.000462198786996834,
    -0.000440002140613816,
    -0.000411952704341032,
    -0.000378899819642991,
    -0.000341726521704976,
    -0.000301331888234236,
    -0.000258614145001311,
    -0.000214454792226085,
    -0.000169703982452710,
    -0.000125167344591775,
    -0.000081594411144424,
    -0.000039668767060758,
    0.000000000000000000,
    0.000036882506308216,
    0.000070533930663553,
    0.000100596554843032,
    0.000126800548113775,
    0.000148963087376258,
    0.000166985930473317,
    0.000180851582474859,
    0.000190618213101743,
    0.000196413497745654,
    0.000198427564722564,
    0.000196905237495444,
    0.000192137762725383,
    0.000184454213338623,
    0.000174212750574550,
    0.000161791920506623,
    0.000147582149152330,
    0.000131977586395364,
    0.000115368432947368,
    0.000098133866910573,
    0.000080635667608300,
    0.000063212614669226,
    0.000046175720316148,
    0.000029804332836321,
    0.000014343129689318,
    0.000000000000000000,
    -0.000013055201387705,
    -0.000024691062273079,
    -0.000034814232348420,
    -0.000043368314452681,
    -0.000050332099596060,
    -0.000055717226083616,
    -0.000059565349488373,
    -0.000061944914505111,
    -0.000062947621895446,
    -0.000062684683892679,
    -0.000061282959687534,
    -0.000058881059110905,
    -0.000055625497541764,
    -0.000051666978594010,
    -0.000047156873488270,
    -0.000042243957418221,
    -0.000037071453906663,
    -0.000031774428346416,
    -0.000026477561863906,
    -0.000021293326549746,
    -0.000016320573179747,
    -0.000011643532995295,
    -0.000007331226099166,
    -0.000003437260706241,
    0.000000000000000000,
    0.000002956933206939,
    0.000005423849343747,
    0.000007403922276185,
    0.000008911899964597,
    0.000009972640952454,
    0.000010619523175670,
    0.000010892771636295,
    0.000010837750522702,
    0.000010503263454775,
    0.000009939902774182,
    0.000009198485287018,
    0.000008328607709128,
    0.000007377350381167,
    0.000006388152733587,
    0.000005399878616277,
    0.000004446084088351,
    0.000003554494713110,
    0.000002746693939173,
    0.000002038018882517,
    0.000001437654858541,
    0.000000948915441402,
    0.000000569690731633,
    0.000000293042962342,
    0.000000107925625857,
    0.000000000000000000,
    -0.000000047478674302,
    -0.000000052734048791,
    -0.000000034529485211,
    -0.000000011245324186,
    0.000000000000000000,
]

sig = normalize_array(sig, 1.2)

sig_avg = sum(sig)/len(sig)
print("average: ", sig_avg)

sig = [n-sig_avg for n in sig]

threshold = (sum([abs(number) for number in sig])/len(sig))
arr = [0.3 if n > threshold or n < -1*threshold else 0 for n in sig]

annnew = []
count = 0
print(len(annsamp))
for i in range(len(sig)):
	if count < len(annsamp) and annsamp[count] == i:
		annnew.append(0.2)
		count += 1
	else:
		annnew.append(0)
		
'''
gapsum = 0
for a in range(len(arr)-1):
	gapsum += abs(arr[a+1]-arr[a])

print("average gap: ", gapsum/(len(arr)-1))'''
pyplot.plot(sig)
#pyplot.plot(array_power(sig, 20))
#pyplot.plot(arr)
#pyplot.plot(annnew)
#pyplot.plot(abs_array_power(sig, 3))

#summ = max(sig)
#transformed = np.convolve(array_derivative([100*(n/summ)*n for n in sig],1),h)
#pyplot.plot(transformed)

pyplot.show()


