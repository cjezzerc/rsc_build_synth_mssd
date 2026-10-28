import tomllib
import random
import time

def read_disease_codelist_file(filename=None):
    concepts = {}
    for line in open(filename).readlines()[1:]:
        condition_id, concept_id, condition_name, term = line.split("\t")
        concepts[concept_id] = term
    return concepts

def read_epd_file(filename=None):
    counts = {}
    for line in open(filename).readlines():
        f = line.split()
        if len(f) > 1:  # ignore the count of blanks - need to check why there
            count, concept_id = line.split()
            counts[concept_id] = int(count)
    return counts

def read_snomed_usage_file(filename=None):
    counts = {}
    for line in open(filename).readlines()[1:]:
        usage, snomed_concept_id, fsn = line.split("\t")
        counts[snomed_concept_id] = int(usage)
    return counts

def generate_weighted_concept_occurrences(config_file=None, n_occurrences=None):

    config = tomllib.load(open("config.toml", "rb"))

    non_meds_filename = (
        f"{config["reference_file_directory"]}/{config["disease_codelist_file"]}"
    )

    meds_filename = (
        f"{config["reference_file_directory"]}/{config["prescription_codelist_file"]}"
    )

    epd_filename = f"{config["reference_file_directory"]}/{config["EPD_counts_file"]}"

    snomed_usage_filename = (
        f"{config["reference_file_directory"]}/{config["SNOMED_code_usage_file"]}"
    )

    non_meds_concepts = read_disease_codelist_file(filename=non_meds_filename)
    meds_concepts = read_disease_codelist_file(filename=meds_filename)
    epd_counts = read_epd_file(filename=epd_filename)
    snomed_counts = read_snomed_usage_file(filename=snomed_usage_filename)

    concepts_list = []
    counts_list = []
    for concept_id, term in non_meds_concepts.items():
        concept_count = snomed_counts.get(concept_id, 0)
        if concept_count > 0:
            concepts_list.append((concept_id, term.strip(), concept_count))
            counts_list.append(concept_count)

    rch = random.choices(concepts_list, weights=counts_list, k=n_occurrences)
    return rch

if __name__ == "__main__":
    t0 = time.time()
    gwco = generate_weighted_concept_occurrences(
        config_file="config.toml", n_occurrences=10
    )
    print(time.time() - t0)
    for x in gwco:
        print(x)
