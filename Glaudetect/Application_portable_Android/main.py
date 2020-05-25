'''
Showcase of Kivy Features
=========================

This showcases many features of Kivy. You should see a
menu bar across the top with a demonstration area below. The
first demonstration is the accordion layout. You can see, but not
edit, the kv language code for any screen by pressing the bug or
'show source' icon. Scroll through the demonstrations using the
left and right icons in the top right or selecting from the menu
bar.

The file showcase.kv describes the main container, while each demonstration
pane is described in a separate .kv file in the data/screens directory.
The image data/background.png provides the gradient background while the
icons in data/icon directory are used in the control bar. The file
data/faust_github.jpg is used in the Scatter pane. The icons are
from `http://www.gentleface.com/free_icon_set.html` and licensed as
Creative Commons - Attribution and Non-commercial Use Only; they
sell a commercial license.

The file android.txt is used to package the application for use with the
Kivy Launcher Android application. For Android devices, you can
copy/paste this directory into /sdcard/kivy/showcase on your Android device.

'''

import time
from kivy.app import App
from os.path import dirname, join
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.camera import Camera
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage, Image
import os

from kivy.properties import OptionProperty
#from kivy.core.window import Window
#import numpy as np
#import cv2
#from scipy import ndimage
#from skimage.transform import hough_circle, hough_circle_peaks
# from skimage.feature import canny
# from scipy.spatial import distance as dis
# from sklearn.metrics import confusion_matrix
# from skimage.measure import label, regionprops
# from skimage.morphology import convex_hull_image
# import scipy.ndimage.measurements as snm
import csv
from pathlib import Path
import shutil

courant = os.getcwd()

DATA_FOLDER = os.getenv('EXTERNAL_STORAGE') #or os.path.expanduser("~")
folder = DATA_FOLDER+"/Glaudetect'"
try:
    os.mkdir(folder)
except OSError:
    pass


photos = folder+"/Photos_Capturées"
try:
    os.mkdir(photos)
except OSError:
    pass

diagnostic = folder+"/Diagnostic"
try:
    os.mkdir(diagnostic)
except OSError:
    pass

liste = []
listeImage = []
valeur_cdr = [0.0]
listeBase = []
save = []
langue = ['FR']


# class Segment:
#         def __init__(self,segments=4):
#             #define number of segments, with default 3
#             self.segments=segments
            
#         def kmeans(self,image):
#            # Etape de prétraitement : application d'un filtre anisotrope
#            #image=mfs.anisotropic_diffusion(image, niter=1, kappa=50, gamma=0.1, voxelspacing=None, option=1)
           
#            vectorized=image.flatten()
#            vectorized=np.float32(vectorized)
#            criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
#                   10, 1.0)
#            ret,label,center=cv2.kmeans(vectorized,self.segments,None,
#                   criteria,10,cv2.KMEANS_RANDOM_CENTERS)
#            res = center[label.flatten()]
#            segmented_image = res.reshape((image.shape))
#            return label.reshape((image.shape[0],image.shape[1])), segmented_image.astype(np.uint8), center
       
#         def extractComponent(self,image,label_image,label):
#            component=np.zeros(image.shape,np.uint8)
#            component[label_image==label]=image[label_image==label]
#            return component


