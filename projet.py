from moteur_id3.noeud_de_decision import NoeudDeDecision
from moteur_id3.id3 import ID3
from donnees.traitement import TraitementDonnees
from donnees.statistiques import StatistiquesID3

#partie 1

importation = TraitementDonnees()
donnees_entrainement = importation.import_donnees('res/train_bin.csv')

id3 = ID3()
arbre = id3.construit_arbre(donnees_entrainement)
print('Arbre de décision :')
print(arbre)

#calculs à faire pour partie 1
stat = StatistiquesID3()
#trouve le nombre d'enfants de l'arbre
#et autres stat A COMPLETER
nb_enfants = len(arbre.enfants)

#partie 2

donnees_test = importation.import_donnees_test('res/test_public_bin.csv')

#resultats de la classification
predicted = []
actual = []

print('Exemplification :')

for donnee in donnees_test:
    rep = arbre.classifie(donnee)
    actual.append(donnee['target'])
    #print(rep)
    #takes the last character of rep i.e the result of classification
    predicted.append(rep[-1])

print('pourcentage de classifications correctes :')
print(stat.evaluer_similitude(predicted,actual))

#partie 3

