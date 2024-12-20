import pandas as pd
import numpy as np

# Read the TSV files
df_verb = pd.read_csv("verbs.tsv", sep="\t")
df_caus = pd.read_csv("caus.tsv", sep="\t")

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


# Merge the two dataframes
df_merged = pd.merge(
    df_lemma_counts_verb,
    df_lemma_counts_caus,
    left_on="verb_lemma",
    right_on="caus_lemma",
    how="left"
)

# Calculate total number of verbs
total_verbs = df_merged["verb_freq"].sum()
# print(f"The total number of verbs is {total_verbs}.") # Outputs: The total number of verbs is 4777071. (12/19/24)

# Merge the 2 dataframes into one first, and then make the calculations
# Calculate P(verb)
df_merged["P(verb)"] = (
    df_merged["verb_freq"] / total_verbs
).round(3)
###

# Calculate P(CAUS)
total_caus = df_merged["caus_freq"].sum()
# print(f"Total number of causative tokens is {total_caus}.")
df_merged["P(CAUS)"] = (total_caus / total_verbs).round(3)

# Fill NaN values in caus_freq with a small number that will not affect the other calculations
df_merged["caus_freq"] = df_merged["caus_freq"].fillna(1e-10)

# Calculate expected and actual proportions
df_merged["expected_P(CAUS^verb)"] = (df_merged["P(verb)"] * 0.064)
df_merged["actual_P(CAUS^verb)"] = (df_merged["caus_freq"] / df_merged["verb_freq"])

# Calculate log of expected and actual proportions
df_merged["log_expected"] = np.log(df_merged["expected_P(CAUS^verb)"].replace(0, np.nan))  # Replace 0 with NaN to avoid log(0)
df_merged["log_actual"] = np.log(df_merged["actual_P(CAUS^verb)"].replace(0, np.nan))  # Replace 0 with NaN to avoid log(0)

# Calculate the log odds ratio (LR)
df_merged["log_odds_ratio"] = (df_merged["log_expected"] - df_merged["log_actual"]).round(3)

# # Fill NaN values in log_odds_ratio with a placeholder (e.g., 0 or any value you decide)
# df_merged["log_odds_ratio"] = df_merged["log_odds_ratio"].fillna(0)

# # Replace NaN values in log_actual with a placeholder (e.g., -np.inf or 0)
# df_merged["log_actual"] = df_merged["log_actual"].fillna(0).round(3)  # Replace NaN logs with 0
# df_merged["log_expected"] = df_merged["log_expected"].fillna(0).round(3)

# Reorder the columns
df_merged = df_merged[
    [
        "verb_lemma",
        "verb_freq",
        "P(verb)",
        "caus_freq",
        "P(CAUS)",
        "expected_P(CAUS^verb)",
        "actual_P(CAUS^verb)",
        "log_expected",
        "log_actual",
        "log_odds_ratio",
    ]
]

# Output the merged dataframe to another TSV file
df_merged.to_csv("proportions.tsv", sep="\t", index=False)

df_merged_less = df_merged[
    [
        "verb_lemma",
        "P(verb)",
        "P(CAUS)",
        "expected_P(CAUS^verb)",
        "actual_P(CAUS^verb)",
        "log_odds_ratio",
    ]
]

# Output the merged dataframe to another TSV file
df_merged_less.to_csv("proportions-less.tsv", sep="\t", index=False)


# Filter the dataframe to include only rows where log_odds_ratio > 0
df_positive_lor = df_merged[df_merged['log_odds_ratio'] > 0.0]

# # Sort the filtered dataframe by log_odds_ratio in descending order
# df_positive_lor = df_positive_lor.sort_values('log_odds_ratio', ascending=False)

# Select the desired columns for the output
df_positive_lor_less = df_positive_lor[
    [
        "verb_lemma",
        "P(verb)",
        "P(CAUS)",
        "expected_P(CAUS^verb)",
        "actual_P(CAUS^verb)",
        "log_odds_ratio",
    ]
]

# Output the filtered dataframe to a new TSV file
df_positive_lor_less.to_csv("positive_log_odds_ratio.tsv", sep="\t", index=False)