class ShowcaseScreen(Screen):
    fullscreen = BooleanProperty(False)

    def contenu(self):
        return os.listdir(diagnostic)
    
    def dossier(self):
        return folder

    def ou(self):
        return(os.getcwd())

    def len(self, txt):
        if txt == 'Home':
            return True
        else:
            return False

    # def langue(self, txt):
    #     if len(langue) != 0:
    #         del langue[0]
    #     langue.append(txt)


    # def cdr(self):
    #     if valeur_cdr[0] > 0.63 and valeur_cdr[0] < 1.0:
    #         if  langue[0]== 'FR':
    #             self.ids.textCDR.add_widget(Label(text="         CDR = {} \n Le patient est [color=C41B1B]susceptible[/color] \nd'être atteint de Glaucome.".format(valeur_cdr[0]), markup=True))
    #         else:
    #             self.ids.textCDR.add_widget(Label(text="         CDR = {} \n The patient is [color=C41B1B]likely[/color] \naffected by Glaucoma.".format(valeur_cdr[0]), markup=True))
    #     elif valeur_cdr[0] <= 0.63 and valeur_cdr[0] > 0.0:
    #         if  langue[0]== 'FR':
    #             self.ids.textCDR.add_widget(Label(text='        CDR = {} \n      Le patient est [color=1BFE04]sain[/color].'.format(valeur_cdr[0]), markup=True))
    #         else:
    #             self.ids.textCDR.add_widget(Label(text='        CDR = {} \n      The patient is [color=1BFE04]healthy[/color].'.format(valeur_cdr[0]), markup=True))
    #     elif valeur_cdr[0] < 0.0:
    #         if  langue[0]== 'FR':
    #             self.ids.textCDR.add_widget(Label(text='        CDR = {} \n Erreur de calcul : \nVeuillez réeffectuer le test.'.format(valeur_cdr[0])))
    #         else:
    #             self.ids.textCDR.add_widget(Label(text='        CDR = {} \n Calculation error : \nPlease try again.'.format(valeur_cdr[0])))
    #     elif valeur_cdr[0] > 1.0:
    #         if  langue[0]== 'FR':
    #             self.ids.textCDR.add_widget(Label(text='        CDR = {} \n Erreur de calcul : \nVeuillez réeffectuer le test.'.format(valeur_cdr[0])))
    #         else:
    #             self.ids.textCDR.add_widget(Label(text='        CDR = {} \n Calculation error : \nPlease try again.'.format(valeur_cdr[0])))

    #     self.ids.textCDR.load_next(mode='next')
    #     os.chdir(listeBase[0])
    #     fichier = os.path.basename(listeBase[0])
    #     base = open(fichier + '.csv', 'a')
    #     name = os.path.basename(liste[0])
    #     try:
    #         writer = csv.writer(base)
    #         if valeur_cdr[0] > 0.63:
    #             writer.writerow([name, valeur_cdr[0], "Patient suceptible d'être atteint de Glaucome"])
    #         elif valeur_cdr[0] <= 0.63 and valeur_cdr[0] > 0.0:
    #             writer.writerow([name, valeur_cdr[0], "Patient sain"])
    #     finally:
    #         base.close()
    #     os.chdir(courant)

    def selected(self,filename):
        if len(filename) != 0:
            self.ids.image.source = filename[0]
            return filename[0]
        else:
            self.ids.image.source = 'data/background.png'

    def selected2(self, filename):
        if len(filename) != 0:
            return filename[0]
        else:
            pass
        
    def capture(self):
        os.chdir(photos)
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png(save[0]+ "_{}.png".format(timestr))
        self.ids.carousel.add_widget(Image(source=save[0]+ '_{}.png'.format(timestr)))
        self.ids.carousel.load_next(mode='next')
        listeImage.append(save[0]+ "_{}.png".format(timestr))
        os.chdir(courant)
        print("Captured")

    def save(self, txt):
        if len(save) != 0:
            del save[0]
        save.append(txt)

    def save2(self):
        if len(save) != 0:
            del save[0]
        save.append('Glaudetect')

    # def valider(self):
    #     if self.ids.carousel.current_slide != self.ids.carousel.slides[0]:
    #         file = listeImage[self.ids.carousel.index - 1]
    #         name, ext = Path(file).name.split('.')
    #         #image = cv2.imread(photos + '/' + file)

    #         Dossier = listeBase[0] + '/' + name
    #         try:
    #             os.mkdir(Dossier)
    #         except OSError:
    #             pass
    #         os.chdir(Dossier)
    #         cv2.imwrite('Image_base.png', image)
    #         os.chdir(courant)
    #         if len(liste) != 0:
    #             del liste[0]
    #         liste.append(Dossier)
    #     else:
    #         print('Erreur')
    #         pass
        
    # def valider2(self, filename):
    #     os.chdir(courant)
    #     if len(liste) != 0:
    #         del liste[0]
    #     name, ext = Path(filename).name.split('.')
    #     image = cv2.imread(filename)
    #     DossierImage = listeBase[0] + '/'+ name
    #     try:
    #         os.mkdir(DossierImage)
    #     except OSError:
    #         pass
    #     os.chdir(DossierImage)
    #     liste.append(DossierImage)
    #     cv2.imwrite("Image_base.png", image)
    #     os.chdir(courant)

    def valider_base1(self,txt):
        os.chdir(courant)
        if len(listeBase) != 0:
            del listeBase[0]
        Dossier = diagnostic + '/' + txt
        if os.path.exists(Dossier+'.csv'):
            pass
        else:
            os.chdir(Dossier)
            fichier = (txt) + ('.csv')
            base = open(fichier, 'w')
            try: 
                writer = csv.writer(base)
                writer.writerow(["Nom de l'image", "Valeur du CDR", "Diagnostic"])
            finally:
                base.close()
            os.chdir(courant)
        listeBase.append(Dossier)
        os.chdir(courant)

    def valider_base2(self,txt):
        os.chdir(courant)
        if len(listeBase) != 0:
            del listeBase[0]
        Dossier = diagnostic + '/' + txt
        if os.path.exists(Dossier):
            shutil.rmtree(Dossier, ignore_errors=False, onerror=None)
        try:
            os.mkdir(Dossier)
        except OSError:
            pass
        os.chdir(Dossier)
        fichier = (txt) + ('.csv')
        base = open(fichier, 'w')
        try: 
            writer = csv.writer(base)
            writer.writerow(["Nom de l'image", "Valeur du CDR", "Diagnostic"])
        finally:
            base.close()
        listeBase.append(Dossier)
        os.chdir(courant)


  #------------- Détecter -------------#
    #----- Menu d'images -----#

    def image1(self):
        os.chdir(liste[0])
        self.ids.image1.add_widget(Image(source='7_cropped.jpg'))
        self.ids.image1.load_next(mode='next')
        os.chdir(courant)

    def image2(self):
        os.chdir(liste[0])
        self.ids.image2.add_widget(Image(source='6_oc_chull.jpg'))
        self.ids.image2.load_next(mode='next')
        os.chdir(courant)

    def image3(self):
        os.chdir(liste[0])
        self.ids.image3.add_widget(Image(source='7_od_chull.jpg'))
        self.ids.image3.load_next(mode='next')
        os.chdir(courant)

    def image4(self):
        os.chdir(liste[0])
        self.ids.image4.add_widget(Image(source='4_oc_hough.jpg'))
        self.ids.image4.load_next(mode='next')
        os.chdir(courant)

    def image5(self):
        os.chdir(liste[0])
        self.ids.image5.add_widget(Image(source='5_od_hough.jpg'))
        self.ids.image5.load_next(mode='next')
        os.chdir(courant)

    def image6(self):
        os.chdir(liste[0])
        self.ids.image6.add_widget(Image(source='overlay.png'))
        self.ids.image6.load_next(mode='next')
        os.chdir(courant)

    #----------------------------#
    #------- Grande Image -------#

    def grandImage(self, index):
        os.chdir(liste[0])
        if index == 0:
            self.ids.bigImage.load_slide(self.ids.bigImage.slides[0])
        elif index == 1:
            self.ids.bigImage.load_slide(self.ids.bigImage.slides[1])
        # elif index == 2:
        #     self.ids.bigImage.load_slide(self.ids.bigImage.slides[2])
        # elif index == 3:
        #     self.ids.bigImage.load_slide(self.ids.bigImage.slides[3])
        # elif index == 2:
        #     self.ids.bigImage.load_slide(self.ids.bigImage.slides[2])
        # elif index == 3:
        #     self.ids.bigImage.load_slide(self.ids.bigImage.slides[3])
        elif index == 2:
            self.ids.bigImage.load_slide(self.ids.bigImage.slides[2])
            #self.ids.bigImage.load_next(mode='next')
        elif index == 3:
            self.ids.bigImage.load_slide(self.ids.bigImage.slides[3])
        else:
            pass
        os.chdir(courant)

    #----------------------------#        


    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(ShowcaseScreen, self).add_widget(*args)


