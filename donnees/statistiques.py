class StatistiquesID3:
    """ Calcule les statistiques d'ID3 """

    def __init__(self):
        self.nb_changement_1 = 0
        self.nb_changement_2 = 0

    def trouver_taille_maximale(self, arbre):
        """ trouve la taille maximale de l'arbre généré """


    def evaluer_similitude(self, predicted, actual):
        """ calcule le % de similarité entre les 2 listes"""
        count_same = sum(1 if x == y else 0 for x,y in zip(actual,predicted))
        count_total = len(actual)
        return count_same/count_total

    def evaluer_model(self,donnees,arbre):
        """ evalue le modèle basé sur les données de test et l'arbre fournit en parametre. Retourne le pourcentage d'évaluation correcte """
        predit = []
        vrai_val = []

        for donnee in donnees:

            rep = arbre.classifie(donnee[1])
            vrai_val.append(donnee[0])

            #takes the last character of rep i.e the result of classification
            predit.append(rep[-1])

        return self.evaluer_similitude(predit,vrai_val)*100

    def evaluer_diagnostique(self, nb_de_correct):
        """ evalue si le diagnostique a 2 ou moins changements de parametres en ajoutant le cas écheant à l'attribut qui comptabilise le bon nombre """
        if nb_de_correct == 2:
            self.nb_changement_2 += 1
        if nb_de_correct == 1:
            self.nb_changement_1 +=1


    def trouver_nombre_patients_ok(self):
        """ retourne le nombre de patients avec un diagnostique de changement de 1 et 2 paramètres"""
        return self.nb_changement_1, self.nb_changement_2

    def get_nombre_malades(self,patients):
        """ Retourne le nombre de patients malades dans les données test"""
        nb_malade =0
        for patient in patients:
            if patient['target'] == '1':
                nb_malade +=1
        return nb_malade

    def calculer_statistiques(self, regles):
        """ calcule les statistiques de l'arbre construit pour la partie 1:
        le nombre d'enfants, la profondeure moyenne et maximale."""

        self.nb_enfants = len(regles)

        self.taille_max = -1
        self.taille_moyenne = 0

        for regle in regles:
            taille_regle = len(regle)

            if taille_regle >= self.taille_max:
                self.taille_max = taille_regle

            self.taille_moyenne += taille_regle

        self.taille_moyenne/= self.nb_enfants

    def get_statistiques(self):
        """ retourne une string avec les statistiques de l'arbre """
        print('il y a ' + str(self.nb_enfants) + ' enfants. Larbre a une taille moyenne de '
         + str(round(self.taille_moyenne,0)) + '. Sa taille maximale est de ' + str(self.taille_max)
            + '.')
