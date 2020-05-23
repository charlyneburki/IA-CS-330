from moteur_id3.noeud_de_decision import NoeudDeDecision
from moteur_id3.id3 import ID3
from donnees.traitement import TraitementDonnees
from donnees.statistiques import StatistiquesID3
from moteur_diagnostic.diagnostic import Diagnostic


#last part
from moteur_id3.id3_pt5 import ID3_PT5
from moteur_id3.noeud_de_decision_pt5 import NoeudDeDecision_PT5

class ResultValues():

    def __init__(self):
        
        # load data
        donnees_entrainement, self.donnees_test, self.donnees_entrainement_adv, self.donnees_test_adv = self.importer_donnees()
        
        id3 = ID3()
        
        #Task 1
        self.arbre = id3.construit_arbre(donnees_entrainement)
        
        #Statistics pour task 1 A COMPLETER dans fonction get_statistique
            #pour partie 1
        self.stat = StatistiquesID3()
        nb_enfants = len(self.arbre.enfants)
        
        #Task 2
         #evaluate the tree created in part 1:
        self.evaluation_model_1 = self.evaluer_classification( self.donnees_test, self.arbre)
        

        
        # Task 3
        self.faits_initiaux = donnees_entrainement
        self.regles = self.generer_regles(self.arbre)
        
        
        
        # Task 5
        id3_adv = ID3_PT5()
        
        self.arbre_advance = id3_adv.construit_arbre(self.donnees_entrainement_adv)
        
        self.evaluation_model_2 = self.evaluer_classification( self.donnees_test_adv, self.arbre_advance)

    def get_results(self):
        return [self.arbre, self.faits_initiaux, self.regles, self.arbre_advance]
    
    def importer_donnees(self):
        """se charge d'importer les données pour le programme """
        importation = TraitementDonnees()
        donnees_entrainement = importation.import_donnees('res/train_bin.csv')
        donnees_test = importation.import_donnees('res/test_public_bin.csv')
        
        donnees_entrainement_avance = importation.import_donnees('res/train_continuous.csv')
        
        donnees_test_avancee = importation.import_donnees('res/test_public_continuous.csv')
        
        return donnees_entrainement, donnees_test, donnees_entrainement_avance, donnees_test_avancee
    
    def evaluer_classification(self,donnees,arbre):
        """ evalue le modèle basé sur les données de test et l'arbre fournit en parametre Retourne le pourcentage d'évaluation correcte """
        return self.stat.evaluer_model(donnees,arbre)
        
    def generer_regles(self,arbre, chemin=[]):
        """ genere une liste de règles correspondant à l'arbre passé en paramètre. """
        # Check if node is end node
        if arbre.terminal():
            # return path built until then inside a list
            listeUneRegle = []
            chemin.append(('=>',arbre.classe()))
            listeUneRegle.append(chemin)
            return listeUneRegle
        else:
            # List of rules geneated in child nodes
            nouvellesRegles = []
            for valeur, enfant in arbre.enfants.items():
                # update path
                cheminEnfant = chemin.copy()
                cheminEnfant.append((arbre.attribut, valeur))
                # Call method on child with updated path
                reglesEnfant = self.generer_regles(enfant,cheminEnfant)
                # Concatenate lists
                nouvellesRegles += reglesEnfant
                
            #sort the new rules alphabetically for stability purpose
            nouvellesRegles= sorted(nouvellesRegles, key=lambda r: r[0])
            return nouvellesRegles
                
    def determine_equality(self,patient, regle):
        """ determine si une regle correspond aux conditions du patient en comptabilisant le nombre de conditions vraies de la règle pour le patient"""
        sorted_rules = []
        rule = regle.copy()
        #we sort the rule to make it easier to classify
        result = rule.pop()
        sorted_rule= sorted(rule, key=lambda r: r[0])
        sorted_rule.append(result)
        
        
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
        #we try to find the second best rule
        print('no suitable rule found')
        return self.regles[0]
        
    def rprs_justification(self, patient):
        """ représente les informations d'un patient et son diagnostique. """
        
        etat_patient = patient[0]
        caract_patient = patient[1]
        
        justification = self.justification_prediction(caract_patient)
        print('---')
        print('Patient avec :')
        for key,value in caract_patient.items():
                print('{} = {},'.format(key,value))

        print('est {}.'.format(etat_patient[0]))

        print('est classifié comme {}'.format(justification[-1][-1]))
        print('car :')
        for condition in justification:
            print('{} = {},'.format(condition[0],condition[1]), end=' ')
        print('')
        print('***')
        print('suggestion de diagnostic:')
        print(self.rprs_diagnostic(caract_patient))
        print('***')
    
    def find_diagnostic(self, patient):
        """ basé sur les données du patient ainsi que les règles des patients en bonne santé établies à partir de l'arbre, cette fonctionne va trouver la meilleure règle correspondante au conditions du patient. """
        diagnose = Diagnostic()
        
        #find a list of all the healthy rules
        healthy_rules = diagnose.identifie_parametres_bons(self.regles)
        diagnostic_rules = []
        
        """same_sex = False
        same_age = False
        for healthy_rule in healthy_rules:
            # we first test to see if there is a matching rule with same age & sex
            for conditions in healthy_rule:
                for condition in conditions:
                    if (condition[0] == 'age' and condition[1] == patient['age']):
                        same_age = True
                    if (condition[0] == 'sex' and condition[1] == patient['sex']):
                        same_sex = True
            if same_sex or same_age:
                diagnostic_rules.append(healthy_rule)
            same_sex = False
            same_age = False"""
        
        diagnostic_rules = healthy_rules
        count_best =0
        minimal_best = 0
        final_diagnostic_rule = []
        
        etat_patient = patient[0]
        caract_patient = patient[1]
        print(caract_patient)
        
        #amongst the best candidates, finds the rule that has the least divergence in the conditions
        for diagnostic_rule in diagnostic_rules:
            for conditions in diagnostic_rule:
                for condition_rule,condition_patient in zip(conditions,patient.items()):
                    if condition_rule[0]==caract_patient and condition_rule[1] == condition_patient[1]:
                        count_best += 1
            if count_best >= minimal_best :
                minimal_best = count_best
                final_diagnostic_rule = diagnostic_rule

        return final_diagnostic_rule
        
    def suggest_diagnostic(self, patient, diagnostic_rule):
        """ basé sur une règle de diagnostique passé en paramètre, cette fonctionne retourne les suggestions de changement des paramètres du patient pour qu'il soit en bonne santé """
        
        justification = self.justification_prediction(patient)
  
        #no diagnostics to do
        if justification[-1][-1] == '0':
            return None
        else:
            change_suggestion = []
            for cond_patient in justification[:-1]:
                for conds_rule in diagnostic_rule:
                    for cond_rule in conds_rule:
                        if cond_rule[0] == cond_patient[0] and cond_rule[1] != cond_patient[1]:
                            change_suggestion.append(cond_rule)
                            
            #remove suggestions that involve age or sex
            change_suggestion_final = [change for change in change_suggestion if not (change[0] == 'age' or change[0] == 'sex')]
            
            return change_suggestion_final
    
    def rprs_diagnostic(self,patient):
        """ affiche la représentation d'un diagnostique du patient. """
        
        suggestion = self.diagnose_patient(patient)
        
        if suggestion == None:
            return 'patient en bonne santé, continuez comme ça !'
        else:

            diagnostic_final = ''
            diagnostic_final += 'Il faut changer: '
            for conds_suggestion in suggestion:
                diagnostic_final += ' {} à {} '.format(conds_suggestion[0] ,conds_suggestion[1], end=' ')
            return diagnostic_final
    
    def get_patients_sauves(self):
        """ retourne le nombre de patients nécéssitant 2 ou moins changements de paramètre pour etre en bonne santé"""
        return self.stat.trouver_nombre_patients_ok()
        
    
    def get_statistiques(self):
        """ fonction qui retourne tous les statistiques nécessaires """
        print('nb malades:')
        print(self.stat.get_nombre_malades(self.donnees_test))
        
        
    def diagnose_patient(self,patient):
        """ gère le diagnostique du patient"""
    
        diagnostic = self.find_diagnostic(patient)
        suggestion = self.suggest_diagnostic(patient,diagnostic)
        
        #counts the suggestion
        self.stat.evaluer_diagnostique(suggestion)
        
        return suggestion
        
        
                    
                
        
                    
                    
            
            
        
            
        
        
                
                