class ShowcaseApp(App):

    index = NumericProperty(-1)
    current_title = StringProperty()
    time = NumericProperty(0)
    show_sourcecode = BooleanProperty(False)
    sourcecode = StringProperty()
    screen_names = ListProperty([])
    hierarchy = ListProperty([])
    language = OptionProperty('FR', options=('FR', 'EN'))

    def saveCDR(self):
    	os.chdir(liste[0])
    	screen = self.load_screen(self.screen_names.index('Detecter'))
    	screen.export_to_png("Resultat_CDR.png")
    	os.chdir(courant)

    def affiche(self):
        return liste[0]

    def build(self):
        self.title = "Bienvenue sur Glaudetect'"
        self.screens = {}
        self.available_screens = sorted([
            'Langues','Credits', 'Aides', 'Accueil', 'Detecter', 'Commencer', 'Capturer', 'Parcourir', 'Demarrer', 'Choose', 'Create', 'Save'])
        self.screen_names = self.available_screens
        curdir = dirname(__file__)
        self.available_screens = [join(curdir, 'data', 'screens',
            '{}.kv'.format(fn).lower()) for fn in self.available_screens]
        self.go_next_screen()

    def francais(self, *args):
        self.language = 'FR'
        self.title = "Bienvenue sur Glaudetect'"

    def anglais(self, *args):
        self.language = 'EN'
        self.title = "Welcome to Glaudetect'"    


    def go_folder(self):
        os.chdir(folder)


    def on_pause(self):
        return True

    def on_resume(self):
        pass


    def go_previous_screen(self):
        self.index = (self.index - 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='right')
        self.current_title = screen.name
        self.update_sourcecode()

    def go_next_screen(self):
        self.index = (self.index + 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='left')
        self.current_title = screen.name
        self.update_sourcecode()

    def go_screen(self, idx):
        os.chdir(courant)
        if self.index != idx:
            self.screens = {}
            self.index = idx
            self.root.ids.sm.switch_to(self.load_screen(idx), direction='left')
            self.update_sourcecode()
        else: pass

    def go_hierarchy_previous(self):
        ahr = self.hierarchy
        if len(ahr) == 1:
            return
        if ahr:
            ahr.pop()
        if ahr:
            idx = ahr.pop()
            self.go_screen(idx)

    def load_screen(self, index):
        if index in self.screens:
            return self.screens[index]
        screen = Builder.load_file(self.available_screens[index])
        self.screens[index] = screen
        return screen

    def read_sourcecode(self):
        fn = self.available_screens[self.index]
        with open(fn) as fd:
            return fd.read()

    def toggle_source_code(self):
        self.show_sourcecode = not self.show_sourcecode
        if self.show_sourcecode:
            height = self.root.height * .3
        else:
            height = 0

        Animation(height=height, d=.3, t='out_quart').start(
                self.root.ids.sv)
        self.update_sourcecode()

    def update_sourcecode(self):
        if not self.show_sourcecode:
            self.root.ids.sourcecode.focus = False
            return
        self.root.ids.sourcecode.text = self.read_sourcecode()
        self.root.ids.sv.scroll_y = 1

    def showcase_floatlayout(self, layout):

        def add_button(*t):
            if not layout.get_parent_window():
                return
            if len(layout.children) > 5:
                layout.clear_widgets()
            layout.add_widget(Builder.load_string('''
#:import random random.random
Button:
    size_hint: random(), random()
    pos_hint: {'x': random(), 'y': random()}
    text:
        'size_hint x: {} y: {}\\n pos_hint x: {} y: {}'.format(\
            self.size_hint_x, self.size_hint_y, self.pos_hint['x'],\
            self.pos_hint['y'])
'''))
            Clock.schedule_once(add_button, 1)
        Clock.schedule_once(add_button)

    def showcase_boxlayout(self, layout):

        def add_button(*t):
            if not layout.get_parent_window():
                return
            if len(layout.children) > 5:
                layout.orientation = 'vertical'\
                    if layout.orientation == 'horizontal' else 'horizontal'
                layout.clear_widgets()
            layout.add_widget(Builder.load_string('''
Button:
    text: self.parent.orientation if self.parent else ''
'''))
            Clock.schedule_once(add_button, 1)
        Clock.schedule_once(add_button)

    def showcase_gridlayout(self, layout):

        def add_button(*t):
            if not layout.get_parent_window():
                return
            if len(layout.children) > 15:
                layout.rows = 3 if layout.rows is None else None
                layout.cols = None if layout.rows == 3 else 3
                layout.clear_widgets()
            layout.add_widget(Builder.load_string('''
Button:
    text:
        'rows: {}\\ncols: {}'.format(self.parent.rows, self.parent.cols)\
        if self.parent else ''
'''))
            Clock.schedule_once(add_button, 1)
        Clock.schedule_once(add_button)

    def showcase_stacklayout(self, layout):
        orientations = ('lr-tb', 'tb-lr',
                        'rl-tb', 'tb-rl',
                        'lr-bt', 'bt-lr',
                        'rl-bt', 'bt-rl')

        def add_button(*t):
            if not layout.get_parent_window():
                return
            if len(layout.children) > 11:
                layout.clear_widgets()
                cur_orientation = orientations.index(layout.orientation)
                layout.orientation = orientations[cur_orientation - 1]
            layout.add_widget(Builder.load_string('''
Button:
    text: self.parent.orientation if self.parent else ''
    size_hint: .2, .2
'''))
            Clock.schedule_once(add_button, 1)
        Clock.schedule_once(add_button)

    def showcase_anchorlayout(self, layout):

        def change_anchor(self, *l):
            if not layout.get_parent_window():
                return
            anchor_x = ('left', 'center', 'right')
            anchor_y = ('top', 'center', 'bottom')
            if layout.anchor_x == 'left':
                layout.anchor_y = anchor_y[anchor_y.index(layout.anchor_y) - 1]
            layout.anchor_x = anchor_x[anchor_x.index(layout.anchor_x) - 1]

            Clock.schedule_once(change_anchor, 1)
        Clock.schedule_once(change_anchor, 1)


