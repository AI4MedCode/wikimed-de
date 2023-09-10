Code for the paper **[WikiMed-DE: Constructing a Silver-Standard Dataset for German Biomedical Entity Linking using Wikipedia and Wikidata, 2023, Yi Wang, Corina Dima, Steffen Staab, Wikidata workshop](https://openreview.net/forum?id=5dQ7YDSYya)**

---

WikiMed-DE is a German biomedical Wikipedia dataset serving as a silver standard for biomedical entity linking tasks. Every sample in WikiMed-DE contains a unique Wikipedia page id, url, title, text and structured information mapped from Wikidata, namely qid, cui, tui, semantic type, wikidata_cui, mesh, mesh_cui, doid, doid_cui and mentions. In WikiMed-DE, we extracted every hyperlinked text span in Wikipedia articles as a mention, which typically refers to a reference or allusion to a specific person, place, event, or some specific concepts. Usually, each hyperlinked text span can be link to other Wikipedia articles. Each mention in WikiMed-DE contains its title (named mention in WikiMed-DE), start_index, end_index structured information mapped from Wikidata. More details can be found in https://openreview.net/forum?id=5dQ7YDSYya

  
WikiMed-DE will be stored as JSON format with one document per line. Each document has the following structure:

```

{'id': '3286460',
 'url': 'https://de.wikipedia.org/wiki?curid=3286460',
 'title': 'Filamin',
 'text': 'Filamine "(FLN)" sind Proteine bei Eukaryoten und gehören zu den Aktin-bindenden Proteinen "(ABP)". Sie sind an der Quervernetzung von Aktinfilamenten, einem Hauptbestandteil des Zytoskeletts, sowie der Vernetzung von Aktinfilamenten mit Proteinen in der Zellmembran beteiligt.',
 'qid': 'Q410803',
 'cui': ['C0127603', 'C0060383'],
 'tui': ['T116', 'T123'],
 'semantic type': ['Amino Acid, Peptide, or Protein',
  'Biologically Active Substance'],
 'mesh': 'D064448',
 'mesh_cui': ['C3887933', 'C0127603', 'C1612831', 'C1612279', 'C0060383'],
 'doid': 'None',
 'doid_cui': [],
 'mentions': [{'mention': 'Eukaryoten',
   'start_index': 35,
   'end_index': 45,
   'mention_link': 'https://de.wikipedia.org/wiki/Eukaryoten',
   'qid': 'Q19088',
   'cui': ['C0684063'],
   'tui': ['T204'],
   'semantic type': ['Eukaryote'],
   'mesh': 'D056890',
   'mesh_cui': ['C0684063'],
   'doid': 'None',
   'doid_cui': []},
  {'mention': 'Aktin-bindenden Proteinen',
   'start_index': 65,
   'end_index': 90,
   'mention_link': 'https://de.wikipedia.org/wiki/Aktin-bindendes%20Protein',
   'qid': 'None',
   'cui': [],
   'tui': [],
   'semantic type': [],
   'mesh': 'None',
   'mesh_cui': [],
   'doid': 'None',
   'doid_cui': []},
  {'mention': 'Quervernetzung',
   'start_index': 116,
   'end_index': 130,
   'mention_link': 'https://de.wikipedia.org/wiki/Quervernetzung',
   'qid': 'Q898597',
   'cui': [],
   'tui': [],
   'semantic type': [],
   'mesh': 'None',
   'mesh_cui': [],
   'doid': 'None',
   'doid_cui': []},
  {'mention': 'Aktinfilament',
   'start_index': 135,
   'end_index': 148,
   'mention_link': 'https://de.wikipedia.org/wiki/Aktinfilament',
   'qid': 'Q185269',
   'cui': ['C0022142',
    'C0001271',
    'C0002278',
    'C0005186',
    'C0016890',
    'C0002240',
    'C1180307',
    'C0017019'],
   'tui': ['T116', 'T123'],
   'semantic type': ['Amino Acid, Peptide, or Protein',
    'Biologically Active Substance'],
   'mesh': 'D000199',
   'mesh_cui': ['C0022142',
    'C0001271',
    'C0002278',
    'C0005186',
    'C0016890',
    'C0002240',
    'C1180307',
    'C1317971',
    'C0017019'],
   'doid': 'None',
   'doid_cui': []},
  {'mention': 'Zytoskelett',
   'start_index': 179,
   'end_index': 190,
   'mention_link': 'https://de.wikipedia.org/wiki/Zytoskelett',
   'qid': 'Q154626',
   'cui': ['C0010853', 'C0086623', 'C0010835', 'C0010851'],
   'tui': ['T026'],
   'semantic type': ['Cell Component'],
   'mesh': 'D003599',
   'mesh_cui': ['C0010853', 'C0086623', 'C0010835', 'C0010851'],
   'doid': 'None',
   'doid_cui': []},
  {'mention': 'Zellmembran',
   'start_index': 255,
   'end_index': 266,
   'mention_link': 'https://de.wikipedia.org/wiki/Zellmembran',
   'qid': 'Q29548',
   'cui': ['C0007603'],
   'tui': ['T026'],
   'semantic type': ['Cell Component'],
   'mesh': 'D002462',
   'mesh_cui': ['C0007603'],
   'doid': 'None',
   'doid_cui': []},
  {'mention': 'Zell-Zell-',
   'start_index': 338,
   'end_index': 348,
   'mention_link': 'https://de.wikipedia.org/wiki/Zellkontakt',
   'qid': 'Q189073',
   'cui': [],
   'tui': [],
   'semantic type': [],
   'mesh': 'None',
   'mesh_cui': [],
   'doid': 'None',
   'doid_cui': []}]}

```

  

Running the code

---
Step 1 - Obtaining German Wikipedia Articles:
1. Downloading the German Wikipedia articles dewiki-20230620-pages-articles-multistream.xml.bz2 from **[German Wikipedia dump](https://dumps.wikimedia.org/dewiki/20230620/)**
2. Using **[WikiExtractor](https://github.com/attardi/wikiextractor)** to extract the clean text from Wikipedia database backup dump. Follow the instructions of WikiExtractor to run the command line: 
```

python -m wikiextractor.WikiExtractor dewiki-20230620-pages-articles-multistream.xml.bz2 --json -l

```
After using WikiExtractor, we obtain a directory named "multistream". This directory comprises numerous subfolders, each of which contains approximately 100 TXT files. Each TXT file has several JSON lines.
3. Running **[extracted_data_to_json.py]()**, which convert the files in multistream to a JSON file named multistream.json.

Step 2 - Preprocessing
1. Running the following SPARQL query on  the **[Official Wikidata SPARQL endpoint](https://query.wikidata.org/)**. The results are stored under the title wikidata_CUI.csv, wikidata_MeSH_ID.csv and wikidata_DOID.csv
```
    SELECT ?entity ?CUI
    WHERE {
      ?entity wdt:P2892 ?CUI .
    }
```

```
    SELECT ?entity ?MeSH_ID
    WHERE {
      ?entity wdt:P486 ?MeSH_ID .
    }
```

```
    SELECT ?entity ?DOID
    WHERE {
      ?entity wdt:P699 ?DOID .
    }
    
```

2. **[preprocessing/wiki_id_to_qid.py]()** 
	* Goal: convert the Wikipedia page ID to QID that can be used to extract Wididata properties. 
	* To run this code, we need:
		* the German Wikipedia page property file dewiki-20230620-page_props.sql.gz downloaded from **[German Wikipedia dump](https://dumps.wikimedia.org/dewiki/20230620/)**
	* Output: wiki_id_qid.csv

3. **[preprocessing/CUI_TUI.py]()**  
	* Goal: map UMLS CUI with TUI. 
	* To run this code, we need:
		* **[MRSTY.RRF]()** downloaded from **[ umls-2023AA-mrconso.zip](https://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html)**. 
		* wikidata_CUI.csv
	* Outputs: 
		* cui_tui_csv 
		* qid_cui_tui.csv
4.  **[preprocessing/mesh_cui.py]()** 
	* Goal: map MeSH ID with UMLS CUI. 
	* To run this code, we need:
		* **[MRCONSO.RRF]()** downloaded from **[ umls-2023AA-mrconso.zip](https://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html)**.
		* cui_tui.csv
		* wikidata_MeSH_ID.csv
	* Outputs:
		* mesh_cui.csv
		* mesh_cui_tui.csv
		* qid_mesh.csv

5. **[preprocessing/DOID_CUI.py]()** 
	* Goal: map DOID with UMLS CUI. 
	* To run this code, we need:
		* **[ doid.json](https://github.com/DiseaseOntology/HumanDiseaseOntology/blob/main/src/ontology/releases/doid.json)** 
		* wikidata_DOID.csv
		* cui_tui.csv 
	* Outputs:
		* doid_cui.csv 
		* doid_cui_tui.csv.
		* qid_doid.csv

Step 3 - Filtering Wikipedia Articles
1. **[generate_initial_data.py]()**
	* Goal: filter the German Wikipedia articles which contains either UMLS CUI, MeSH ID or DOID.
	* To run this code, we need:
		* multistream.json
		* wiki_id_qid.csv
		* qid_cui_tui.csv
		* qid_mesh.csv
		* qid_doid.csv
	* Outputs:
		* multistream_only_cui_mesh_doid.json

2. **[filtering_initial_data.py]()** 
	* Goal: filter out the Wikipedia articles without any mention (without HTML tags)
	* To run this code, we need:
		* multistream_only_cui_mesh_doid.json
	* Outputs:
		* multistream_text.json

Step 4 - Mapping Mentions to Wikidata
1. **[save_mentions.py]()** 
	* Goal: save all mentions appearing in German Wikipedia articles and map mention URL with Wikipedia page ID
	* To run this code, we need:
		* multistream_text.json
	* Outputs
		* mention.csv
		* mention_url.csv

2. **[mentions_to_qid.py]()** 
	* Goal: map mention URL with QID
	* To run this code, we need:
		* mention_url.csv
		* wiki_id_qid.csv
	* Outputs:
		* mentions_qids.csv
3. **[redirect_mention_urls.py]()** 
	* Goal: redirect the URLs to new page ID
	* To run this code, we need:
		* mention_url.csv
		* wiki_id_qid.csv
	* Outputs:
		* mentions_url_including_redirect.csv

Step 5 - Integrating all information
1. **[generate_Wikimedde.ipynb]()** 
	* To run this code, we need:
		* multistream_text.json
		* wiki_id_qid.csv
		* qid_cui_tui.csv
		* qid_mesh.csv
		* qid_doid.csv
		* mesh_cui_tui.csv
		* doid_cui_tui.csv
		* mentions_url_including_redirect.csv
	* Outputs
		* WikiMed-DE.json

