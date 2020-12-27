import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import IPython
import scipy as sp
from scipy.io import wavfile

fs1, nahravka1 = wavfile.read('maskoff_tone.wav')
nahravka1 = nahravka1[16000:32160]  # 1.01 sec
nahravka1_ramce = []

fs2, nahravka2 = wavfile.read('maskon_tone.wav')
nahravka2 = nahravka2[16000:32160]  # 1.01 sec
nahravka2_ramce = []

# ------------ UKOL 3 ---------------------------------------------------
# NAHRAVKA 1
counter = 0
for i in range(100):
    sublist = []
    for j in range(320):
        helper = nahravka1[j + counter]
        helper -= np.mean(nahravka1)  # ustredneni
        helper /= np.abs(nahravka1).max()  # normalizace
        sublist.append(helper)
    nahravka1_ramce.append(sublist)
    counter += 160

# NAHRAVKA 2
counter = 0
for i in range(100):
    sublist = []
    for j in range(320):
        helper = nahravka2[j + counter]
        helper -= np.mean(nahravka2)  # ustredneni
        helper /= np.abs(nahravka2).max()  # normalizace
        sublist.append(helper)
    nahravka2_ramce.append(sublist)
    counter += 160

ramce2vybrane = nahravka1_ramce[50] + nahravka2_ramce[50]
t = np.arange(len(ramce2vybrane)) / fs1

plt.plot(t, ramce2vybrane)
plt.figure(1)
plt.title('Ramec 1 - maskOFF | Ramec 2 - maskON')
plt.xlabel('time [s]')
plt.ylabel('y')
plt.show()

# ------------ UKOL 4 ---------------------------------------------------
def print_ramec(cislonahravky, cisloramce):
    if cislonahravky == "1":
        ramec_vybrany = nahravka1_ramce[cisloramce]
        t1 = (np.arange(len(ramec_vybrany)) / fs1)
    else:
        ramec_vybrany = nahravka2_ramce[cisloramce]
        t1 = (np.arange(len(ramec_vybrany)) / fs2)

    plt.plot(t1, ramec_vybrany)
    plt.title('Ramec')
    plt.xlabel('time [s]')
    plt.ylabel('y')
    plt.show()

# Center clipping
def clipping(create_graph):
    ramec_clipping = []
    maximum_abs = np.abs(ramec_vybrany).max()
    for i in range (len(ramec_vybrany)):
        if ramec_vybrany[i] > (0.7*maximum_abs):
            ramec_clipping.append(int('1'))
        elif ramec_vybrany[i] < (-0.7*maximum_abs):
            ramec_clipping.append(int('-1'))
        else:
            ramec_clipping.append(int('0'))
            
    if create_graph == True:
        t2 = (np.arange(len(ramec_clipping)) / fs1)
        plt.plot(t2, ramec_clipping)
        plt.title('Centralni klipovani s 70%')
        plt.xlabel('time [s]')
        plt.ylabel('y')
        plt.show()
    return ramec_clipping

# Autokorelace
def autocorrelation_math(ramec_clipping, k):
    ramec_clipping_my = ramec_clipping
    vysledok = 0
    for i in range(len(ramec_clipping_my) - int(k)):
        vysledok += (int(ramec_clipping_my[i]) * int(ramec_clipping_my[i+int(k)]))
    return vysledok

def autocorrelate(ramec_clipping, returnlag, create_graph):
    ramec_clipping_my2 = ramec_clipping
    lag_x = ['0']
    lag_y = ['0']
    prah_x = ['0']
    prah_y = ['0']
    ramec_correlate = []
    for i in range(len(ramec_clipping_my2)):
        ramec_correlate.append(autocorrelation_math(ramec_clipping_my2, i))
        if ((int(ramec_correlate[i]) > int(lag_y[0])) and i > 10):
            lag_y[0] = ramec_correlate[i]
            lag_x[0] = i / fs1
        elif i == 10:
            prah_x[0] = i / fs1
            prah_y[0] = ramec_correlate[0]

    if create_graph == True:  
        t3 = (np.arange(len(ramec_correlate)) / fs1)
        plt.plot(t3, ramec_correlate)
        plt.stem(lag_x, lag_y, linefmt='red', label="Lag")
        plt.stem(prah_x, prah_y, use_line_collection=True, label="Prah")
        plt.title('Autokorelace')
        plt.xlabel('vtime [s]')
        plt.ylabel('y')
        plt.legend()
        plt.show()
        
    if returnlag == True:
        return lag_x[0]*fs1
    else:
        return 0

# Zakladni frekvence
zakladni_frekvence_nahravka1 = []
zakladni_frekvence_nahravka2 = []

for i in range(100):
    ramec_clipping = []
    ramec_vybrany = []
    ramec_vybrany = nahravka1_ramce[i]
    ramec_clipping = clipping(False)
    zakladni_frekvence_nahravka1.append(16000 / autocorrelate(ramec_clipping, True, False))
for i in range(100):
    ramec_clipping = []
    ramec_vybrany = []
    ramec_vybrany = nahravka2_ramce[i]
    ramec_clipping = clipping(False)
    zakladni_frekvence_nahravka2.append(16000 / autocorrelate(ramec_clipping, True, False))
    
t4 = np.arange(len(zakladni_frekvence_nahravka1))
t5 = np.arange(len(zakladni_frekvence_nahravka2))
plt.plot(t4, zakladni_frekvence_nahravka1, color='red', label="bez rousky")
plt.plot(t5, zakladni_frekvence_nahravka2, color='blue', label="s rouskou")
plt.title('Zakladni frekvence ramcu')
plt.xlabel('ramce')
plt.ylabel('y')
plt.legend()
plt.show()
        
print_ramec(1, 50)
ramec_vybrany = nahravka2_ramce[51]
ramec_clipping = clipping(True)
autocorrelate(ramec_clipping, False, True)


 