#     #Egalisation des histogrammes
#     def equalization(self,image):
#         clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
#         cl1 = clahe.apply(image)
#         cl1 = clahe.apply(cl1)
#         return cl1.astype(np.uint8)

#     def binarization(self,image):
#     #seuil, image_b = cv2.threshold(image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
#     #seuil, image_b = cv2.threshold(image,200,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#         seuil, image_b = cv2.threshold(image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#         if seuil < 82:
#             seuil = seuil + 40
#             seuil_max = 15
#         else:
#             seuil = seuil + 60
#             seuil_max = 10
#         print(seuil)
#         seuil, image_b = cv2.threshold(image,seuil,255,cv2.THRESH_BINARY)
        
#         return seuil, seuil_max, image_b

# # --------------------------- Step I : Détection des points candidats ---------------------------

#     def bright_points(self,image):
            
#         #cv2.imwrite(outpath+'0_image.jpg', image)

#         # Extraction du canal G de l'image
#         im = image[:,:,1]
#         im_eq = self.equalization(im)
        
#         #plt.imshow(im)
#         #plt.show()

#         #cv2.imwrite(outpath+'1_image_egalisee.jpg', im_eq)
        
#         # Binarisation de l'image par la méthode d'Otsu
#         seuil, seuil_max, image_b = self.binarization(im_eq)
#         #cv2.imwrite('2_image_seuillee.png', image_b)
        
