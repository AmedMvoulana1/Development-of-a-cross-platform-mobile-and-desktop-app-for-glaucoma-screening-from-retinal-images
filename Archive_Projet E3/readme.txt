L'archive suivante comporte les outils permettant d'impl�menter la m�thode de dignostic de glaucome sur des images r�tiniennes.
Dans cette archive, vous retrouverez les dossiers suivants :

- Scripts : contient les fichiers .py d'impl�mentation de la m�thode, avec
	- template_creation.py : permet de cr�er les histogrammes de r�f�rence du disque optique, pour l'application d'un algorithme de Template Matching
	- OD_detection : permet de d�tecter le disque optique sur une image r�tinienne, en d�tectant les zones de plus grande intensit� de l'image pour ensuite appliquer un
	algorithme de Template Matching sur ces points brillants gr�ce aux histogrammes de r�f�rence cr�es avec template_creation.py. Finalement, une sous-fen�tre contenant 
	le disque optique est extraite
	- OC_OD_segmentation.py : permet de faire la segmenation du OC et du OD, depuis la sous-fen�tre contenant le disque optique. La m�thode exploite un algorithme de K-means et
	la transform�e de Hough circulaire. Gr�ce � la segmentation, le CDR est calcul� pour ensuite d�livrer un diagnostic de glaucome

- Images : les images r�tiniennes d'entr�e, avec le r�sultat de crop du disque optique

- Template : contient les images de r�f�rence du disque optique, ainsi que les histogrammes associ�s pour appliquer le Template Matching

- OD_detection : contient les images obtenus lors de l'impl�mentation de la m�thode de d�tection du disque, de l'�tape de preprocessing � l'image finale du crop du disque

- OC_OD_segmentation : contient les images obtenus lors de l'impl�mentation de la m�thode de segmentation du OC et du OD, avec les r�sultat de K-means, d'extraction des r�gions et 
de Hough circulaire

- article.pdf et poster.pdf, li�s � la description de la m�thode de diagnostic de glaucome.