import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import itertools
from sklearn import preprocessing
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import seaborn as sn


with open('FinalList.csv','r') as csv_file:
    lines = csv_file.readlines()

Name = []
DXO = []
CPU = []
GPU= []
MEM= []
UX = []
Total = []
Pric = []
for line in lines:
    data = line.split(',')
    Name.append(data[0])
    DXO.append(data[1])
    CPU.append(data[2])
    GPU.append(data[3])
    MEM.append(data[4])
    UX.append(data[5])
    Total.append(data[6])
    Pric.append(data[7])

Price = [x.replace('\n', '').replace(' ', '') for x in Pric]

Name.pop(0)
CPU.pop(0)
DXO.pop(0)
GPU.pop(0)
MEM.pop(0)
UX.pop(0)
Total.pop(0)
Price.pop(0)

aCPU = []
aGPU = []
aUX = []
aMEM = []
aDXO = []
aTotal = []
aPrice = []






for i in range(0, len(CPU)):
    CPU[i] = int(CPU[i])
aCPU = CPU.copy()
amin, amax = min(CPU), max(CPU)
for i, val in enumerate(CPU):
    CPU[i] = (val-amin) / (amax-amin)

for i in range(0, len(GPU)):
    GPU[i] = int(GPU[i])
amin, amax = min(GPU), max(GPU)
for i, val in enumerate(GPU):
    GPU[i] = (val-amin) / (amax-amin)
aGPU = GPU.copy()

for i in range(0, len(MEM)):
    MEM[i] = int(MEM[i])
aMEM = MEM.copy()
amin, amax = min(MEM), max(MEM)
for i, val in enumerate(MEM):
    MEM[i] = (val-amin) / (amax-amin)

for i in range(0, len(UX)):
    UX[i] = int(UX[i])
aUX=UX.copy()
amin, amax = min(UX), max(UX)
for i, val in enumerate(UX):
    UX[i] = (val-amin) / (amax-amin)

for i in range(0, len(Total)):
    Total[i] = int(Total[i])
aTotal = Total.copy()
amin, amax = min(Total), max(Total)
for i, val in enumerate(Total):
    Total[i] = (val-amin) / (amax-amin)

for i in range(0, len(Price)):
    Price[i] = int(Price[i])
aPrice = Price.copy()
amin, amax = min(Price), max(Price)
for i, val in enumerate(Price):
    Price[i] = (val-amin) / (amax-amin)

for i in range(0, len(DXO)):
    DXO[i] = int(DXO[i])
aDXO = DXO.copy()
amin, amax = min(DXO), max(DXO)
for i, val in enumerate(DXO):
    DXO[i] = (val-amin) / (amax-amin)
 

print("NORMALIZZED DATA")
print(Name)
print()
print(DXO)
print()
print(CPU)
print()
print(GPU)
print()
print(UX)
print()
print(MEM)
print()
print(Total)
print()
print(Price)


def Average(lst):
    return sum(lst) / len(lst)


Davg = Average(DXO)
Uavg = Average(UX)
Cavg = Average(CPU)
Mavg = Average(MEM)
Gavg = Average(GPU)

print("AVERAGE")
print(Davg)
print(Uavg)
print(Cavg)
print(Mavg)
print(Gavg)

gmean = (Davg+Uavg+Mavg+Gavg+Cavg)/5
print()
print("GMEAN")
print (gmean)

k= 5

def Subtract(lst):
    b = Average(lst)
    c = []
    for i in range(len(lst)):
        a =(lst[i] - b)
        a = a*a
        c.append(a)
    return c
    
Dsub = Subtract(DXO)
Usub = Subtract(UX)
Csub = Subtract(CPU)
Msub = Subtract(MEM)
Gsub = Subtract(GPU)

print()
print()
print("SUM OF SUBTRACTIONS")
Dsum = sum(Dsub)
Usum = sum(Usub)
Csum = sum(Csub)
Msum = sum(Msub)
Gsum = sum(Gsub)

print(Dsum)
print(Usum)
print(Csum)
print(Msum)
print(Gsum)

Grandsum = Dsum+Usum+Csum+Msum+Gsum
print()
print("Total Sum")
print(Grandsum)

big = []
big.append(aDXO)
big.append(aUX)
big.append(aCPU)
big.append(aMEM)
big.append(aGPU)
print()

print()
print()
plt.boxplot(big)
plt.xticks([1,2,3,4,5],['DXO', 'UX', 'CPU', 'MEM','GPU'])

df = pd.DataFrame(big)
df = df.transpose()
df.columns = ['DXO', 'UX', 'CPU', 'MEM','GPU']
#print (df)
plt.show()
fvalue, pvalue = stats.f_oneway(df['DXO'], df['UX'], df['CPU'], df['MEM'], df['GPU'])
print("FVALUE AND PVALUE")
print(fvalue, pvalue)
print()

print()
print()
d_melt = pd.melt(df.reset_index(), id_vars=['index'], value_vars=['DXO', 'UX', 'CPU', 'MEM','GPU'])
d_melt.columns = ['index', 'treatments', 'value']
model = ols('value ~ C(treatments)', data=d_melt).fit()
print("SUMMARY")
model.summary()

anova_table = sm.stats.anova_lm(model, typ=2)
anova_table
print (anova_table)
print()
print()
print()
m_comp = pairwise_tukeyhsd(endog=d_melt['value'], groups=d_melt['treatments'], alpha=0.10)
print(m_comp)


plt.bar(aPrice,aTotal)
plt.ylabel("TOTAL BENCHMARK")
plt.xlabel("PRICE")

plt.show()
plt.bar(aDXO,aPrice)
plt.xlabel("CAMERA RATING")
plt.ylabel("PRICE")
plt.show()

print()
print()

core = df.corr()
print("CORRELATION")
print(core)
print()
print()

sn.heatmap(core, annot=True)
plt.show()
