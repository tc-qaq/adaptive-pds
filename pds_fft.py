import cv2 as cv  
import scipy
import numpy as np  
from matplotlib import pyplot as plt

img = cv.imread('plot-ori.png', 0);
f = np.fft.fft2(img); #get frequence  
fshift = np.fft.fftshift(f); # remove to center
fimg = np.log(np.abs(fshift)); # fft abs to A

img1 = cv.imread('plot-pps.png', 0);
f1 = np.fft.fft2(img1); #get frequence  
fshift1 = np.fft.fftshift(f1); # remove to center
fimg1 = np.log(np.abs(fshift1)); # fft abs to A

# display
plt.subplot(231), plt.imshow(img, 'gray'), plt.title('ori');
plt.subplot(232), plt.imshow(fimg, 'gray'), plt.title('FFT');

plt.subplot(234), plt.imshow(img1, 'gray'), plt.title('samlers');
plt.subplot(235), plt.imshow(fimg1, 'gray'), plt.title('FFT');


plt.show();