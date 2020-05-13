
class Diagnostic:

    def identifie_parametres_problematiques(self, rules):
            sick_rule = []
            
            for rule in rules:
                if rule[-1][-1]=='1' :
                    sick_rule.append([rule])
            
            for rule in sick_rule:
                print(rule)
    
    def identifie_parametres_bons(self,rules):
        good_rules = []
        
        for rule in rules:
            if rule[-1][-1] == '0':
                good_rules.append([rule])
        
        return good_rules
    
    
            
            
