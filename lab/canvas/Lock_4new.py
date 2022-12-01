# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 21:43:38 2020

@author: Amaranth
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 10:04:10 2020

@author: mattw
"""
from scipy.ndimage.interpolation import rotate
import numpy as np
import matplotlib.pyplot as plt
import cv2
from skimage.restoration import denoise_nl_means, estimate_sigma #, denoise_bilateral
from skimage import morphology
from matplotlib_scalebar.scalebar import ScaleBar
def measure_lath(file,ang_step):

    #img = Image.open(file).convert('L') # converting to grayscale
    img11 = cv2.imread(file,0)
    img11_arr = np.array(img11)     
    plt.figure(figsize=(10,10))
    plt.title('Primary Image')
    plt.imshow(img11_arr)
    plt.savefig('primary_img.Tif', format='Tif')
    plt.colorbar()
    plt.show()
    Height_1=0#6-Univ.of Manchester
    width_1=0
    width_2= 1280#1024-Univ.of Manchester;1024-rjlee
    Height_2=960#1024-Univ.of Manchester;1030-rjlee
    img1= img11[Height_1:Height_2,width_1:width_2]
    img1_arr=np.array(img1)
    hyp=(((img1_arr.shape[0])**(2))+((img1_arr.shape[1])**(2)))**(0.5)
    print(hyp)
    plt.figure(figsize=(10,10))
    plt.title('Cropped Image')
    plt.imshow(img1_arr)
    plt.savefig('Cropped_img.Tif', format='Tif')
    plt.colorbar()
    plt.show()
    print (img1_arr)
    max_value = np.max(img1_arr)
    min_value = np.min(img1_arr)
    img1_inv = ~img1_arr  # invert B&W img=-img if we have to calculate the white spacings ---> use img = ~img for alpha lath thickness and img =img for beta thickness
    plt.hist(img1_inv.flat, bins=100, range=(0,255))
    print (max_value)
    print (min_value)
    sigma_est=np.mean(estimate_sigma(img1_inv, multichannel = True))
    nlm=denoise_nl_means(img1_inv,h=1.15*sigma_est,fast_mode=True,patch_size=5,patch_distance=3,multichannel=False,preserve_range=True).astype('uint8')
    plt.figure(figsize=(10,10))
    plt.title('Skde')
    plt.imshow(nlm)
    plt.savefig('Skde_img.Tif', format='Tif')
    plt.colorbar()
    plt.show()
    counts,bins,mm=plt.hist(nlm.flat, bins=100, range=(0,255))
    img1_blur = cv2.medianBlur(nlm,3)  # usually varies between 3,5,7.
    plt.figure(figsize=(10,10))
    plt.title('Noise Reduced Image')
    plt.imshow(img1_blur)
    plt.savefig('Noise_red.Tif', format='Tif')
    plt.colorbar()
    plt.show() 
    img1_thresh = cv2.adaptiveThreshold(img1_blur,1,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2.5) # Other option is using cv2.ADAPTIVE_THRESH_GAUSSIAN_C ; cv2.ADAPTIVE_THRESH_MEAN_C
    kernel=np.ones((3,3),np.uint8)
    plt.figure(figsize=(10,10))
    plt.title('Threshold Image')
    plt.imshow(img1_thresh)
    plt.savefig('Thresholded_img.png',dpi= 300, format='png')
    plt.show()
# =============================================================================
    dst = cv2.fastNlMeansDenoising(img1_thresh,None,2,3,3)
#    # fastNlMeansDenoising(src, dst, h, templateWindowSize, searchWindowSize)
#                 # h: Parameter regulating filter strength. Big "h" value perfectly removes noise 
#                 # but also removes image details, smaller "h" value preserves details but also preserves some noise
#     
    plt.figure(figsize=(10,10))
    plt.title('Denoise Threshold Image')
    plt.imshow(dst)
    plt.savefig('Denoise Thresholded_img.Tif',dpi= 300, format='Tif')
    plt.show()
    plt.hist(img1_thresh.flat, bins=100, range=(0,1)) 
    opening =cv2.morphologyEx(dst, cv2.MORPH_OPEN, kernel)
    plt.hist(opening.flat, bins=100) 
    opening = opening > 0
    dst1 = morphology.remove_small_objects(opening, min_size= 2)
    dst= morphology.remove_small_holes(dst1,area_threshold=55, connectivity=1) 
    fig=plt.figure(frameon=False)
    fig.set_size_inches(7.01,7.01)
    plt.axis('off')
    plt.imshow(dst)
    scalebar = ScaleBar(0.054054054, "um", box_color = None)
    plt.gca().add_artist(scalebar)
    
    plt.savefig('Remove_small_Holes.png',dpi=300, format='png')
    plt.show
    dst_arr=np.array(dst)
    np_img= np.array(img1_thresh)
    print(np_img)
    print (img1_thresh.shape)

    
    #img1_thresh=img1_thresh[:,1:] # If the image size is odd : like 1767 * 2400 or something then write it as img1_thresh=img1_thresh[1:,:]
    dst_thresh=dst[:,:]    
    #print (img1_thresh.shape)
    print (dst_thresh.shape)
    shp = np.array(img1_thresh.shape)//2 
    print (shp)
    tpix= (2*2*shp[0]*shp[1])
    print (tpix)
    pix=(2*shp[1])
    print (pix)
    shape = [2048,2048] # calculate the canvas size by calculating hypotenuse of the image size.
    dst_arr = np.zeros(shape) # canvas 
    dst_arr[shape[0]//2-shp[0]:shape[0]//2+shp[0],shape[1]//2-shp[1]:shape[1]//2+shp[1]] = dst_thresh
    
    plt.figure(figsize=(10,10))
    plt.imshow(dst_arr)
    plt.savefig('Thresholded_img_padded.Tif', format='Tif')
    plt.show()
    avg_dist = []
    avg_invd = []
    avg_afrac = []
    distance1 = []
    indis1=[]
    a_avg_afrac=[]
    b_frac=[]

    
    for angle in np.arange(0,180,ang_step): #for any step size varying from 0 to 360
        display_img = rotate(dst_arr,angle,order=0)
        display_img = display_img[display_img.shape[0]//2-shape[0]//2:display_img.shape[0]//2+shape[0]//2,
                        display_img.shape[1]//2-shape[1]//2:display_img.shape[1]//2+shape[1]//2]# square shaped 2d image 
        plt.imshow(display_img)
        plt.show()
        distance =[]
        indis =[]
        aafrac=[]
        for i in range(display_img.shape[0]):
            for j in range(display_img.shape[1]-1):
                if display_img[i,j+1]-display_img[i,j] == 1:
                    left = j
                if display_img[i,j+1]-display_img[i,j] == -1:
                    distance.append(j-left)
                    indis.append(1/(j-left))  
        distance1.append(distance)
        distance=np.array(distance)
        indis1.append(indis)
        indis=np.array(indis)
        print (distance)
        print (len(distance))
        tdist=np.sum(distance[1:-1])
        afrac=(tdist*100)/tpix
        bfrac=(100-afrac)
        b_frac.append(bfrac)
        avg_afrac.append(afrac)
        print("The sum of Alpha is :",np.sum(distance[1:-1]))#distance = distance[distance>min_thick]					     
        print("The Alpha Fraction is :",afrac)
    avg_dist.append(np.mean(distance[1:-1])) 
    avg_invd.append(np.mean(indis[1:-1]))
    print(np.mean(distance[1:-1]))
    print(np.mean(indis[1:-1]))
    aafrac=np.array(avg_afrac)
    a_avg_afrac.append(np.mean(aafrac))
    print('Average distance list:',avg_dist)
    print('Average distance in pixels for all rotations:',np.mean(avg_dist)) 
    print('Average Inv distance in pixels for all rotations:',np.mean(avg_invd)) 
    print('Average Area Frac:',a_avg_afrac)
    return (nlm,counts,bins,img1_blur,dst, afrac, np_img ,distance1,indis1)