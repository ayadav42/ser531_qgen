from openie import StanfordOpenIE
from owlready2 import *

import helper
import rules

properties = {
    'openie.affinity_probability_cap': 2 / 3
}

# def getQuestionsAndAnswer():
onto = get_ontology("/Users/amaryadav/PycharmProjects/Qgen/resources/qgen.owl").load()

# for cc in onto.classes():
#     print(cc, type (cc))
#
for prop in onto.properties():
    ontoProp = prop
    print(prop, type(prop))

amar = onto.Person("Amar")
aman = onto.Person("Aman")
amar.hasBrother.append(aman)

print("amar", amar)

for prop in amar.get_properties():
    print(prop, type (prop))

# amar.hasBrother(aman)
# print(amar.hasBrother, type (amar.hasBrother))
