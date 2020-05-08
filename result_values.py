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
            #chose a random example to see how it works
        self.faits_initiaux = self.donnees_test[0]
        self.regles = self.arbre.regles_generation()
        #self.justification_prediction(self.faits_initiaux)
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
        
    def justification_prediction(self, exemple):
        """ finds the justifications for classifying an example """
        #sort example keys alphabetically
        sorted_example =sorted(exemple.items())
        #sort rules by keys alphabetically
        sorted_rules = self.sort_rules()
        
        
        justification = []
        minimum_correct = -1
            
        for rule in sorted_rules:
            correct_cond = 0
            for cond_rule,cond_ex in zip(rule,sorted_example):
                if cond_rule == cond_ex:
                    correct_cond += 1
                if correct_cond > minimum_correct:
                    minimum_correct = correct_cond
                    justification.append(rule)
        
        #we choose to return the rule that has the most conditions true
        try:
            return_value = max(justification, key=len)
        except:
            #otherwise we return the first found
            return_value = justification[0]
        return return_value
    
    def sort_rules(self):
        """ orders the rules in alphabetical order """
        sorted_rules = []
        for regle in self.regles:
        
            sorted_rule= sorted(regle, key=lambda r: r[0])
            
            result = sorted_rule.pop(0)
            sorted_rule2= sorted(sorted_rule, key=lambda r: r[0])
            sorted_rule2.append(result)
            
            sorted_rules.append(sorted_rule2)
        return sorted_rules
    

