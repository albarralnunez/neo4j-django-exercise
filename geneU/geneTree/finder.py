from collections import Counter
from geneTree.models_person import Person


class finder:

    def find_persons(self, per):

        def __comp_peson(p1, p2):
                if not (p2.name or p2.surname or p2.second_surname):
                    return True
                else:
                    return (not ((p1.name == p2.name or
                            not p1.name or not p2.name) and
                            (p1.surname == p2.surname or
                            not p1.surname or not p2.surname) and
                            (p1.second_surname == p2.second_surname or
                            not p1.second_surname or not p2.second_surname)))

        per = Person.get(id=per)
        print per
        res = []
        death_ev_s = per.get_similar_death()
        res += death_ev_s
        lived_ev_s = per.get_similar_lived()
        res += lived_ev_s
        married_ev_s = per.get_similar_marriages()
        res += married_ev_s
        divorced_ev_s = per.get_similar_divorces()
        res += divorced_ev_s
        birth_adp_ev_s = per.get_similar_birth_adp()
        res += birth_adp_ev_s

        res = Counter(res)
        res = filter(lambda x: res[x] >= 3, res)

        print res

        res = [Person.get(id=x) for x in res]
        print [x.name for x in res]

        res = filter(lambda x: __comp_peson(per, x), res)
        print [x.name for x in res]
        return res
