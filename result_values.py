from moteur_id3.noeud_de_decision import NoeudDeDecision
from moteur_id3.id3 import ID3
from donnees.traitement import TraitementDonnees
from donnees.statistiques import StatistiquesID3

class ResultValues():

    def __init__(self):
        
        # load data
        self.donnees_entrainement, self.donnees_test = self.import_data()
        
        id3 = ID3()
        
        #Task 1
        self.arbre = id3.construit_arbre(self.donnees_entrainement)
        
        #Statistics pour task 1 A COMPLETER
        self.stat = StatistiquesID3()
        nb_enfants = len(self.arbre.enfants)
        
        # Task 3
        self.faits_initiaux = None
        #self.regles = self.arbre.gen_regles()
        # Task 5
        self.arbre_advance = None

    def get_results(self):
        return [self.arbre, self.faits_initiaux, self.regles, self.arbre_advance]
    
    def get_arbre(self):
        return self.arbre
    
    def get_faits_initiaux(self):
        return self.faits_initiaux
    
    def get_regles(self):
        return self.regles
    
    def get_arbre_avance(self):
        return self.regles
    
    def import_data(self):
        importation = TraitementDonnees()
        donnees_entrainement = importation.import_donnees('res/train_bin.csv')
        donnees_test = importation.import_donnees_test('res/test_public_bin.csv')
        return donnees_entrainement, donnees_test
    
    def evaluer_model(self):
        predicted = []
        actual = []
        
        for donnee in self.donnees_test:
            rep = self.arbre.classifie(donnee)
            actual.append(donnee['target'])
            
            #takes the last character of rep i.e the result of classification
            predicted.append(rep[-1])
        
        return self.stat.evaluer_similitude(predicted,actual)

        
    
    
    
    
    
    