#         """
#         if base == 'DRIVE/':
        
#             # Opération permettant de ne pas considérer le bord dans le calcul de la carte de distances
#             centre = (292,282)
#             R = 230
            
#             for j in range(0, image.shape[0]):
#                 for i in range(0, image.shape[1]):
#                     dist = dis.euclidean((i,j), (centre[0], centre[1]))
#                     if dist > R:
#                         image_b[j,i] = 0
#         """                               
                        
#         # Calcul de la carte de distance euclidienne
        
#         dist = ndimage.distance_transform_edt(image_b)
#         #cv2.imwrite(outpath + '3_distance_map.jpg', dist)
#         #plt.imshow(dist, cmap=plt.cm.gray)
        
               
#         # Calcul des maxima de la carte de distances 
#         maximum, index = np.amax(dist), np.unravel_index(np.argmax(dist, axis=None), dist.shape)
        
#         xd = index[0]
#         yd = index[1]
            
#         # Affichage du point le plus "brillant" sur l'image d'origine        
#         #cv2.circle(image, (yd, xd), 2, (0, 0, 255), thickness=4)
        
#         # Carte contenant les maximas    
#         #maxima = dist > maximum - 10
#         maxima = dist > maximum - seuil_max
#         #maxima = dist > moyenne+ecart
        
#         image1 = im_eq.copy()
        
#         # Image faisant apparaitre les zones maximales 
#         for i in range(0, maxima.shape[0]):
#             for j in range(0, maxima.shape[1]):
#                 if maxima[i][j] == True:
#                     image1[i][j] = 0
        
#         #plt.imshow(image1, cmap=plt.cm.gray)
#         #cv2.imwrite(outpath + '4_max_dist_map.jpg', image1)
        
#         maxima = maxima*1
        
#         # Etiquetage des zones maximales selon leur connexité
#         label_points = label(maxima)
        
#         # Liste des centres des zones maximales de l'image
#         centres = []
        
#         for region in regionprops(label_points):
            
#             # On ne considère uniquement les zones supérieures à une certaine aire
#             if region.area > 200:
                
#                 i = region.label
            
#                 centre = snm.center_of_mass(maxima, label_points, i)
#                 centre = (int(centre[0]), int(centre[1]))
                
#                 centres.append(centre)
            
#         #liste_centres.append(centres)
        
#         # Images faisant apparaitre les centres candidats
        
#         image2 = im_eq.copy()
            
#         for point in centres:
#             cv2.circle(image2, (point[1], point[0]), 5, (0, 0, 255), thickness=4)
            
#         #cv2.imwrite(outpath + '5_bright_points.jpg', image2)
        
#         return centres
    

    
# #---------------------- Step II : Détection du disque optique via template matching sur les points brillants détectés ---------------------------

