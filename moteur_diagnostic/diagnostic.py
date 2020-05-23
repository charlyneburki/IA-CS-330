

class Diagnostic:

    def __init__(self,regles,arbre):
        self.arbre = arbre
        self.good_rules = self.identifie_parametres_bons(regles)
        #self.suggestion = self.diagnose_patient(patient,justification)


    def identifie_parametres_problematiques(self, rules):
            sick_rule = []

            for rule in rules:
                if rule[-1][-1]=='1' :
                    sick_rule.append([rule])

            for rule in sick_rule:
                print(rule)

    def identifie_parametres_bons(self,rules):
        good_condition = []
        list_condition =[]
        todo_regles = rules

        for regle in todo_regles:
            if regle[-1][-1] == '0':
                rep=regle.pop()
                for condition in regle:
                    good_condition.append(condition)
                regle.append(rep)

        for g_condition in good_condition:
            nb_occurence = good_condition.count(g_condition)
            if ((g_condition,nb_occurence) not in list_condition) and not(g_condition[0]== 'sex' or g_condition[0]== 'age'):
                list_condition.append((g_condition,nb_occurence))

        self.list_condition = list_condition.sort(key=self.takeSecond,reverse = True)
        print("list_condition",list_condition)
        return list_condition

    def find_diagnostic(self, patient):
        """ basé sur les données du patient ainsi que les règles des patients en bonne santé établies à partir de l'arbre, cette fonctionne va trouver la meilleure règle correspondante au conditions du patient. """

        list_condition = self.good_rules
        diagnostic_rules = []
        count_best =0
        minimal_best = 0
        final_diagnostic_rule = []
        list_a_etudier=[]

        nb_de_cond_a_etudier = 0
        for a_etudier in self.good_rules:
            if a_etudier[0] not in patient:
                nb_de_cond_a_etudier +=1
                #print("condition pas dans patient",a_etudier[0],nb_de_cond_a_etudier)
                list_a_etudier.append(a_etudier[0])



        list_fixe = list_a_etudier
        liste_courante = list_fixe

        #test toute les changements possible qui sont proposé dans la liste diagnostic rules

        #print(list_condition)

        iteration = 1
        futur_liste =[]
        first_set_of_iteration = True
        condition=[]

        while (iteration < 100000):

            print("iteration",iteration)


            if iteration > nb_de_cond_a_etudier:
                liste_courante = futur_liste
                nb_de_cond_a_etudier = len(liste_courante)
                iteration = 1
                first_set_of_iteration = False
                print("je passe ici et le liste[0] est",liste_courante[0])


            test = patient.copy()

            if first_set_of_iteration:
                condition = [liste_courante[0]]
                #for cond_etudie in condition:
                    #print("c'est ici",cond_etudie)
                    #print(cond_etudie[0],cond_etudie[1])
            else:
                condition = liste_courante[0]

            #print("condition ic ",condition)

            #print(condition)

            #if(iteration > 1):
                #print("futur liste[0]",futur_liste[0])

            for cond_etudie in condition:
                #print("je passe ici",cond_etudie[0],cond_etudie[1])
                for key,values in patient.items():
                    if key == cond_etudie[0]and values != cond_etudie[1]:

                        #print("je passe ici2")
                        #print("voila les valeurs étudié",key,values)
                        test[key]=cond_etudie[1]
                        #print("voila le changement", cond_etudie)
                #print("diagnostique sur test",rep)

            rep = self.arbre.classifie(test)[-1]
            print("avec le changement le patient est",rep)
            if rep == '0':
                final_diagnostic_rule.append(condition)
                #print("diagnostique trouvé!",final_diagnostic_rule)
                #print("le patient sans changement",patient)
                #print("le patient avec changement",test)
                return final_diagnostic_rule
            else:
                #print("ici",list_courante[0])
                #print("et la aussi",cond_etudie)
                liste_courante.remove(liste_courante[0])
                #print("er la aussi",cond_etudie)

                    #print("et la",ensemble_de_regle_diag[0])

                    #génère la suite de la liste
                #print("list courante",liste_courante,"\n")
                futur_condition = condition
                for cond in list_fixe: #A AMELIORER POUR QU'IL NE FASSE PAS DE BOUCLE
                        #print("alors la y'a un soucis",cond[0])
                        #print("alors la y'a un 2 soucis",condition[0])
                    futur_condition.append(cond)
                    #print("futur condition",futur_condition)
                    futur_liste.append(futur_condition)
                    futur_condition = [cond_etudie]
                        #print(suite)
                #print("futur liste", futur_liste)

                #print("nouvelle liste_courante", liste_courante)
            iteration += 1




        print("Pas de combinaison possible pour le diagnostique")
        return []


                #ensemble_de_regle_diag.pop()

            #for condition in ensemble_de_regle_diag:
             #   test = patient.copy()
              #  for key,values in patient.items():
                    #print(key,values)
               #     if key == condition[0][0] and values != condition[0][1]:
                #        ensemble_de_regle_diag.append(condition[0])
                 #       print(key,values)
                  #      test[key]=condition[0][1]
                        #print("newvalues",key,values)
                    #print("on va changer",condition[0])
                    #print("avant changement",patient)
                    #print("changement du patient",test)
                       # rep = self.arbre.classifie(test)[-1]
                      #  if rep == '0':
                       #     print("diagnostique trouvé!",ensemble_de_regle_diag)
                        #    return ensemble_de_regle_diag
                        #else:
                         #   ensemble_de_regle_diag.pop()
            #if iteration == 2:
             #   for condition in list_condition:
              #      ensemble_de_regle_diag.append(condition[0])
               #     new_list_condition = list_condition.copy()
                #    for new_cond in new_list_condition:
                 #       if new_cond[0][0] = condition[0][0]:
                  #          delete(new_list_condition[new_cond[0]])
                   # for condition in

            #iteration += 1
        print("Pas de combinaison possible pour le diagnostique")
        return []




            #for key,value in patient.items():
             #   print(key,value)
                #if condition[0]== caract:
                    #("condition dans la liste",condition[0])
            #
             #   print("condtion pas dans la liste",condition[0])
              #  test[condition[0]]=condition[0]

            #else:
               # print("condition dans la liste",condition[0])

        #
        #        print(test)
        #        print("cond de suggest",conds_suggestion[0])
        #        for condition,value in test.items():
        #            if condition == conds_suggestion[0]:
        #               test[condition] = conds_suggestion[1]
        #amongst the best candidates, finds the rule that has the least divergence in the conditions
        for diagnostic_rule in diagnostic_rules:
            for conditions in diagnostic_rule:
                for condition_rule,condition_patient in zip(conditions,patient.items()):
                    if condition_rule[0]==condition_patient[0] and condition_rule[1] == condition_patient[1]:
                        count_best += 1
            if count_best > minimal_best :
                minimal_best = count_best
                final_diagnostic_rule = diagnostic_rule

        return final_diagnostic_rule

    def BFS_Search(self,ensemble_de_regle_diag,patient):

        rep=[]
        return rep

    def suggest_diagnostic(self, patient, diagnostic_rule):
        """ basé sur une règle de diagnostique passé en paramètre, cette fonctionne retourne les suggestions de changement des paramètres du patient pour qu'il soit en bonne santé """



        #no diagnostics to do
        if justification[-1][-1] == '0':
            return None
        else:
            change_suggestion = []
            for cond_patient in justification[:-1]:
                for conds_rule in diagnostic_rule:
                    for cond_rule in conds_rule:
                        #only takes in consideration suggestions that don't involve age or sex
                        if cond_rule[0] == cond_patient[0] and cond_rule[1] != cond_patient[1] and not(cond_rule[0] == 'age' or cond_rule[0] == 'sex'):
                            change_suggestion.append(cond_rule)


            print("Suggestion",change_suggestion)
            return change_suggestion

    def diagnose_patient(self,patient):#,justification):
        """ gère le diagnostique du patient"""
        rep = self.arbre.classifie(patient)[-1]
        print("avec le changement le patient est",rep)
        if rep == '0':
            print("je passe ici")
            diagnostic = None
        else:
            diagnostic = self.find_diagnostic(patient)
        #suggestion = self.suggest_diagnostic(patient,diagnostic)

        return diagnostic
    # take second element for sort
    def takeSecond(elem,elem1):
        #print("elem",elem,"elem1",elem1)
        return elem1[1]




