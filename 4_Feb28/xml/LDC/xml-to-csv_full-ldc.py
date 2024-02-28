import pandas as pd
from collections import Counter

# Open the XML file
# with open("short-LDC.xml", "r") as file:
with open("TS_Wikipedia_PosTagged.xml", "r") as file:
    data = []
    in_text_tag = False
    for line in file:
        # Check if line contains the start of <text> tag
        if "<text" in line:
            in_text_tag = True
            text_data = []
        # Check if line contains the end of </text> tag
        elif "</text>" in line:
            in_text_tag = False
            # Process the data collected between <text> and </text> tags
            for text_line in text_data:
                elements = text_line.strip().split()
                if len(elements) == 5:  # Ensure there are exactly five elements
                    data.append({
                        'word': elements[0],
                        'pos_tag': elements[1],
                        'morph_parse': elements[2],
                        'lemma': elements[3],
                        'correct_form': elements[4]
                    })
        # Collect lines between <text> and </text> tags
        elif in_text_tag:
            text_data.append(line)


# Create DataFrame
df = pd.DataFrame(data)

# Save DataFrame to TSV
#df.to_csv("full_wiki_output.tsv", sep='\t', index=False)
# df.to_csv("output.tsv", sep='\t', index=False)

#print(df)

# Create a new DataFrame with only the Verb rows from the pos_tag column
df_verb = df[df.pos_tag == "Verb"]
df_verb.to_csv("full-output-verb.tsv", sep='\t', index=False)
print(df_verb.head())

# Filter the DataFrame by a string value in the "morph_parse" column
df_caus = df_verb[df_verb["morph_parse"].str.contains("Caus")]
df_caus.to_csv("full-output-caus.tsv", sep='\t', index=False)
print(df_caus.head())

# Count the frequency of rows where "morph_parse" contains at least one "Caus"
freq = Counter(row['morph_parse'].count('Caus') > 0 for index, row in df_verb.iterrows())

# Save the output to a file
output_file = "full-freq_caus.txt"
with open(output_file, "w") as file:
    for key, value in freq.items():
        file.write(f"{'Contains Caus' if key else 'Does not contain Caus'}: {value}\n")

print(f"Output saved to {output_file}")

# Print the frequency
#print(freq)



