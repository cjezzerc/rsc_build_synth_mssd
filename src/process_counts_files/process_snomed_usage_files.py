# Reads a set of files downloaded from https://digital.nhs.uk/data-and-information/publications/statistical/mi-snomed-code-usage-in-primary-care
# and sums usage for each code across the collection

import sys

import glob


def read_snomed_usage_files(filename_glob_pattern=None):
    counts = {}
    filenames = glob.glob(filename_glob_pattern)
    for filename in filenames:
        for line in open(filename).readlines()[1:]:
            snomed_concept_id, description, usage, active_at_start, active_at_end = (
                line.split("\t")
            )
            if usage == "*":
                usage = 5
            if snomed_concept_id not in counts:
                counts[snomed_concept_id] = 0
            counts[snomed_concept_id] += int(usage)
    return counts

def read_snomed_pt_fsn_file(filename=None):
    fsn_dict={}
    for line in open(filename).readlines()[1:]:
        id, active, pt, fsn=line.split('\t')
        fsn_dict[id]=fsn.strip()
    return fsn_dict

snomed_usage_filename_glob_pattern = sys.argv[1]
snomed_pt_fsn_file = sys.argv[2]
output_filename = sys.argv[3]

snomed_counts = read_snomed_usage_files(
    filename_glob_pattern=snomed_usage_filename_glob_pattern
)

list_of_duplets = [[snomed_counts[x], x] for x in snomed_counts]
list_of_duplets.sort(reverse=True, key=lambda x: x[0])

snomed_fsn_dict=read_snomed_pt_fsn_file(filename=snomed_pt_fsn_file)
print(list_of_duplets[:10])
ofh = open(output_filename, "w")
for count, concept_id in list_of_duplets:
    ofh.write(f"{count}\t{concept_id}\t{snomed_fsn_dict[concept_id]}\n")
ofh.close()
