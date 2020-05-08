from result_values import ResultValues



results = ResultValues()

print('arbre resultant:')
#print(results.arbre)

print('pourcentage de classifications correcte:')
print(results.evaluer_model())


print('Exemplification :')
#for i in range(len(results.donnees_test)):
#    print(results.arbre.classifie(results.donnees_test[i]))

#trouver les règles à partir de l'arbre établi.
#regles = results.arbre.gen_regless()
#rules = results.arbre.chemin
#print(len(rules))
#for i in range(len(rules)):
#    print(rules[i])
#    print('---')

print('****')
print('part 3')
print('Prints the rules decided for each patient: ')
regles = results.regles

for i in range(len(results.donnees_test)):
    print('patient ' + str(i+1))
    print('final: ')
    r = results.justification_prediction(results.donnees_test[i])
    print(r)

#checks the % correctly classified
predicted = []
for donnee in results.donnees_test:
    rep = results.arbre.classifie(donnee)
    predicted.append(rep[-1])

actual = []
for rr in r:
    actual.append(rr[-1])

#problem -- only 40% of correctly classified patients ? 
print(results.stat.evaluer_similitude(predicted,actual))
