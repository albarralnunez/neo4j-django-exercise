from .gedcom_parser import Gedcom
from .models import Person
from neomodel import db
from datetime import datetime


class GedcomUploader:

    def __init__(self, gedcom_file):
        self.data = Gedcom(gedcom_file)
        self.__persons = {}

    def __create_persons(self):
        for iden in self.data.element_dict():
            act_ele = self.data.element_dict()[iden]
            if act_ele.is_individual():
                name, surname = act_ele.name()
                gender = act_ele.gender()
                self.__persons[act_ele.pointer()] = Person(
                    name=name if name else None,
                    surname=surname if surname else None,
                    genere=gender if gender else None
                    ).save()

    def __marriage(self, act_ele):
        spouses = self.data.get_family_members(act_ele, "PARENTS")
        spouses_obj = [self.__persons[x.pointer()] for x in spouses]
        if len(spouses_obj) > 1:
            print 'warning'
            date, place = self.data.marriage(spouses[0], spouses[1])
            date = datetime.strptime(
                        date, "%Y-%m-%d")
            print 'warning'
            marriage = {
                'spouse': spouses_obj[1].id,
                'date': date
                # 'location': place
                }
            spouses_obj[0].add_marriage(marriage)
        return spouses_obj

    def __childs(self, act_ele, spouses):
        childs = self.data.get_family_members(act_ele, "CHIL")
        childs_obj = [self.__persons[x.pointer()] for x in childs]
        for spouse in spouses:
            for child in childs_obj:
                spouse.add_son(child.id)
        return childs_obj

    def __create_relations(self):
        for iden in self.data.element_dict():
            act_ele = self.data.element_dict()[iden]
            if act_ele.is_family():

                #  marriages
                spouses = self.__marriage(act_ele)

                #  childs
                self.__childs(act_ele, spouses)

                #  marriages test
                print 'Family:'
                print '  $spouses$'
                fam = self.data.get_family_members(act_ele, "PARENTS")
                if len(fam) > 1:
                    print self.data.marriage(fam[0], fam[1])
                for spouse in fam:
                    print '-------------------------------'
                    print '  ' + str(spouse.name())
                    print '  ' + str(spouse.pointer())
                    print '  ' + str(spouse.tag())
                    print '-------------------------------'

                # childs test
                print '    $childs$'
                for child in self.data.get_family_members(act_ele, "CHIL"):
                    print '-------------------------------'
                    print '    ' + str(child.name())
                    print '    ' + str(child.pointer())
                    print '-------------------------------'

    @db.transaction
    def upload(self):
        #  print self.data.element_dict()
        #  print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'

        #  all persons
        self.__create_persons()

        #  all families
        self.__create_relations()
