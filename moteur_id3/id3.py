from math import log
from .noeud_de_decision import NoeudDeDecision

class ID3:
    """ Algorithme ID3. """
    
    def construit_arbre(self, donnees):
        """ Construit un arbre de décision à partir des données d'apprentissage.

            :param list donnees: les données d'apprentissage\
            ``[classe, {attribut -> valeur}, ...]``.
            :return: une instance de NoeudDeDecision correspondant à la racine de\
            l'arbre de décision.
        """
        
        # Nous devons extraire les domaines de valeur des 
        # attributs, puisqu'ils sont nécessaires pour 
        # construire l'arbre.
        attributs = {}
        for donnee in donnees:
            for attribut, valeur in donnee[1].items():
                valeurs = attributs.get(attribut)
                if valeurs is None:
                    valeurs = set()
                    attributs[attribut] = valeurs
                valeurs.add(valeur)
            
        arbre = self.construit_arbre_recur(donnees, attributs)
        
        return arbre

    def construit_arbre_recur(self, donnees, attributs):
        """ Construit rédurcivement un arbre de décision à partir 
            des données d'apprentissage et d'un dictionnaire liant
            les attributs à la liste de leurs valeurs possibles.

            :param list donnees: les données d'apprentissage\
            ``[classe, {attribut -> valeur}, ...]``.
            :param attributs: un dictionnaire qui associe chaque\
            attribut A à son domaine de valeurs a_j.
            :return: une instance de NoeudDeDecision correspondant à la racine de\
            l'arbre de décision.
        """
        def classe_unique(donnees):
            if len(donnees)==0:
                return True
            premiere_classe = donnees[0][0]
            for donnee in donnees:
                if donnee[0] != premiere_classe:
                    return False
            return True
        
        
        if donnees == []:
            return None
        elif classe_unique(donnees):
            #noeud terminal (si toutes les données restantes font partie de la meme classe)
            return NoeudDeDecision(None,donnees)
        
        else:
            #noeud interm
            h_C_As_att = [(self.h_C_A(donnees, attribut, attributs[attribut]),attribut) for attribut in attributs]
            attribut = min(h_C_As_att, key=lambda h_a: h_a[0])[1]
            
            #crée les sous-arbres de manière recursive
            attributs_restants = attributs.copy()
            del attributs_restants[attribut]
            
            partitions = self.partitionne(donnees,attribut,attributs[attribut])
            enfants = {}
            
            for valeur, partition in partitions.items():
                enfants[valeur] = self.construit_arbre_recur( partition, attributs_restants)
            return NoeudDeDecision(attribut,donnees,enfants)

    def partitionne(self, donnees, attribut, valeurs):
        """ Partitionne les données sur les valeurs a_j de l'attribut A.

            :param list donnees: les données à partitioner.
            :param attribut: l'attribut A de partitionnement.
            :param list valeurs: les valeurs a_j de l'attribut A.
            :return: un dictionnaire qui associe à chaque valeur a_j de\
            l'attribut A une liste l_j contenant les données pour lesquelles A\
            vaut a_j.
        """

        partitions = {valeur: [] for valeur in valeurs}
        
        for donnee in donnees:
            partition = partitions[donnee[1][attribut]]
            partition.append(donnee)
            
        return partitions
        
    def p_aj(self, donnees, attribut, valeur):
        """ p(a_j) - la probabilité que la valeur de l'attribut A soit a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.            
            :return: p(a_j)
        """
        
        nombre_donnees = len(donnees)
        
        #evite division par 0
        if nombre_donnees == 0:
            return 0.0
        
        #on compte le nombre d'occurences de la valeur parmi les données
        nombre_aj = 0
        for donnee in donnees:
            if donnee[1][attribut] == valeur:
                nombre_aj += 1
        
        #nombre d'occurences de la valeur / nombre de données
        return nombre_aj/nombre_donnees
                
        
    def p_ci_aj(self, donnees, attribut, valeur, classe):
        """ p(c_i|a_j) - la probabilité conditionnelle que la classe C soit c_i\
            étant donné que l'attribut A vaut a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.
            :param classe: la valeur c_i de la classe C.
            :return: p(c_i | a_j)
        """
        
        # occurence de a_j parmi les données
        donnees_aj = [donnee for donnee in donnees if donnee[1][attribut]==valeur]
        nb_aj = len(donnees_aj)
        
        #evite division par 0
        if nb_aj == 0:
            return 0.0
        
        #occurence de la classe c_i parmi les données ou A vaut a_j
        donnees_ci = [donnee for donnee in donnees_aj if donnee[0]==classe]
        nb_ci = len(donnees_ci)
        
        return nb_ci/nb_aj

    def h_C_aj(self, donnees, attribut, valeur):
        """ H(C|a_j) - l'entropie de la classe parmi les données pour lesquelles\
            l'attribut A vaut a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.
            :return: H(C|a_j)
        """
        #toutes les classes dans une liste
        classes = list(set([donnee[0] for donnee in donnees]))
        
        #p(c_i/a_j) pour chaque classe c_i
        p_ci_ajs = [self.p_ci_aj(donnees,attribut,valeur,classe) for classe in classes]
        
        return -sum([p_ci_aj*log(p_ci_aj,2.0) for p_ci_aj in p_ci_ajs if p_ci_aj != 0])
        
        
        
    def h_C_A(self, donnees, attribut, valeurs):
        """ H(C|A) - l'entropie de la classe après avoir choisi de partitionner\
            les données suivant les valeurs de l'attribut A.
            
            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param list valeurs: les valeurs a_j de l'attribut A.
            :return: H(C|A)
        """
        
        #P(a_j) pour chaque valeur a_j de l'attribut A
        p_ajs = [self.p_aj(donnees,attribut,valeur) for valeur in valeurs]
        #H_C_aj pour chaque valeur a_j de l'attribut A
        h_c_ajs = [self.h_C_aj(donnees, attribut, valeur) for valeur in valeurs]
        
        return sum(p_aj*h_c_aj for p_aj,h_c_aj in zip(p_ajs, h_c_ajs))
