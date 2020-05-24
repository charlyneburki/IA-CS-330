from result_values import ResultValues

results = ResultValues()

arbre, faits_initiaux, regles, arbre_advance =results.get_results()
print('TACHE #1:')
print("Les statistiques de l'arbre resultant:")
results.stat.get_statistiques()
#print(arbre)

print('=-=-=-=-=-=-=-=-=-=-=-=-=')
print('TACHE #2:')
print('pourcentage de classifications correcte:')
print(results.evaluer_classification(results.donnees_test,results.arbre))


print('=-=-=-=-=-=-=-=-=-=-=-=-=')
print('TACHE #3:')
print('Il y a',len(regles),"règles générées par l'algorithme")
for regle in regles:
    print (regle)


print('=-=-=-=-=-=-=-=-=-=-=-=-=')
print('TACHE #4:')

for i in range(len(results.donnees_test)):
   print('***')
   print(i)
   #c'est de cette manière qu'on affiche un patient ansis que la justification de classification
   #et le diagnostique trouvé
   results.rprs_justification(results.donnees_test[i])

print('nombre de patients sauvés (avec 2 ou moins changements):')
nb_change_1, nb_change_2 = results.stat.get_nb_changement()

print("nombre de patient sauvé avec 1 changement",nb_change_1)
print("nombre de patient sauvé avec 2 changements",nb_change_2)

print('=-=-=-=-=-=-=-=-=-=-=-=-=')
print('TACHE #5:')
print('arbre resultant:')
print(arbre_advance)
print('pourcentage de classifications correcte:')
print(results.evaluer_classification(results.donnees_test_adv,results.arbre_advance))


print('=-=-=-=-=-=-=-=-=-=-=-=-=')
