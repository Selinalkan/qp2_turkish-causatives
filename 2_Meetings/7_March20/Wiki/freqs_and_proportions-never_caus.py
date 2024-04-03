"""
Reads two TSV files containing verb and causative data, identifies 
verbs that never appear in the causative form,
computes their frequency counts and proportions, and outputs the 
results to a new TSV file.

Parameters:
-----------
None

Returns:
--------
None

Explanation:
------------
This script reads two tab-separated value (TSV) files, "full-verb.tsv" and 
"full-caus.tsv", containing verb and causative data, respectively, using
the pandas library. It then counts the frequency of each unique lemma for
verbs and causatives separately.

Next, it identifies verbs that never appear in the causative form by 
comparing the lemma frequencies between verbs and causatives.
It calculates the total number of verbs among those that never appear 
in the causative form.

The proportions of these verbs are calculated by dividing their 
frequency counts by the total number of such verbs, and rounding the
results to three decimal places.

The resulting dataframe contains columns for verb lemma, frequency, 
and proportion. The script outputs this dataframe to a new
TSV file named "verbs_not_in_causative.tsv".
"""


import pandas as pd

# Read the TSV files
df_verb = pd.read_csv("full-verb.tsv", sep="\t")
df_caus = pd.read_csv("full-caus.tsv", sep="\t")

# Count the frequency of each unique lemma for verbs and causatives separately
lemma_counts_verb = df_verb["lemma"].value_counts()
lemma_counts_caus = df_caus["lemma"].value_counts()

# Convert the lemma counts series to dataframes
df_lemma_counts_verb = pd.DataFrame({"verb_lemma": lemma_counts_verb.index, "verb_freq": lemma_counts_verb.values})
df_lemma_counts_caus = pd.DataFrame({"caus_lemma": lemma_counts_caus.index, "caus_freq": lemma_counts_caus.values})

# Identify verbs that never appear in the causative
non_causative_verbs = df_lemma_counts_verb[~df_lemma_counts_verb["verb_lemma"].isin(df_lemma_counts_caus["caus_lemma"])]

# Calculate total number of verbs
total_verbs = non_causative_verbs["verb_freq"].sum()

# Calculate proportions of verbs
non_causative_verbs["verb_proportion"] = (non_causative_verbs["verb_freq"] / total_verbs).round(3)

# Reorder the columns
non_causative_verbs = non_causative_verbs[["verb_lemma", "verb_freq", "verb_proportion"]]

# Output the dataframe of verbs that never appear in the causative to a new TSV file
non_causative_verbs.to_csv("verbs_never_in_causative.tsv", sep="\t", index=False)
