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
        self.faits_initiaux = self.donnees_test[0] #what is this ?
        self.regles = self.arbre.generer_regles()
        
        # Task 5
        self.arbre_advance = None

    def get_results(self):
        return [self.arbre, self.faits_initiaux, self.regles, self.arbre_advance]
    
    def import_data(self):
        """se charge d'importer les données pour le programme """
        importation = TraitementDonnees()
        donnees_entrainement = importation.import_donnees('res/train_bin.csv')
        donnees_test = importation.import_donnees_test('res/test_public_bin.csv')
        return donnees_entrainement, donnees_test
    
    def evaluer_model(self):
        """ evalue le modèle basé sur les données de test. Retourne le pourcentage d'évaluation correcte """
        predicted = []
        actual = []
        
        for donnee in self.donnees_test:
            rep = self.arbre.classifie(donnee)
            actual.append(donnee['target'])
            
            #takes the last character of rep i.e the result of classification
            predicted.append(rep[-1])
        
        return self.stat.evaluer_similitude(predicted,actual)*100
                
    def determine_equality(self,patient, regle):
        """ determine si une regle correspond aux conditions du patient en comptabilisant le nombre de conditions vraies de la règle pour le patient"""
        sorted_rules = []
        rule = regle.copy()
        #we sort the rule to make it easier to classify
        result = rule.pop()
        sorted_rule= sorted(rule, key=lambda r: r[0])
        sorted_rule.append(result)
        
        sorted_rules.append(sorted_rule)
        
        #we sort the example alphabetically as well
        sorted_patient= sorted(patient.items())
        
        total = 0
        for cond_rule in sorted_rule:
            for cond_patient in sorted_patient:
                if cond_rule==cond_patient:
                    total += 1

        if total == (len(sorted_rule)-1):
            return True
        else:
            return False
    
    def justification_prediction(self, patient):
        """ recherche la règle correspondant aux conditions du patients. Retourne la meilleure règle qui décrit ses symptotes. """
        best_rule = []
        for rule in self.regles:
            equality = self.determine_equality(patient, rule)
            
            if equality:
                return rule
        
        
        #return never used
        #TO DO : FIND BETTER ALTERNATIVE THAN RETURNING FIRST RULE
        print('no suitable rule found')
        return self.regles[0]
    
    def evaluer_regles(self):
        
        predicted = []
        actual = []
        
        for donnee in self.donnees_test:
            rep = self.arbre.classifie(donnee)
            actual.append(donnee['target'])
            
            #takes the last character of rep i.e the result of classification
            result = self.justification_prediction(donnee)
            predicted.append(result[-1][-1])
        
        return self.stat.evaluer_similitude(predicted,actual)*100
        
    def rprs_justification(self, patient):
        
        justification = self.justification_prediction(patient)
        print('Patient avec :')
        for key,value in patient.items():
            if key == 'target':
                print('devrait être {}.'.format(value))
            else:
                print('{} = {},'.format(key,value))
                
        print('est classifié comme {}'.format(justification[-1][-1]))
        print('car :')
        for condition in justification:
            print('{} = {},'.format(condition[0],condition[1]), end=' ')
        
            
        
        
                
                
