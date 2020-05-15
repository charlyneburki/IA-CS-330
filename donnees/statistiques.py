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
    
    def evaluer_diagnostique(self, diagnostique):
        """ evalue si le diagnostique a 2 ou moins changements de parametres en ajoutant le cas écheant à l'attribut qui comptabilise le bon nombre """
        if diagnostique != None:
            if len(diagnostique) == 2:
                self.nb_changement_2 += 1
            if len(diagnostique) == 1:
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
        
