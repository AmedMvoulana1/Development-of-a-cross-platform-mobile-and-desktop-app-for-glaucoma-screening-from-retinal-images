L'archive suivante comporte les outils permettant d'implémenter la méthode de dignostic de glaucome sur des images rétiniennes.
Dans cette archive, vous retrouverez les dossiers suivants :

- Scripts : contient les fichiers .py d'implémentation de la méthode, avec
	- template_creation.py : permet de créer les histogrammes de référence du disque optique, pour l'application d'un algorithme de Template Matching
	- OD_detection : permet de détecter le disque optique sur une image rétinienne, en détectant les zones de plus grande intensité de l'image pour ensuite appliquer un
	algorithme de Template Matching sur ces points brillants grâce aux histogrammes de référence crées avec template_creation.py. Finalement, une sous-fenêtre contenant 
	le disque optique est extraite
	- OC_OD_segmentation.py : permet de faire la segmenation du OC et du OD, depuis la sous-fenêtre contenant le disque optique. La méthode exploite un algorithme de K-means et
	la transformée de Hough circulaire. Grâce à la segmentation, le CDR est calculé pour ensuite délivrer un diagnostic de glaucome

- Images : les images rétiniennes d'entrée, avec le résultat de crop du disque optique

- Template : contient les images de référence du disque optique, ainsi que les histogrammes associés pour appliquer le Template Matching

- OD_detection : contient les images obtenus lors de l'implémentation de la méthode de détection du disque, de l'étape de preprocessing à l'image finale du crop du disque

- OC_OD_segmentation : contient les images obtenus lors de l'implémentation de la méthode de segmentation du OC et du OD, avec les résultat de K-means, d'extraction des régions et 
de Hough circulaire

- article.pdf et poster.pdf, liés à la description de la méthode de diagnostic de glaucome.