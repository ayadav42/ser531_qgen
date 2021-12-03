from openie import StanfordOpenIE
from owlready2 import *

from src.helper import *
from src.rules import *


def getQuestionsAndAnswersFromText(text):
    properties = {
        'openie.affinity_probability_cap': 2 / 3
    }

    # def getQuestionsAndAnswer():
    onto = get_ontology(
        "./resources/qgen.owl").load()

    # text2 = "Sam is the father of Tom. Tara is the wife of Sam."
    # text = "Sam is the father of Tom. Tara is the wife of Sam. Sarah is the sister of Tom."
    # text = "Sam is the son of Tom. Tom is the parent of Carl. Kevin is the brother of Carl."
    print(text)

    with onto:
        class Person(Thing):
            pass

        def getPerson(name):
            ans = None
            for person in onto.get_instances_of(Person):
                # for person in onto.get_instances_of(onto.Person):
                if (person._name).lower() == name.lower():
                    ans = person
                    break

            if ans is None:
                # ans = onto.Person(name)
                ans = Person(name, namespace=onto)

            return ans

        filteredTriples = []

        with StanfordOpenIE(properties=properties) as client:
            for triple in client.annotate(text):
                prop = closest_relation(triple['relation'], onto)

                if prop is not None:
                    triple['subject'] = getPerson(triple['subject'])
                    triple['relation'] = prop
                    triple['object'] = getPerson(triple['object'])
                    filteredTriples.append(triple)

        for triple in filteredTriples:
            s = triple['subject']
            p = triple['relation']
            o = triple['object']
            name = p._name
            s.__setattr__(p._name, [o])

    def getQuestionAndAnswers(triplet):
        predicate = triplet[1]
        predicate = predicate.namespace.base_iri + predicate._name

        obj = triplet[2]
        obj = obj.namespace.base_iri + obj._name

        query = "SELECT ?x WHERE{ ?x <%s> <%s>. FILTER (?x != <%s>)}" % (
            predicate, obj, obj)

        # print("query", query)

        answers = list(
            default_world.sparql(
                query
            )
        )

        ansList = []
        for ans in answers:
            ansList.append(ans[0]._name)

        qAns = (
            "Who " +
            " ".join(lower_camel(triplet[1]._name)
                     ) + " " + triplet[2]._name + "?",
            ansList
        )

        # print(qAns)
        return qAns

    qAnswers = {}

    sync_reasoner_pellet(infer_property_values=True,
                         infer_data_property_values=True)

    infer = get_ontology("http://inferrences/")

    print("inferredTriples1-------------------------------------------------------")
    inferredTriples1 = set()
    for s, p, o in infer.get_triples():
        # print(s, p, o)
        x = default_world._entities.get(s)
        y = default_world._entities.get(p)
        z = default_world._entities.get(o)
        if (not x or not y or not z):
            pass
        else:
            inferredTriples1.add((x, y, z))
            # print("sub:", x, " pred:", y, " obj: ", z)

    # for triple in inferredTriples1:
    #     print(triple)
        # qAnswers.append(getQuestionAndAnswers(triple))

    # print("inferredTriples2-------------------------------------------------------")

    with onto:
        for rule in rules:
            # print(rule)
            ruleImp = Imp()
            ruleImp.set_as_rule(rule)

    sync_reasoner_pellet(infer_property_values=True,
                         infer_data_property_values=True)
    inferredTriples2 = set()
    for s, p, o in infer.get_triples():
        # print(s, p, o)
        x = default_world._entities.get(s)
        y = default_world._entities.get(p)
        z = default_world._entities.get(o)
        if (not x or not y or not z):
            # print("sub:", x, " pred:", y, " obj: ", o)
            pass
        else:
            if x is not z:
                inferredTriples2.add((x, y, z))

    for triple in inferredTriples2:
        predicate = triple[1]._name
        if (
            (not predicate.startswith("has", 0, len(predicate))) and
            ("Related" not in predicate)
        ):
            qa = getQuestionAndAnswers(triple)
            qAnswers[qa[0]] = qa

    # print("question and answers----------------------------------------------------")
    # for qAnswer in qAnswers:
    #     print(qAnswer)

    return qAnswers
