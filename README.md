Code for the paper: 

[WikiMed-DE: Constructing a Silver-Standard Dataset for German Biomedical Entity Linking using Wikipedia and Wikidata](https://openreview.net/forum?id=5dQ7YDSYya). 2023. Yi Wang, Corina Dima, Steffen Staab. Wikidata workshop @ ISWC 2023.

You can download the WikiMed-DE dataset from https://doi.org/10.5281/zenodo.8188966.

WikiMed-DE is a silver standard German biomedical entity linking dataset. It was created automatically by connecting the links in German Wikipedia articles to Wikidata and through Wikidata to the Unified Medical Language System (UMLS), the Medical Subject Headings (MeSH) and the Disease Ontology (DO). 

Every sample in WikiMed-DE is associated to its unique Wikipedia page ID and the corresponding url, title and text as well as structured information mapped from Wikidata, namely the QID, the UMLS CUI, the UMLS TUI, the UMLS semantic type, the MeSH ID and the DOID. 

In WikiMed-DE, we extract every hyperlinked text span in Wikipedia articles as a mention. Each mention in WikiMed-DE features its surface form, its title, the start and end indices and the structured information mapped from Wikidata. More details can be found in the paper linked above.
  
WikiMed-DE is provided in a JSON format, one document per line. Here is a sample annotated article:

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

### Prerequisites

The code is written in [Python](https://www.python.org) and was tested on Python version 3.10.9. 

Use `pip install -r requirements.txt` to install the required packages.

You will need enough space on your machine, given that both the Wikidata archives and the UMLS distribution contain large files.

To recreate the dataset you need access to the UMLS. You can obtain a license from the [UMLS Terminology Services](https://uts.nlm.nih.gov/license.html).

### WikiMed-DE versions

WikiMed-DE version 1.0 uses the Wikipedia dumps from 20.06.2023, the UMLS release 2023AA and the June 2023 release of the Disease Ontology. 

---

### Running the code

#### Part A - Obtain the German Wikipedia articles:

1. Download the German Wikipedia articles `dewiki-20230620-pages-articles-multistream.xml.bz2` from the **[German Wikipedia dumps](https://dumps.wikimedia.org/dewiki/20230620/)** and place it in the `data` directory.

2. Install **[WikiExtractor](https://github.com/attardi/wikiextractor)** using `pip`, then use it to extract the clean text from the archive downloaded at step 1. Run the command line: 

```python
python -m wikiextractor.WikiExtractor dewiki-20230620-pages-articles-multistream.xml.bz2 --json -l
```

Important! The command line above will also work with the repository-version of WikiExtractor. However, it will produce errors regarding MediaWiki templates, and the extraction will last much longer.
On a typical machine the extraction is relatively fast, and it should take less than 30 minutes.

The result of the above command line is a directory named `text`. This directory comprises numerous subfolders, each containing approximately 100 files. Each file has several JSON lines.

3. Run **[extracted_data_to_json.py](https://github.com/AI4MedCode/wikimed-de/blob/main/code/extracted_data_to_json.py)**, which converts the files in the `text` directory to a JSON file named `multistream.json`, which will be saved under the `outputs` directory.

```python
python code/extracted_data_to_json.py
```

---
#### Part B - Preprocessing

1. Run the following SPARQL queries on  the **[official Wikidata SPARQL endpoint](https://query.wikidata.org/)**. Store the results as `wikidata_CUI.csv`, `wikidata_MeSH_ID.csv` and `wikidata_DOID.csv` under the `data` directory.

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

Given that this step queries the current version of Wikidata, the results might differ from the ones we reported in our paper. In general, however, if the number of extracted IDs is higher, the quality of the dataset will be better.
For reproducibility, we provide the results of these queries use to generate the dataset described in the paper in the `data` directory.  

2. Run the script **[preprocessing/wiki_id_to_qid.py](https://github.com/AI4MedCode/wikimed-de/blob/main/code/preprocessing/wiki_id_to_qid.py)** 
	* Goal: map the Wikipedia page IDs to Wikidata QIDs. 
	* To run this code we need the German Wikipedia page props file `dewiki-20230620-page_props.sql.gz` downloaded from the **[German Wikipedia dump](https://dumps.wikimedia.org/dewiki/20230620/)**. Please place this file in the `data` directory.
	* Output: wiki_id_qid.csv

  ```python
  python code/preprocessing/wiki_id_to_qid.py
  ```

3. Run the script **[preprocessing/CUI_TUI.py](https://github.com/AI4MedCode/wikimed-de/blob/main/code/preprocessing/CUI_TUI.py)**  
	* Goal: map UMLS CUIs to their corresponding TUIs. 
	* To run this code, we need:
		* **[MRSTY.RRF]()** downloaded from **[ umls-2023AA-mrconso.zip](https://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html)**. Place this file in the `data` directory, under `2023AA/META/`.
		* wikidata_CUI.csv (obtained in step B1)
	* Outputs: 
		* cui_tui_csv 
		* qid_cui_tui.csv

```python
python code/preprocessing/CUI_TUI.py
```

If you use another UMLS release, please update the file paths accordingly.

4. Run the script **[preprocessing/mesh_cui.py](https://github.com/AI4MedCode/wikimed-de/blob/main/code/preprocessing/mesh_cui.py)** 
	* Goal: map MeSH IDs with UMLS CUIs. 
	* To run this code, we need:
		* **[MRCONSO.RRF]()** downloaded from **[ umls-2023AA-mrconso.zip](https://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html)**. Place this file in the `data` directory, under `2023AA/META/`.
		* cui_tui.csv (obtained in step B3)
		* wikidata_MeSH_ID.csv (obtained in step B1)
	* Outputs:
		* mesh_cui.csv
		* mesh_cui_tui.csv
		* qid_mesh.csv

```python
python code/preprocessing/mesh_cui.py
```

5. Run the script **[preprocessing/DOID_CUI.py](https://github.com/AI4MedCode/wikimed-de/blob/main/code/preprocessing/DOID_CUI.py)** 
	* Goal: map DOIDs to UMLS CUIs. 
	* To run this code, we need:
		* **[doid.json](https://github.com/DiseaseOntology/HumanDiseaseOntology/blob/main/src/ontology/releases/doid.json)**, from the Disease Ontology. Place this file in the `data` directory. We used the DO release June 2023 for generating the dataset.
		* wikidata_DOID.csv (obtained in step B1)
		* cui_tui.csv (obtained in step B3)
	* Outputs:
		* doid_cui.csv 
		* doid_cui_tui.csv.
		* qid_doid.csv

```python
python code/preprocessing/DOID_CUI.py
```
---

#### Part C - Filter Wikipedia articles

1. Run the script **[generate_initial_data.py](https://github.com/AI4MedCode/wikimed-de/blob/main/code/generate_initial_data.py)**
	* Goal: filter the German Wikipedia articles which have a UMLS CUI, MeSH ID or DOID associated to them.
	* To run this code, we need:
		* multistream.json (obtained in step A3)
		* wiki_id_qid.csv (obtained in step B2)
		* qid_cui_tui.csv (obtained in step B3)
		* qid_mesh.csv (obtained in step B4)
		* qid_doid.csv (obtained in step B5)
	* Outputs:
		* multistream_only_cui_mesh_doid.json

```python
python code/generate_initial_data.py
```

2. Run the script **[filtering_initial_data.py](https://github.com/AI4MedCode/wikimed-de/blob/main/code/filtering_initial_data.py)** 
	* Goal: filters out the Wikipedia articles without any mention (without HTML tags)
	* To run this code, we need:
		* multistream_only_cui_mesh_doid.json (obtain in step C1)
	* Outputs:
		* multistream_text.json

```python
python code/filtering_initial_data.py
```

--- 
#### Part D - Map mentions to Wikidata

1. Run the script **[save_mentions.py](https://github.com/AI4MedCode/wikimed-de/blob/main/code/save_mentions.py)** 
	* Goal: saves all mentions appearing in German Wikipedia articles and maps mention URLs to Wikipedia page IDs
	* To run this code, we need:
		* multistream_text.json (obtained in step C2)
	* Outputs
		* mention.csv
		* mention_url.csv

```python
python code/save_mentions.py
```

This script will take a longer time to complete (~9h, depending the machine/internet connection), as it checks that the mention URLs are valid.

2. Run the script **[mentions_to_qid.py](https://github.com/AI4MedCode/wikimed-de/blob/main/code/mentions_to_qid.py)** 
	* Goal: map mention URL to QID
	* To run this code, we need:
		* mention_url.csv (obtained in step D1)
		* wiki_id_qid.csv (obtained in step B2)
	* Outputs:
		* mentions_qids.csv

```python
python code/mentions_to_qid.py
```

3. Run the script **[redirect_mention_urls.py](https://github.com/AI4MedCode/wikimed-de/blob/main/code/redirect_mention_urls.py)** 
	* Goal: solve redirect URLs to the correct page IDs
	* To run this code, we need:
		* mention_url.csv (obtained in step D1)
		* wiki_id_qid.csv (obtained in step B2)
	* Outputs:
		* mentions_url_including_redirect.csv

```python
python code/redirect_mention_urls.py
```

This script also takes longer to run (~7h), as it will check for redirects for pages by making requests to the Wikipedia API.

---

#### Part E - Integrate all the information and generate the final dataset

1. Run the notebook **[generate_Wikimedde.ipynb](https://github.com/AI4MedCode/wikimed-de/blob/main/code/generate_Wikimedde.ipynb)** 
	* To run this code, we need:
		* multistream_text.json (obtained in step C2)
		* wiki_id_qid.csv (obtained in step B2)
		* qid_cui_tui.csv (obtained in step B3)
		* qid_mesh.csv (obtained in step B4)
		* qid_doid.csv (obtained in step B5)
		* mesh_cui_tui.csv (obtained in step B4)
		* doid_cui_tui.csv (obtained in step B5)
		* mentions_url_including_redirect.csv (obtained in step D3)
	* Outputs
		* WikiMed-DE.json
    * WikiMed-DE-BEL.json

You can either run the Jupyter notebook interactively or you can convert it to a Python script and run it from the command line, like so:

```python
jupyter nbconvert --to python code/generate_Wikimedde.ipynb
python code/generate_Wikimedde.py
```
