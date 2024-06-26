"""This program outputs Turkish sentences where verb lemmas
that are parsed as never appearing with a causative marker
in the Wiki corpus act as the embedded causative verb.

The template is of the form "Ben ona bunlari <verb_lemma+DIR>"

This is to provide a clause structure for the verbs to "fake" some
context. The allomorphy is ignored.
"""

# importing csv since data is only 19 KB
import csv

# Passing the input TSV file to read_csv() function
with open("verbs_never_in_causative.tsv", "r", newline="") as source, open("caus_test_sentences.tsv", "w", newline="") as sink:
    # Create the reader and writer objects
    tsv_reader = csv.reader(source, delimiter="\t")
    tsv_writer = csv.writer(sink, delimiter=' ', quotechar='"')
    
    # Skip the header row if present
    next(tsv_reader, None)

    # Create an empty list to store the verb lemmas
    verb_lemmas = []
    # Iterate through the each row of the first column in the reader object
    for row in tsv_reader:
        # Append the verb lemmas to the empty list
        verb_lemmas.append(row[0])

    # Write formatted strings to the new file
    for lemma in verb_lemmas:
        formatted_string = f"Ben ona bunları {lemma}dırdım."
        tsv_writer.writerow([formatted_string]) # Need [] to prevent .writerow() treating <lemma> as an iterable. 
        # Otherwise, it adds whitespace between each character





# printing to test
# print(tsv_reader)





