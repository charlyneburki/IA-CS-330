from moteur_id3.noeud_de_decision import NoeudDeDecision
from moteur_id3.id3 import ID3
from donnees.traitement import TraitementDonnees
from donnees.statistiques import StatistiquesID3
from moteur_diagnostic.diagnostic import Diagnostic


#last part
from moteur_id3.id3_adv import ID3_ADV
from moteur_id3.noeud_de_decision_adv import NoeudDeDecision_ADV

class ResultValues():

    def __init__(self):

        # load data
        donnees_entrainement, self.donnees_test, self.donnees_entrainement_adv, self.donnees_test_adv = self.importer_donnees()

        id3 = ID3()

        #Task 1
        self.arbre = id3.construit_arbre(donnees_entrainement)

        #Statistics pour task 1
        self.stat = StatistiquesID3()

        #Task 2
         #evaluate the tree created in part 1:
        self.evaluation_model_1 = self.evaluer_classification( self.donnees_test, self.arbre)



        # Task 3
        self.faits_initiaux = donnees_entrainement
        self.regles = self.generer_regles(self.arbre)

        self.stat.calculer_statistiques(self.regles)


        #Task 4

        self.diagnostic = Diagnostic(self.regles,self.arbre)

        # Task 5
        id3_adv = ID3_ADV()

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
        self.rprs_diagnostic(caract_patient)
        print('***')


    def rprs_diagnostic(self,patient):
        """ affiche la représentation d'un diagnostique du patient. """

        diagnostic = self.diagnostic.diagnose_patient(patient)

        if diagnostic == None:

            return 'patient en bonne santé, continuez comme ça !'
        else:
            print("Diagnostic",diagnostic)
            print('Ensemble des changement à faire pour que le patient soit guéri:')
            nb_de_suggestion = 0
            for suggestion in diagnostic:
                for conds_suggestion in suggestion:
                    print('Il faut changer {} à {} '.format(conds_suggestion[0] ,conds_suggestion[1]))
                    nb_de_suggestion +=1
            #counts the suggestion
            self.stat.evaluer_diagnostique(nb_de_suggestion)

    def get_patients_sauves(self):
        """ retourne le nombre de patients nécéssitant 2 ou moins changements de paramètre pour etre en bonne santé"""
        return self.stat.trouver_nombre_patients_ok()


    def get_statistiques(self):
        """ fonction qui retourne tous les statistiques nécessaires """
        print('nb malades:')
        print(self.stat.get_nombre_malades(self.donnees_test))
