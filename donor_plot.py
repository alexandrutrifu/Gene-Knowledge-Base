from data_interaction import get_donor_data

def get_age_comparison_plot(gene_name):
	# Select all columns containing young/old donor data
	young_donor_data, old_donor_data = get_donor_data(gene_name)