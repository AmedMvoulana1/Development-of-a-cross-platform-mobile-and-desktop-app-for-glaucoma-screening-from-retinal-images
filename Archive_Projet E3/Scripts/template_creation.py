#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script permettant de générer des images de référence du disque optique
# sur quelques images de la base de données


import numpy as np
import cv2
import os
#import matplotlib.pyplot as plt
#from skimage import exposure
#from scipy import ndimage
import csv



""" ---------------------------------------------------------------------------------------------- """


base = '../Template/Input/'

# Lecture des fichiers du dossier path
fichiers = os.listdir(base)
fichiers.sort()

# Dossier source contenant les images en entrée et dossier cible
outpath1 = '../Template/Output/'

try:
    os.makedirs(outpath1)
except OSError:
    if not os.path.isdir(outpath1):
        Raise


""" ---------------------------------------------------------------------------------------------- """


def equalization(image):
    #image = cv2.imread(path+image, 0)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl1 = clahe.apply(image)
    cl1 = clahe.apply(cl1)
    
    # Enregistrement des résultats
    #cv2.imwrite(outpath2+str(image), cl1)
    
    return cl1.astype(np.uint8)


def histogramme_ref(base):
        
    # Lecture des images de référence
    
    image0 = cv2.imread(base + "drishtiGS_004.png")
    image1 = cv2.imread(base + "drishtiGS_008.png")
    image2 = cv2.imread(base + "drishtiGS_010.png")
    image3 = cv2.imread(base + "drishtiGS_012.png")
    image4 = cv2.imread(base + "drishtiGS_015.png")  
    image5 = cv2.imread(base + "drishtiGS_016.png")
        
    # Liste des images de référence
    
    images = [image0, image1, image2, image3, image4, image5]
    
    # Liste des images après preprocessing
    
    new_images = []
    
    # Redimensionnement des images
    
    width, height = images[0].shape[:2]
    ratio = width/height
    print(width)
    
    for image in images:
        if width > 900 :
            image = cv2.resize(image, (900, int(900*ratio)), interpolation = cv2.INTER_CUBIC)
        
        # Processing : filtre médian
        
        #im_eq = equalization(image)
        im = cv2.medianBlur(image, 5)
        new_images.append(im)
    
    
    # On rogne les images pour former des images de référence du disque optique
    
    new_images[0] = new_images[0][370:610, 320:560]
    new_images[1] = new_images[1][310:550, 365:605]
    new_images[2] = new_images[2][270:510, 280:520]
    new_images[3] = new_images[3][330:570, 360:600]
    new_images[4] = new_images[4][270:510, 360:600]
    new_images[5] = new_images[5][290:530, 350:590]
      
    
    # Histogrammes des différents canaux
    histo_r = []
    histo_g = []
    histo_b = []
    
    for i in range(0, len(images)):
        
        cv2.imwrite(outpath1 + fichiers[i], new_images[i])

        r = new_images[i][:,:,2]
        g = new_images[i][:,:,1]
        b = new_images[i][:,:,0]
        
        
        # Histogrammes des différents canaux RGB
        hist1,bins1 = np.histogram(r,256,[0,256])
        hist2,bins2 = np.histogram(g,256,[0,256])
        hist3,bins3 = np.histogram(b,256,[0,256])

        histo_r.append(hist1)
        histo_g.append(hist2)
        histo_b.append(hist3)
        
    # Histogrammes de référence associés à chaque canal
    
    hist_ref_r = np.zeros(len(histo_r[0]))
    hist_ref_g = np.zeros(len(histo_g[0]))
    hist_ref_b = np.zeros(len(histo_b[0]))
    
    
    for i in histo_r:
        #print(i)
        hist_ref_r = hist_ref_r[0:200] + i[0:200]
    
    for i in histo_g:
        #print(i)
        hist_ref_g = hist_ref_g[0:200] + i[0:200]    

    for i in histo_b:
        #print(i)
        hist_ref_b = hist_ref_b[0:200] + i[0:200]    
    

    hist_ref_r = hist_ref_r/len(images)
    hist_ref_r = hist_ref_r + 0.5*np.ones(len(hist_ref_r))
    hist_ref_r = hist_ref_r.astype(int)

    hist_ref_g = hist_ref_g/len(images)
    hist_ref_g = hist_ref_g + 0.5*np.ones(len(hist_ref_g))
    hist_ref_g = hist_ref_g.astype(int)

    hist_ref_b = hist_ref_b/len(images)
    hist_ref_b = hist_ref_b + 0.5*np.ones(len(hist_ref_b))
    hist_ref_b = hist_ref_b.astype(int)

    return hist_ref_r, hist_ref_g, hist_ref_b



""" ---------------------------------------------------------------------------------------------- """

hist_ref_r, hist_ref_g, hist_ref_b = histogramme_ref(base)


# Enregistrement de l'histogramme associé au canal R

with open(outpath1 + 'hist_ref_r.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in hist_ref_r:
        spamwriter.writerow([i])


# Enregistrement de l'histogramme associé au canal G

with open(outpath1 + 'hist_ref_g.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in hist_ref_g:
        spamwriter.writerow([i])


# Enregistrement de l'histogramme associé au canal B
        
with open(outpath1 + 'hist_ref_b.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in hist_ref_b:
        spamwriter.writerow([i])
      
        
        
        