# # A partir de la liste des centres de chaque image, le but est de trouver le centre du disque pour
# # chaque image en utilisant le critère de Template Matching

#     def template_matching(self,image,centres):
        
#         # Application d'un filtre gaussien
#         median = cv2.medianBlur(image, 5)

#         # Pour chaque point candidat dans une image, on construit une fenêtre centrée en ce point et on 
#         # calcule l'histogramme
        
#         #similarites = []
#         #correlations = []
#         c = 0
        
#         # Lecture des histogrammes de référence associés à la base générée grâce au 
#         # script 'template.py'
        
#         hist_ref_r = []
#         hist_ref_g = []
#         hist_ref_b = []

#         print(os.getcwd())
#         input_template = courant + '/data/Template/Output/'
#         print(os.getcwd())
        
#         with open(input_template + 'hist_ref_r.csv') as csvfile:
#             reader = csv.reader(csvfile)
#             for d in reader : 
#                 hist_ref_r.append(int(d[0]))

#         with open(input_template + 'hist_ref_g.csv') as csvfile:
#             reader = csv.reader(csvfile)
#             for d in reader : 
#                 hist_ref_g.append(int(d[0]))

#         with open(input_template + 'hist_ref_b.csv') as csvfile:
#             reader = csv.reader(csvfile)
#             for d in reader : 
#                 hist_ref_b.append(int(d[0]))
        
        
#         # Pour chaque centre de chaque image, on compare l'histogramme de sa fenêtre avec 
#         # l'histogramme de référence
        
#         #for tuplet in liste_centres[i]:
#         for tuplet in centres:

#             fenetre = median[tuplet[0]-120:tuplet[0]+120, tuplet[1]-120:tuplet[1]+120]

#             # Calcul de l'histogramme de chaque canal de la fenêtre courante
#             r = fenetre[:,:,2]
#             g = fenetre[:,:,1]
#             b = fenetre[:,:,0]
            
#             hist_r,bins_r = np.histogram(r,256,[0,256])
#             hist_g,bins_g = np.histogram(g,256,[0,256])
#             hist_b,bins_b = np.histogram(b,256,[0,256])
            
#             # Nous considérons uniquement les valeurs inférieures à 200
            
#             hist_r = hist_r[0:200]
#             hist_g = hist_g[0:200]
#             hist_b = hist_b[0:200]
            
#             # Calcul de la similarité et de la corrélation entre les deux histogrammes
#             # pour chacun des canaux
            
#             simi_r = (hist_r-hist_ref_r)**2
#             simi_r = sum(simi_r)
            
#             simi_g = (hist_g-hist_ref_g)**2
#             simi_g = sum(simi_g)

#             simi_b = (hist_b-hist_ref_b)**2
#             simi_b = sum(simi_b)
            
#             #similarites.append(simi)
            
#             # Correlation entre les deux histogrammes du canal R
#             c_r = 1/(1+simi_r)
            
#             # Correlation entre les deux histogrammes du canal G
#             c_g = 1/(1+simi_g)

#             # Correlation entre les deux histogrammes du canal B
#             c_b = 1/(1+simi_b)        
            
#             # Paramètres
#             t_r, t_g, t_b = 0.5, 2.0, 1.0
            
#             # Corrélation finale
#             corr = t_r*c_r + t_g*c_g + t_b*c_b
                    
#             if corr > c:
#                 centre_disque = tuplet
#                 #print(centre_disque)
#                 c = corr

#         # Affichage du point detecté sur l'image
#         image_cross = image.copy()
        
#         cv2.line(image_cross, (centre_disque[1]-10, centre_disque[0]-10), (centre_disque[1]+10, centre_disque[0]+10), (255,0,0), 2)
#         cv2.line(image_cross, (centre_disque[1]+10, centre_disque[0]-10), (centre_disque[1]-10, centre_disque[0]+10), (255,0,0), 2)
        
#         # Enregistrement des résultats
#         #cv2.imwrite(outpath+'6_Od_point.jpg', image_cross)
        
#         return centre_disque

# #----------------------------------------------------------------------------------------------

#     def OD_detection(self):
#         #image = cv2.imread("drishtiGS_036.png")
#         os.chdir(liste[0])
#         image = cv2.imread("Image_base.png")
#         #print(image.shape)

#         width, height = image.shape[:2]
#         ratio = width/height
#         if width > 900 :
#             image = cv2.resize(image, (900, int(900*ratio)), interpolation=cv2.INTER_CUBIC)

