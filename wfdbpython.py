import wfdb
import numpy as np
np.set_printoptions(threshold=np.nan)
dirrr = "/Users/williamadriance/Programs/Python/RobustDetection/entry/sources/set-p/100"
sig, fields = wfdb.rdsamp(dirrr)
annsamp=wfdb.rdann(dirrr, 'atr')[0]
sig = [row[0] for row in sig]
temp = np.around(sig,2)
print([row[0] for row in temp])
wfdb.plotwfdb(sig, fields, annsamp)