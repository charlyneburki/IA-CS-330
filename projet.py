from result_values import ResultValues
from donnees.traitement import TraitementDonnees

treat = TraitementDonnees()

results = ResultValues()

print('arbre resultant:')
print(results.arbre)

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

predicted = []
for i in range(len(results.donnees_test)):
    print('patient ' + str(i+1))
    print('final: ')
    r = results.justification_prediction(results.donnees_test[i])
    print(r)
    predicted.append(r[-1][-1])
    

#checks the % correctly classified
actual = []
donneess = treat.import_donnees_test('res/test_public_bin.csv')
for donnee in donneess:
    rep = results.arbre.classifie(donnee)
    actual.append(rep[-1])

#problem -- only 40% of correctly classified patients ? 
print(results.stat.evaluer_similitude(predicted,actual))
