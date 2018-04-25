#generate coverage and ebt data for test sampling
import numpy as np
import random
import matplotlib.pyplot as plt
import math

file_name     = 'data/bike_w2v100102D_name.txt';
coverage_file = 'data/sampling/bike_w2v100102D_coverage.txt';
ebt_file      = 'data/sampling/bike_w2v100102D_ebt.txt';
fr  = open(file_name,'r',encoding='utf-8');
fw1 = open(coverage_file,'w',encoding='utf-8');
fw2 = open(ebt_file,'w',encoding='utf-8');

len_file = len(fr.readlines());
sampleNo = len_file;

mu    = [0,2,5];
sigma = [1,1,3];
np.random.seed(0);
coverages = [];
for i in range(0,sampleNo):
    if(i % 2 == 0):
        coverages.append(random.random()/2);
    else:
        coverages.append(random.random());

ebts = [];
s = np.random.normal(0.8, 1, sampleNo)
max = s.max();
min = s.min();
nor = max - min;
for i in range(0,sampleNo):
    ebts.append(abs(math.sin(s[i])));

for i in range(0,sampleNo):
    fw1.write('{:.4f}'.format(coverages[i])+'\n');
    fw2.write('{:.4f}'.format(ebts[i])+'\n');
fw1.close();
fw2.close();    

# plt.subplot(121);
# plt.hist(coverages, 30, normed=True);
# 
# plt.subplot(122);
# plt.hist(ebts, 30, normed=True);
# 
# plt.show();