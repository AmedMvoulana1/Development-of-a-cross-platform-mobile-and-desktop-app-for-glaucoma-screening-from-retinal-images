#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Script permettant de faire la segmentation du OC et du OD pour le diagnostic de glaucome grâce au CDR

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny
from scipy.spatial import distance as dis
from sklearn.metrics import confusion_matrix
from skimage.measure import label, regionprops
from skimage.morphology import convex_hull_image


""" ---------------------------------------------------------------------------------------------- """

base = '../Images/'

outpath = '../OC_OD_segmentation/' 

try:
    os.makedirs(outpath)
except OSError:
    if not os.path.isdir(outpath):
        Raise


fichiers = os.listdir(base)
fichiers.sort()


""" ---------------------------------------------------------------------------------------------- """

# Fonction d'égalisation d'histogramme

def equalization(image):

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl1 = clahe.apply(image)
    
    return cl1.astype(np.uint8)


# Classe associée à l'algorithme de K-means 

class Segment:
    def __init__(self,segments=4):
        #define number of segments, with default 3
        self.segments=segments
        
    def kmeans(self,image):
       # Etape de prétraitement : application d'un filtre anisotrope
       #image=mfs.anisotropic_diffusion(image, niter=1, kappa=50, gamma=0.1, voxelspacing=None, option=1)
       
       vectorized=image.flatten()
       vectorized=np.float32(vectorized)
       criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
              10, 1.0)
       ret,label,center=cv2.kmeans(vectorized,self.segments,None,
              criteria,10,cv2.KMEANS_RANDOM_CENTERS)
       res = center[label.flatten()]
       segmented_image = res.reshape((image.shape))
       return label.reshape((image.shape[0],image.shape[1])), segmented_image.astype(np.uint8), center
   
    def extractComponent(self,image,label_image,label):
       component=np.zeros(image.shape,np.uint8)
       component[label_image==label]=image[label_image==label]
       return component
   

# Fonction effectuant le calcul de la distance entre deux points du plan
def get_distance(x, y, i, j):
    
    distance = dis.euclidean((i,j), (x, y))
    
    return distance


# Fonction calculant la transformée de Hough circulaire d'une image binaire
def hough(binary_image, minRad, maxRad):
    
    #image_rgb = cv2.cvtColor(binary_image,cv2.COLOR_GRAY2BGR)
    binary = binary_image.copy()
    
    edges = canny(binary, sigma=5, low_threshold=10, high_threshold=50)
    
    #hough_radii = np.arange(100, 150, 2)
    hough_radii = np.arange(minRad, maxRad, 2)
    hough_res = hough_circle(edges, hough_radii)
    
    # Select the most prominent 5 circles
    accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii,
                                               total_num_peaks=1)
    center_x = cx[0]
    center_y = cy[0]
    radius = radii[0]
    
    (x, y) = (0, 0)
    r = 0
    
    nb_pixels = 0
    
    for center_y, center_x, radius in zip(cy, cx, radii):
        
        distance = [get_distance(center_y, center_x, i, j) for i in range(binary.shape[0]) for j in range(binary.shape[1])]
        distance = np.reshape(distance, binary.shape)

        in_circle = binary[(binary != 0) & (distance < radius)]
        pixels = len(in_circle)
        
        if pixels > nb_pixels:
            nb_pixels = pixels
            (x, y) = (center_x, center_y)
            r = radius
    
    (center_y, center_x) = (y, x)
    radius = r
    
    
    # Remplissage du cercle detecté, pour résultat final de segmentation
    for j in range(0, binary.shape[0]):
        for i in range(0, binary.shape[1]):
            distance = get_distance(center_y, center_x, j, i)

            if distance <= radius and binary[j,i] == 0:
                binary[j,i] = 255
            elif distance > radius and binary[j,i] == 255:
                binary[j,i] = 0
                          
    return binary, radius
        

# Fonction faisant l'union du OC et du DO détectés
    
def disque_optique_entier(od, oc):
    
    disque_optique = cv2.bitwise_or(oc, od)
    
    return disque_optique



# Fonction de segmentation du OC et du DO via K-means
    
