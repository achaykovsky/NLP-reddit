# Natural Language Processing
Natural Language Processing course: exercises using reddit corpus.
All the code is written in Python.

## Tokenizer 
The corpus consisted of 5 .csv files from 5 different countries on the Reddit website: Albania, Argentina, Cyprus, Georgia and Malta.
All the files can be found in the "input files" folder.

The first purpose was to clean the corpus from all the noise in it.
I used regular expressions to remove most of it.
Every method optimizes another aspect of the text: parenthesses, emoticons, HTML tags, e-mails, XML tags, abbreviations, special characters etc.

At the next step, the code splits the corpus into sentences and words.
Then it counts how much sentences each user wrote and prints the messages of the most frequent users of each country.


