

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

        final_diagnostic_rule = []
        list_a_etudier=[]

        liste_fixe =[]
        nb_de_cond_a_etudier = 0
        for a_etudier in self.good_rules:
            if a_etudier[0] not in patient:
                nb_de_cond_a_etudier +=1
                list_a_etudier.append(a_etudier[0])

        liste_fixe = list_a_etudier
        liste_courante = liste_fixe

        #test toute les changements possible qui sont proposé dans la liste diagnostic rules


        iteration = 1
        futur_liste =[]
        first_set_of_iteration = True

        while (iteration < 100000):

            if iteration > nb_de_cond_a_etudier:
                liste_courante = futur_liste

                futur_liste = []

                nb_de_cond_a_etudier = len(liste_courante)


                iteration = 1

                first_set_of_iteration = False

                for a_etudier in self.good_rules:
                    if a_etudier[0] not in patient:
                        liste_fixe.append(a_etudier[0])


            test = patient.copy()
            condition=[]

            if first_set_of_iteration:
                condition = [liste_courante[0]]
            else:
                condition = liste_courante[0]

            for cond_etudie in condition:
                for key,values in patient.items():
                    if key == cond_etudie[0]and values != cond_etudie[1]:
                        #change les conditions d'un patient "test", travail sur une copy du patient original
                        test[key]=cond_etudie[1]

            rep = self.arbre.classifie(test)[-1]

            if rep == '0':
                final_diagnostic_rule.append(condition)

                return final_diagnostic_rule
            else:

                liste_courante.remove(liste_courante[0])

                futur_condition = []
                for cond in condition:
                    futur_condition.append(cond)

                for cond in liste_fixe :
                    param_cond = []
                    for condi in condition:
                        for param in condi:
                            param_cond.append(param)


                    if cond[0] not in param_cond:
                        futur_condition.append(cond)
                        futur_liste.append(futur_condition)
                        futur_condition = []
                        for cond in condition:
                            futur_condition.append(cond)
            iteration += 1

        print("Pas de combinaison possible pour le diagnostique")
        return []


    def diagnose_patient(self,patient):
        """ gère le diagnostique du patient"""
        condition_patient = self.arbre.classifie(patient)[-1]
        if condition_patient == '0':
            diagnostic = None
        else:
            diagnostic = self.find_diagnostic(patient)
        return diagnostic

    # take second element for sort
    def takeSecond(elem,elem1):
        return elem1[1]




