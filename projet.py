from result_values import ResultValues



results = ResultValues()

print('arbre resultant:')
#print(results.arbre)

print('pourcentage de classifications correcte:')
print(results.evaluer_model())


print('Exemplification :')
for i in range(len(results.donnees_test)):
    print(results.arbre.classifie(results.donnees_test[i]))

#trouver les règles à partir de l'arbre établi. 
#regles = results.arbre.gen_regles()
#print(len(regles))

