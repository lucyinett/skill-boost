import requests

endpoint = "http://dbpedia.org/sparql"
query = '''
prefix dbpprop: <http://dbpedia.org/property/>
prefix dbpedia-owl: <http://dbpedia.org/ontology/>
SELECT DISTINCT ?object WHERE {
  <http://dbpedia.org/resource/Computer_science> dbpprop:hasPropertyObject ?property .
  ?property rdf:type dbpedia-owl:Property .
  ?property rdfs:range ?range .
  ?range rdfs:subClassOf dct:StandardizedResource .
  ?property rdfs:domain ?subject .
  ?property rdfs:comment ?comment .
  MINUS { ?property rdfs:domain ?skipSubject . }
  OPTIONAL { ?property dbpprop:hasLanguage ?language . }
  OPTIONAL { ?property rdfs:label ?label . }
  OPTIONAL { ?comment schema:description ?description . }
  OPTIONAL { ?range dbpprop:hasDescription ?rangeDesc . }
  OPTIONAL { ?range rdfs:comment ?rangeComment . }
  FILTER (!CONTAINS(STR(?comment), "redirect"))
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" . }
} ORDER BY DESC(LANG(?object)) LIMIT 50 OFFSET 0'''

response = requests.post(endpoint, params={'format': 'json'}, headers={'Accept': 'application/sparql-results+json'}, data=query)

related_objects = set()
if response.status_code == 200:
    results = response.json()['results']['bindings']
    for result in results:
        print(result)
        obj_val = result['object']['value']
        if '"' not in obj_val:
            related_objects.add(obj_val)

# Retrieve readable names for URI
readable_objects = set()
for uri in related_objects:
    response = requests.get(f"http://lookup.dbpedia.org/{uri}")
    if response.ok:
        readable_objects.add(response.text.strip())

print(sorted(list(readable_objects)))