#         print("Début du traitement sur l'image choisie")
#         liste_centres = self.bright_points(image)
#         print("Liste des centres calculée, début du template matching")
#         centre_disque = self.template_matching(image, liste_centres)
#         #print(centre_disque)
#         cropped = image[centre_disque[1]-150:centre_disque[1]+150, centre_disque[0]-150:centre_disque[0]+150]
#         #print(cropped.shape)
#         cv2.imwrite('7_cropped.jpg', cropped)
#         print("Image traitée")
#         os.chdir(courant)


# #----------------------------------------------------------------------------------------------
#     # Fonction d'égalisation d'histogramme
#     def equalization2(self,image):

#         clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
#         cl1 = clahe.apply(image)
    
#         return cl1.astype(np.uint8)

#     # Fonction effectuant le calcul de la distance entre deux points du plan
#     def get_distance(self,x, y, i, j):
#         distance = dis.euclidean((i,j), (x, y))
#         return distance

#     # Fonction calculant la transformée de Hough circulaire d'une image binaire
#     def hough(self,binary_image, minRad, maxRad):     
#         #image_rgb = cv2.cvtColor(binary_image,cv2.COLOR_GRAY2BGR)
#         binary = binary_image.copy()      
#         edges = canny(binary, sigma=5, low_threshold=10, high_threshold=50)      
#         #hough_radii = np.arange(100, 150, 2)
#         hough_radii = np.arange(minRad, maxRad, 2)
#         hough_res = hough_circle(edges, hough_radii)
#         # Select the most prominent 5 circles
#         accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii,
#                                                    total_num_peaks=3)
#         center_x = cx[0]
#         center_y = cy[0]
#         radius = radii[0]    
#         (x, y) = (0, 0)
#         r = 0      
#         nb_pixels = 0      
#         for center_y, center_x, radius in zip(cy, cx, radii):           
#             distance = [self.get_distance(center_y, center_x, i, j) for i in range(binary.shape[0]) for j in range(binary.shape[1])]
#             distance = np.reshape(distance, binary.shape)
#             in_circle = binary[(binary != 0) & (distance < radius)]
#             pixels = len(in_circle)
#             if pixels > nb_pixels:
#                 nb_pixels = pixels
#                 (x, y) = (center_x, center_y)
#                 r = radius
#         (center_y, center_x) = (y, x)
#         radius = r
#         # Remplissage du cercle detecté, pour résultat final de segmentation
#         for j in range(0, binary.shape[0]):
#             for i in range(0, binary.shape[1]):
#                 distance = self.get_distance(center_y, center_x, j, i)

#                 if distance <= radius and binary[j,i] == 0:
#                     binary[j,i] = 255
#                 elif distance > radius and binary[j,i] == 255:
#                     binary[j,i] = 0
#         return binary, radius

#     # Fonction faisant l'union du OC et du DO détectés
#     def disque_optique_entier(self,od, oc):
#         disque_optique = cv2.bitwise_or(oc, od)
#         return disque_optique
   
#     # Fonction de segmentation du OC et du DO via K-means
#     def segmentation(self,cropped):
    
#         #cropped = equalization2(cropped)

#         # ------------- Algorithme de k-means -------------------------- """
#         seg = Segment()
#         # On extrait une carte des labels, une image résultat des clusters, et un tableau des centres de clusters
#         # (ici, 4 clusters donc 4 centres)
#         label, result, center = seg.kmeans(cropped)
#         #cv2.imwrite(outpath+'1_k_means.jpg', result)

#         # On extrait les pixels appartenant au cluster du centre ayant le niveau de gris le plus important
#         # (les pixels appartenant donc au CUP)
#         extracted=seg.extractComponent(cropped,label, np.argmax(center))
        
#         # Binarisation de l'image résultat d'extraction du CUP
#         ret, thresh = cv2.threshold(extracted, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        
#         # Fermeture morphologique de l'image binarisée
#         kernel = np.ones((3,3),np.uint8)
#         closing_oc = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
#         # Enregistrement de l'image du CUP detecté
#         #cv2.imwrite(outpath+'2_cup.png', closing_oc)
                
#         center[np.argmax(center)] = 0
        
#         # Extraction des pixels du cluster associé au DO
#         extracted2 = seg.extractComponent(cropped,label, np.argmax(center))
        
#         # Binarisation de l'image résultat d'extraction du DO
#         ret2, thresh2 = cv2.threshold(extracted2, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#         complete_od = self.disque_optique_entier(thresh2, thresh)
        
