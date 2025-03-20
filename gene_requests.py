import requests


PUBMED_URL = "https://pubmed.ncbi.nlm.nih.gov/"
MYGENE_URL = "https://mygene.info/v3/gene/"

def get_pubmed_references(gene_id):
	# Request ONLY publication references
	params = {
		"fields": "generif"
	}

	r = requests.get(MYGENE_URL + f"{gene_id}", params=params)

	# Get reference summaries included in JSON reference
	references = r.json()["generif"]

	return references