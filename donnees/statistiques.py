class StatistiquesID3:
    """ Calcule les statistiques d'ID3 """

    def trouver_taille_maximale(self, arbre):
        """ trouve la taille maximale de l'arbre généré """
    
    
    def evaluer_similitude(self, predicted, actual):
        """ calcule le % de similarité entre les 2 listes"""
        count_same = sum(1 if x == y else 0 for x,y in zip(actual,predicted))
        count_total = len(actual)
        
        return count_same/count_total
