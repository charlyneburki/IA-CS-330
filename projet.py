from result_values import ResultValues

results = ResultValues()

arbre, faits_initiaux, regles, arbre_advance =results.get_results()
print('TACHE #1:')
print('Les statistiques de larbre resultant:')
results.stat.get_statistiques()
#print(arbre)

print('=-=-=-=-=-=-=-=-=-=-=-=-=')
print('TACHE #2:')
print('pourcentage de classifications correcte:')
print(results.evaluation_model_1)


#print('Exemplification :')
#for i in range(len(results.donnees_test)):
#   print(results.arbre.classifie(results.donnees_test[i]))

print('=-=-=-=-=-=-=-=-=-=-=-=-=')
print('TACHE #3:')
for regle in regles:
    print (regle)


print('=-=-=-=-=-=-=-=-=-=-=-=-=')
print('TACHE #4:')

#for i in range(len(results.donnees_test)):
    #print(i)
#   results.rprs_justification(results.donnees_test[i])

results.rprs_justification(results.donnees_test[72])

#print('nombre de patients sauvés (avec 2 ou moins changements):')
#nb_change_1, nb_change_2 = results.get_patients_sauves()


#print("nombre de patient sauvé avec 1 changement",nb_change_1)
#print("nombre de patient sauvé avec 2 changements",nb_change_2)

#results.get_statistiques()

#affiche en bon format la prédiction d'un patient
#print('exemplification d un patient diagnosé')
#results.rprs_justification(results.donnees_test[7])



print('=-=-=-=-=-=-=-=-=-=-=-=-=')
print('TACHE #5:')
print('arbre resultant:')
print(arbre_advance)
print('pourcentage de classifications correcte:')
print(results.evaluation_model_2)


print('=-=-=-=-=-=-=-=-=-=-=-=-=')
