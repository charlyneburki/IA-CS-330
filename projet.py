from result_values import ResultValues

results = ResultValues()

print('arbre resultant:')
#print(results.arbre)

print('pourcentage de classifications correcte:')
print(results.evaluer_model())


print('Exemplification :')
for i in range(len(results.faits_initiaux)):
   print(results.arbre.classifie(results.faits_initiaux[i]))

print('****')
print('part 3')
print('Affichage des règles trouvées pour le modèle:')
regles = results.regles
print('Il y a ' + str(len(regles)) + ' règles générées.')
for regle in regles:
    print (regle)

    

#checks the % correctly classified
print('pourcentage de classification correcte basé sur les règles:')
print(results.evaluer_regles())

#affiche en bon format la prédiction d'un patient
results.rprs_justification(results.faits_initiaux[7])

for patient in results.faits_initiaux:
    results.rprs_justification(patient)
    
#TO DO -- restraindre le nombre de changements pour le diagnostique à MAXIMUM 2 changements