#         # Fermeture de l'image binarisée pour refermer les tunnels formés par les vaisseaux
#         closing_od = cv2.morphologyEx(complete_od, cv2.MORPH_CLOSE, kernel)
        
#         # Enregistrement de l'image du DO detecté
#         #cv2.imwrite(outpath+'3_od.jpg', closing_od)
        
        
#         # ------------- Transformée de Hough circulaire -------------------------- """
        
#         OC_hough, OC_radius = self.hough(closing_oc, 60, 80)
#         cv2.imwrite('4_oc_hough.jpg', OC_hough)
#         #self.ids.carousel_detecter.add_widget(Image(source='4_oc_hough.jpg'))

        
#         OD_hough, OD_radius = self.hough(closing_od, 80, 110)
#         cv2.imwrite('5_od_hough.jpg', OD_hough)
#         #self.ids.carousel_detecter.add_widget(Image(source='5_od_hough'))
        
        
#         #------------- Convex hull transform -------------------------- """
        
#         OC_chull = convex_hull_image(closing_oc)
#         #hullPoints = ConvexHull(OC_chull)
#         #print(hullPoints)
#         OC_chull = OC_chull*255
        
#         OD_chull = convex_hull_image(closing_od)
#         OD_chull = OD_chull*255
        
#         return result, closing_oc, closing_od, OC_hough, OD_hough, OC_chull, OD_chull

#     # Fonction faisant le calcul de l'aire d'une image binaire
#     def calcul_aire(self,binary_image):
    
#         binary_image = binary_image[binary_image != 0]
#         aire = len(binary_image)   
#         return aire

#     # Fonction établissant le diagnostic en fonction du ratio
#     def diagnostic(self,ratio):
#         if ratio < 0.64:
#             diag = 'Normal'    
#         elif 0.64 < ratio and ratio <= 1.0:
#             diag = 'Glaucomatous'
#         else:
#             diag = 'Erreur de calcul'
#         return diag

# #---------------------------------------------------------------------------------------------- """

#     def OC_OD_segmentation(self):
#         os.chdir(liste[0])
#         # Lecture de l'image cropped du disque 
#         cropped2 = cv2.imread('7_cropped.jpg',0)
#         #cv2.imwrite(outpath+'0_cropped.jpg', cropped)

#         #Segmentation des regions OC et OD
#         kmeans, OC, OD, OC_hough, OD_hough, OC_chull, OD_chull = self.segmentation(cropped2)
#         #cv2.imwrite('6_oc_chull.jpg', OC_chull)
#         #self.ids.carousel_detecter.add_widget(Image(source='6_oc_chull'))
#         #cv2.imwrite('7_od_chull.jpg', OD_chull)
#         #self.ids.carousel_detecter.add_widget(Image(source='7_od_chull'))

#         #Calcul de l'aire des deux régions
#         aire_oc = self.calcul_aire(OC_hough)
#         aire_od = self.calcul_aire(OD_hough)

#         # Calcul du CDR
#         CDR = aire_oc/aire_od
#         CDR = "%.3f" %CDR
#         CDR = float(CDR)
#         del valeur_cdr[0]
#         valeur_cdr.append(CDR)

#         # Calcul de l'aire du RIM (en pixels)
#         aire_rim = aire_od - aire_oc

#         print("Valeur de CDR:")
#         print(CDR)
#         print("Aire du RIM:")
#         print(aire_rim)

#         # Diagnostic de glaucome
#         diag = self.diagnostic(CDR)
#         os.chdir(courant)


#     def overlay(self, image_oc, image_od):

#         # Valeur décimale entre 0 et 1 pour paramétrer l'opacité pour l'overlapping
#         alpha = 0.6

#         # Copie des images du cup et du disque
#         overlay = image_oc.copy()
#         output = image_od.copy()

#         # On affiche l'image du oc en gris pour la différencier du disque en blanc
#         image_oc[np.where((image_oc == [255,255,255]).all(axis = 2))] = [127,127,127]
        
#         # Overlapping
#         cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

#         #plt.imshow(output)
#         #plt.show()

#         return output

#     def overlay_result(self):
#         os.chdir(liste[0])
#         image_oc = cv2.imread("4_oc_hough.jpg")
#         image_od = cv2.imread("5_od_hough.jpg")
#         output = self.overlay(image_oc, image_od)
#         cv2.imwrite("overlay.png", output)
#         print("Overlay terminé")
#         os.chdir(courant)

#     def total(self):
#         self.OD_detection()
#         self.OC_OD_segmentation()
#         self.overlay_result()


if __name__ == '__main__':
    ShowcaseApp().run()