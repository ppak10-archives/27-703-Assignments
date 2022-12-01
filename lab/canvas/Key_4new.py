# -*- coding: utf-8 -*-
"""
 Created on Mon Apr 04 09:15:44 2020
@author: Amaranth
"""
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 21:58:44 2020

@author: Amaranth
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 19:03:44 2020

@author: Amaranth
"""
import time 
import os
import xlsxwriter
path = '/Users/ak/Downloads/Image_test'# Path for the images 
import numpy as np
import Lock_4new as h
from datetime import datetime
import matplotlib.pyplot as plt


begin = time.time()
row = 0
column = 0
files = os.listdir(path)
abcd= [' ' for k in range (len(files)) ]
Thick_table = np.zeros(len(files))
mean_intercept = np.zeros(len(files))
mean_inv_intercept=np.zeros(len(files))
mean_in=np.zeros(len(files))
frac=np.zeros(len(files))

workbook = xlsxwriter.Workbook('T.xlsx') 
worksheet = workbook.add_worksheet()

# distance in pixel on the scale bar
distance_in_pixel=187   
#distance mentioned on the scale bar in um
distance_in_micrometer=10
for i in range(len(files)):
    dateTimeObj = datetime.now()
    #Text file name for storing the variable details    
    Variable_name='Ak_run_3' 
#Type of adaptive thresholding to be applied. Choose from cv2.ADAPTIVE_THRESH_MEAN_C or cv2.ADAPTIVE_THRESH_GAUSSIAN_C
    Thresholding="cv2.ADAPTIVE_THRESH_GAUSSIAN_C"
    
#Angle step size to facilitate the degree of rotation.    
    ang_size=180
#Median Filter size to be used
    median_filter=3
#Adaptive thresholding filter size to be used
    adpt_thresh_filter=11
#Adaptive thresholding block constant to be subtracted
    adpt_thresh_const=1.5
#Denoise filter h, denoise template window size and denoise search window size 
    DeNoise_h,DeNoise_template_window_size,DeNoise_search_window_size=2,3,3
# kernal size to be used by morphological filters
    kernal_a,kernal_b=3,3
# Small object : Remove objects smaller than the specified size.
    small_objects_min_size=2
# Small holes : Remove contiguous holes smaller than the specified size.
    small_holes_connectivity,small_holes_area_threshold=1,64 #64 is default
    nlm,counts,bins,img1_blur,dst,c, d,distance, Inv_distance = h.measure_lath(path+'/'+files[i],ang_size) # number defines the angle of rotation
    sum_distance=[]
    sum_ind=[]
    avg_beta=[]
    sum_distance1=[]
    sum_ind1=[]
    
    for j in range (len(distance)):
        sum_distance1=sum_distance1+distance[j]
    for k in range (len(Inv_distance)):
        sum_ind1=sum_ind1+Inv_distance[k]   
    sum_distance1=np.array(sum_distance1)	
    

    sum_ind1=np.array(sum_ind1)
    for t in range (len(sum_ind1)):
        if (sum_ind1[t] < 1):
            sum_ind.append(sum_ind1[t])
    for w in range (len(sum_distance1)):
        if (sum_distance1[w] > 1):
            sum_distance.append(sum_distance1[w])
    sum_distance=np.array(sum_distance)	
    sum_ind=np.array(sum_ind)   
    avgdist=np.mean(sum_distance)
    avgind=np.mean(sum_ind)
    plt.figure(figsize=(10,10), dpi=300)
    plt.title(str(files[i]))
    plt.imshow(dst)
    plt.savefig(str(files[i]),dpi= 300 ,format='Tif') #bbox_inches='tight',transparent=True, pad_inches=0
    Thickness=0.67/avgind
    Thick_um=(Thickness*distance_in_micrometer)/distance_in_pixel # the number in the denominator is the distance in pixels from imageJ (Analyse --> Set scale) while the number in numerator is the distance on scale (orginal image scale)
    Thick_table[i] = Thick_um
    mean_intercept[i]=((avgdist*distance_in_micrometer)/distance_in_pixel)#5-171;10-187(5000x)
    #mean_inv_intercept[i]=((InvLamda*186)/10)
    mean_in[i]=((avgind*distance_in_pixel)/distance_in_micrometer)
    #abcd[i]=' '.join(files[i],Thick_table[i])
    frac[i]=c
    sum_distance=(sum_distance*distance_in_micrometer)/distance_in_pixel
    sum_ind=(sum_ind*distance_in_pixel)/distance_in_micrometer
    plt.figure(figsize=(10,10))
    plt.title('Intercept_'+str(files[i]))
    plt.hist(sum_distance, cumulative=True, bins = 100,density = True,  histtype='step',range= ((min(sum_distance)-0.5),(max(sum_distance)+0.5))) 
    plt.xlabel('Intercepts (um)')
    plt.ylabel('Cumulative Frequency')
    plt.savefig('Intercept_'+str(files[i]),dpi= 300 , format='Tif')
    
    plt.figure(figsize=(10,10))
    plt.title('Inverse Intercept_'+str(files[i]))
    plt.hist(sum_ind,bins=100, cumulative=True , density=True, histtype='step',range= ((min(sum_ind)-0.5),(max(sum_ind)+0.5)))
    plt.xlabel('Inverse Intercepts (1/um)')
    plt.ylabel('Cumulative Frequency')
    plt.savefig('Inverse Intercept_'+str(files[i]),dpi= 300 , format='Tif')
	
    abcd[i]=abcd.append(files[i]+'~'+str(mean_intercept[i])+'~'+str(mean_in[i])+'~'+str(frac[i])+'~'+str(Thick_table[i])+'~'+str(dateTimeObj))
    print("The Thickness in um is :",Thick_um)
    print("The file name is:",files[i])
    print(dateTimeObj)
	
print(Thick_table)
# Printing the information to the text file that will contain all the parameters.
Variables = open("Variables_"+Variable_name+" .txt", "w")
Variables.write("Distance in pixels - "+str(distance_in_pixel)+"\n"+"Distance in micrometer scale on SEM image - "+str(distance_in_micrometer)+"\n"+"Threshold_Type - "+Thresholding+"\n"+"Angle Step Size - "+str(ang_size)+"\n"+"Median Blur - "+str(median_filter)+ "\n"+"Adaptive threshold - "+str(adpt_thresh_filter)+","+str(adpt_thresh_const)+"\n"+"Kernal Size - "+"("+str(kernal_a)+","+str(kernal_b)+")"+"\n"+"Denoise - "+"("+str(DeNoise_h)+","+str(DeNoise_template_window_size)+","+str(DeNoise_search_window_size)+")"+"\n"+"Small Objects minimum size - "+str(small_objects_min_size)+"\n"+"Small Holes connectivity - "+str(small_holes_connectivity)+"\n"+"Small Holes area_threshold - "+str(small_holes_area_threshold))
Variables.close()


for i in abcd:
    worksheet.write(row, column, i) 
    row += 1
workbook.close()
time.sleep(1)
end = time.time()
print (f"Total runtime of the program is {end-begin}")