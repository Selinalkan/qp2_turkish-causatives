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
total_verbs = df_lemma_counts_verb["verb_freq"].sum()
# print("total verb count is", total_verbs)

# # Calculate proportions of verbs and causatives
# df_lemma_counts_verb["verb_proportion"] = (
#     df_lemma_counts_verb["verb_freq"] / total_verbs
# ).round(3)

# df_lemma_counts_caus["caus_proportion"] = (
#     df_lemma_counts_caus["caus_freq"] / total_verbs
# ).round(3)

# Merge the dataframes to align the frequencies correctly
df_lemma_counts_merged = pd.merge(
    df_lemma_counts_verb,
    df_lemma_counts_caus,
    how="left",
    left_on="verb_lemma",
    right_on="caus_lemma",
)

df_lemma_counts_merged["caus_verb_proportion"] = (
    df_lemma_counts_merged["caus_freq"] / df_lemma_counts_merged["verb_freq"]
).round(3)

# Reorder the columns
df_lemma_counts_merged = df_lemma_counts_merged[
    [
        "caus_lemma",
        "caus_freq",
        "verb_freq",
        "caus_verb_proportion",
        # "verb_lemma",
    ]
]

# Sort the dataframe based on caus_freq from ascending to descending
df_lemma_counts_merged = df_lemma_counts_merged.sort_values(
    by="caus_verb_proportion", ascending=False
)

# Output the merged dataframe to another TSV file
df_lemma_counts_merged.to_csv("caus-verb_prop.tsv", sep="\t", index=False)
