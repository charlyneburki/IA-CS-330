

class Diagnostic:

    def __init__(self,regles,arbre):
        self.arbre = arbre
        self.good_rules = self.identifie_parametres_bons(regles)

    def identifie_parametres_problematiques(self, rules): #fonction pas utilisé à voir si on garde
            sick_rule = []
            for rule in rules:
                if rule[-1][-1]=='1' :
                    sick_rule.append([rule])

            for rule in sick_rule:
                print(rule)

    def identifie_parametres_bons(self,regles):
        good_conditions = []
        list_condition =[]

        for regle in regles:
            if regle[-1][-1] == '0':
                rep=regle.pop()
                for condition in regle:
                    good_conditions.append(condition)
                regle.append(rep)

        for g_condition in good_conditions:
            nb_occurence = good_conditions.count(g_condition)
            if ((g_condition,nb_occurence) not in list_condition) and not(g_condition[0]== 'sex' or g_condition[0]== 'age'):
                list_condition.append((g_condition,nb_occurence))

        self.list_condition = list_condition.sort(key=self.takeSecond,reverse = True)
        return list_condition

    def find_diagnostic(self, patient):
        """ basé sur les données du patient ainsi que les règles des patients en bonne santé établies à partir de l'arbre, cette fonctionne va trouver la meilleure règle correspondante au conditions du patient. """

        #contiendra la liste des conditions à changer
        final_diagnostic_rule = []



        liste_fixe = self.condition_not_in_patient(patient)
        nb_de_condition_a_etudier = len(liste_fixe)

        #liste qui contiendra toute les possibilités de diagnostique à considérer, est initié
        #avec la liste de toutes les possibilités avec une seule condition à tester
        liste_courante = liste_fixe


        #liste qui contiendra les futurs conditions à explorer générer par l'algorithme
        futur_liste =[]

        #Valable pour les cas où le nombre de condition à considérer en même temps vaut 1
        first_set_of_iteration = True
        iteration = 1

        #algorithme BFS qui explorer toutes les combinaisons de conditions possible,
        #d'abors avec une condition, puis deux, puis trois...
        while (iteration < 100000):

            if iteration > nb_de_condition_a_etudier:
            #si cette condition est remplie, cela veut dire que l'ensemble des conditions à tester
            #fut testé, maintenant la liste des futurs possibilité à considérer devient la liste courante
            #et la liste futur devient vide
                liste_courante = futur_liste
                futur_liste = []
                nb_de_cond_a_etudier = len(liste_courante)


                iteration = 1

                first_set_of_iteration = False

                liste_fixe = self.condition_not_in_patient(patient)

            #tout les changements vont être effectuer sur une copie du patient afin de ne pas changer
            #le patient de base
            test = patient.copy()

            #contiendra l'ensemble des conditions considérés à cette itération
            condition=[]

            if first_set_of_iteration:
                condition = [liste_courante[0]]
            else:
                condition = liste_courante[0]

            for cond_etudie in condition:
                for key,values in patient.items():
                    #si la condition présente le même attribut mais pas la même valeur
                    #que la condition présente dans les conditions positive
                    #on essaye de changer la condition dans le patient test et on regarde
                    #si le patient test est guérit selon notre arbre
                    if key == cond_etudie[0] and values != cond_etudie[1]:
                        test[key]=cond_etudie[1]

            rep = self.arbre.classifie(test)[-1]

            if rep == '0':
                #le patient est guérit, l'algorithme retourne l'ensemble des conditions
                #à changer
                final_diagnostic_rule.append(condition)
                return final_diagnostic_rule
            else:
            #algorithme BFS genère la future liste des conditions à considérer
                liste_courante.remove(liste_courante[0])

                futur_condition = self.copy_list(condition)

                #Soit l'ensemble de conditions étudiés cette itération, on va lui ajouter
                #une condition parmis la liste de conditions de départ qui ne partage pas
                #d'attribut en commun avec l'ensemble considéré cette itération
                #par exemple : si ('cp' = '0') est considéré cette itération
                #on va le fusionner avec une condition qui ne possède pas l'attribut 'cp'
                #-->[('cp' = '0')('ca' = 1)]
                for cond in liste_fixe :
                    ensemble_parametre = []
                    for ensemble_param in condition:
                        for param in ensemble_param:
                            ensemble_parametre.append(param)


                    if cond[0] not in ensemble_parametre:
                        futur_condition.append(cond)
                        futur_liste.append(futur_condition)
                        futur_condition = self.copy_list(condition)

            iteration += 1

        print("Pas de combinaison possible pour le diagnostique trouvé en 100'000 combinaison")
        return []


    def diagnose_patient(self,patient):
        """ gère le diagnostique du patient"""
        condition_patient = self.arbre.classifie(patient)[-1]
        if condition_patient == '0':
            diagnostic = None
        else:
            diagnostic = self.find_diagnostic(patient)
        return diagnostic

    def condition_not_in_patient(self,patient):
        list_condition_a_etudier=[]
        for a_etudier in self.good_rules:
            if a_etudier[0] not in patient:
                list_condition_a_etudier.append(a_etudier[0])
        return list_condition_a_etudier



    #fonction qui sert pour ordonner une liste
    def takeSecond(elem,elem1):
        return elem1[1]

    #effectue une copie d'une liste
    def copy_list(self,liste):
        copie = []
        for element in liste:
            copie.append(element)
        return copie





