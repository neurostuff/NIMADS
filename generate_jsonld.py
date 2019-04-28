import json
from collections import defaultdict
import os

defs = json.load(open('definitions.json', 'r'))

classes = defaultdict(list)
props = defaultdict(lambda: defaultdict(list))

wrap = lambda x: "nimads:{}".format(x) if ':' not in x else x

for t_name, data in defs.items():
    for p_name, p_type in data['properties']:
        ## Type properties
        classes[t_name].append({
            "@id": wrap(p_name),
            "schema:domainIncludes": {"@id": wrap(t_name)}
        })
        # Property mappings
        props[p_name]["domainIncludes"].append({"@id": wrap(t_name)})
        props[p_name]["rangeIncludes"].append({"@id": wrap(p_type)})

        if 'nimads' in p_type:
            p_type = p_type.split(':')[1]
            classes[p_type].append({
                "@id": wrap(p_name),
                "schema:rangeIncludes": {"@id": wrap(p_type)}
            })

context = {
    "schema": "http://schema.org/",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "nimads": "http://neurostuff.org/nimads/"
}

for c, c_props in classes.items():
    graph = [
        {
            "@id": wrap(c),
            "@type": "rdfs:Class",
            "rdfs:comment": "A NIMADS {}".format(c),
            "rdfs:label": c,
            "rdfs:subClassOf": {"@id": "schema:Thing"}
        }
    ] + c_props

    data = {
        "@context": context,
        "@graph": graph
    }

    with open(os.path.join('nimads', c + '.jsonld'), 'w') as f:
        json.dump(data, f, indent=2)

for c, entries in props.items():
    data = {
        "@context": context,
        "@id": wrap(c),
        "@type": "rdf:Property",
        "rdfs:label": c
    }
    data.update(entries)
    with open(os.path.join('nimads', '_' + c + '.jsonld'), 'w') as f:
        json.dump(data, f, indent=2)
