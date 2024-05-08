"""
Reads two TSV files containing verb and causative data, computes frequency counts,
proportions, and differences in proportions, and outputs the results to a new TSV file.

Parameters:
-----------
None

Returns:
--------
None

Explanation:
------------
This script reads two tab-separated value (TSV) files, "full-verb.tsv" and "full-caus.tsv",
containing verb and causative data, respectively, using the pandas library. It then
calculates the frequency of each unique lemma for verbs and causatives separately. Note that
verb frequency counts include lemmas that appear with at least one causative marker, too. Next,
it converts the lemma frequency counts into separate dataframes for verbs and causatives.
The script calculates the total number of verbs and the proportions of verbs and causatives
in the corpus. 

The total number of verbs is calculated by summing the frequency counts of verbs since 
that already includes causatives. The proportions of verbs and causatives are calculated by
dividing their respective frequency counts by the total number of verbs and rounding the
results to three decimal places. 

After computing the proportions, the script calculates the difference between the 
proportions of verbs and causatives. It merges the dataframes for verbs and causatives
based on their lemma, aligning the frequencies correctly.

The columns in the resulting dataframe are reordered for clarity. Finally, the script
outputs the merged dataframe, containing lemma frequencies, proportions, and differences
in proportions, to a new TSV file named "freqs_and_proportions.tsv".
"""

import pandas as pd

# Read the TSV files
df_verb = pd.read_csv("full-verb.tsv", sep="\t")
df_caus = pd.read_csv("full-caus.tsv", sep="\t")

# Count the frequency of each unique lemma for verbs and causatives separately
lemma_counts_verb = df_verb["lemma"].value_counts()
lemma_counts_caus = df_caus["lemma"].value_counts()

# Convert the lemma counts series to dataframes
df_lemma_counts_verb = pd.DataFrame(
    {"verb_lemma": lemma_counts_verb.index, "verb_freq": lemma_counts_verb.values}
)
df_lemma_counts_caus = pd.DataFrame(
    {"caus_lemma": lemma_counts_caus.index, "caus_freq": lemma_counts_caus.values}
)

# Calculate total number of verbs
# NOTE: The count of verb_freq includes verbs showing up in whatever
# form including causation; therefore, the total # of verbs is just
# the sum of all verb_freqs, which is 4777071
# total_verbs = df_lemma_counts_verb["verb_freq"].sum() + df_lemma_counts_caus["caus_freq"].sum()
total_verbs = df_lemma_counts_verb["verb_freq"].sum()
# print(total_verbs)

# Calculate proportions of verbs and causatives
df_lemma_counts_verb["verb_proportion"] = (
    df_lemma_counts_verb["verb_freq"] / total_verbs
).round(3)
df_lemma_counts_caus["caus_proportion"] = (
    df_lemma_counts_caus["caus_freq"] / total_verbs
).round(3)

# Merge the dataframes to align the frequencies correctly
df_lemma_counts_merged = pd.merge(
    df_lemma_counts_verb,
    df_lemma_counts_caus,
    how="left",
    left_on="verb_lemma",
    right_on="caus_lemma",
)

# Calculate difference between proportions after merging
df_lemma_counts_merged["difference"] = (
    df_lemma_counts_merged["verb_proportion"] - df_lemma_counts_merged["caus_proportion"]
).round(3)

# Reorder the columns
df_lemma_counts_merged = df_lemma_counts_merged[
    [
        "verb_lemma",
        "verb_freq",
        "verb_proportion",
        "caus_lemma",
        "caus_freq",
        "caus_proportion",
        "difference",
    ]
]

# Output the merged dataframe to another TSV file
df_lemma_counts_merged.to_csv("freqs_and_proportions.tsv", sep="\t", index=False)