def segmentation(cropped):
    
    #cropped = equalization(cropped)

    """ ------------- Algorithme de k-means -------------------------- """
    
    seg = Segment()
    
    # On extrait une carte des labels, une image résultat des clusters, et un tableau des centres de clusters
    # (ici, 4 clusters donc 4 centres)
    label, result, center = seg.kmeans(cropped)
    cv2.imwrite(outpath+'1_k_means.jpg', result)

    # On extrait les pixels appartenant au cluster du centre ayant le niveau de gris le plus important
    # (les pixels appartenant donc au CUP)
    extracted=seg.extractComponent(cropped,label, np.argmax(center))
    
    # Binarisation de l'image résultat d'extraction du CUP
    ret, thresh = cv2.threshold(extracted, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    # Fermeture morphologique de l'image binarisée
    kernel = np.ones((3,3),np.uint8)
    closing_oc = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    # Enregistrement de l'image du CUP detecté
    cv2.imwrite(outpath+'2_cup.png', closing_oc)
            
    center[np.argmax(center)] = 0
    
    # Extraction des pixels du cluster associé au DO
    extracted2 = seg.extractComponent(cropped,label, np.argmax(center))
    
    # Binarisation de l'image résultat d'extraction du DO
    ret2, thresh2 = cv2.threshold(extracted2, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    complete_od = disque_optique_entier(thresh2, thresh)
    
    # Fermeture de l'image binarisée pour refermer les tunnels formés par les vaisseaux
    closing_od = cv2.morphologyEx(complete_od, cv2.MORPH_CLOSE, kernel)
    
    # Enregistrement de l'image du DO detecté
    cv2.imwrite(outpath+'3_od.jpg', closing_od)
    
    
    """ ------------- Transformée de Hough circulaire -------------------------- """
    
    OC_hough, OC_radius = hough(closing_oc, 60, 80)
    cv2.imwrite(outpath+'4_oc_hough.jpg', OC_hough)
    
    OD_hough, OD_radius = hough(closing_od, 80, 110)
    cv2.imwrite(outpath+'5_od_hough.jpg', OD_hough)
    
    
    """ ------------- Convex hull transform -------------------------- """
    
    OC_chull = convex_hull_image(closing_oc)
    #hullPoints = ConvexHull(OC_chull)
    #print(hullPoints)
    OC_chull = OC_chull*255
    
    OD_chull = convex_hull_image(closing_od)
    OD_chull = OD_chull*255
    
    return result, closing_oc, closing_od, OC_hough, OD_hough, OC_chull, OD_chull

    
# Fonction faisant le calcul de l'aire d'une image binaire
def calcul_aire(binary_image):
    
    binary_image = binary_image[binary_image != 0]
    aire = len(binary_image)
    
    return aire


# Fonction établissant le diagnostic en fonction du ratio
def diagnostic(ratio):
    
    if ratio < 0.64:
        diag = 'Normal'
        
    elif 0.64 < ratio and ratio <= 1.0:
        diag = 'Glaucomatous'
    
    else:
        diag = 'Erreur de calcul'

    return diag


""" ---------------------------------------------------------------------------------------------- """


# Lecture de l'image cropped du disque 
cropped = cv2.imread(base + '7_cropped.jpg', 0)
cv2.imwrite(outpath+'0_cropped.jpg', cropped)

#Segmentation des regions OC et OD
kmeans, OC, OD, OC_hough, OD_hough, OC_chull, OD_chull = segmentation(cropped)

cv2.imwrite(outpath+'6_oc_chull.jpg', OC_chull)
cv2.imwrite(outpath+'7_od_chull.jpg', OD_chull)

#Calcul de l'aire des deux régions
aire_oc = calcul_aire(OC_hough)
aire_od = calcul_aire(OD_hough)

# Calcul du CDR
CDR = aire_oc/aire_od

# Calcul de l'aire du RIM (en pixels)
aire_rim = aire_od - aire_oc

print("Valeur de CDR:")
print(CDR)
print("Aire du RIM:")
print(aire_rim)


# Diagnostic de glaucome
diag = diagnostic(CDR)

      
