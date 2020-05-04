from moteur_id3.noeud_de_decision import NoeudDeDecision
from moteur_id3.id3 import ID3
from donnees.traitement import TraitementDonnees

importation = TraitementDonnees()
donnees = importation.import_donnees('res/train_bin.csv')

id3 = ID3()
arbre = id3.construit_arbre(donnees)
print('Arbre de décision :')
print(arbre)
print()

#print('Exemplification :')
#print(arbre.classifie({'age': 'midlife','competition': 'no','type': 'hardware'}))

#print('printout')
#print(arbre.__repr__())
#print('done')
