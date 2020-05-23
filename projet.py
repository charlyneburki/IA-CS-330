from result_values import ResultValues

results = ResultValues()

arbre, faits_initiaux, regles, arbre_advance =results.get_results()
print('TACHE #1:')
print('arbre resultant:')
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
print('Il y a ' + str(len(regles)) + ' règles générées.')
for regle in regles:
    print (regle)

print('=-=-=-=-=-=-=-=-=-=-=-=-=')
print('TACHE #4:')
#affiche en bon format la prédiction d'un patient
print('exemplification d un patient diagnosé')
#results.rprs_justification(results.donnees_test[7])

#for patient in results.donnees_test:
#    results.diagnose_patient(patient)
   
print('nombre de patients sauvés (avec 2 ou moins changements):')
#nb_change_1, nb_change_2 = results.get_patients_sauves()

#print(nb_change_1)
#print(nb_change_2)

#results.get_statistiques()

print('=-=-=-=-=-=-=-=-=-=-=-=-=')
print('TACHE #5:')
print('arbre resultant:')
print(arbre_advance)
print('pourcentage de classifications correcte:')
print(results.evaluation_model_2)


print('=-=-=-=-=-=-=-=-=-=-=-=-=')
