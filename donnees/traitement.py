
class TraitementDonnees:
    """ Traite les données fournies. """

    def import_donnees(self, filepath):
        """ Importe les données d'entrainement à partir du filepath """
    #impore les données sous forme de dictionnaire
        from csv import DictReader
        # open file in read mode
        with open(filepath, 'r', encoding='UTF-8-sig') as read_obj:
            # pass the file object to DictReader() to get the DictReader object
            dict_reader = DictReader(read_obj)
            # get a list of dictionaries from dct_reader
            donnees = list(dict_reader)
            # print list of dict i.e. rows
            final_donnees = []
            for donnee in donnees:
                    sample = [donnee['target']]
                    del donnee['target']
                    sample.append(donnee)
                    final_donnees.append(sample)
        return final_donnees
    
    def import_donnees_test(self, filepath):
        from csv import DictReader
        # open file in read mode
        with open(filepath, 'r', encoding='UTF-8-sig') as read_obj:
            # pass the file object to DictReader() to get the DictReader object
            dict_reader = DictReader(read_obj)
            # get a list of dictionaries from dct_reader
            donnees = list(dict_reader)
        return donnees
