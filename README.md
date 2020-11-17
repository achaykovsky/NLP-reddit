# Natural Language Processing
Natural Language Processing course: exercises using reddit corpus.
All the code is written in Python.

## Tokenizer 
The corpus consisted of 5 CSV files from 5 different countries on the Reddit website: Albania, Argentina, Cyprus, Georgia and Malta.
All the files can be found in the "input files" folder.

The first purpose was to clean the corpus from all the noise in it.
I used regular expressions to remove most of it.
Every method optimizes another aspect of the text: parenthesses, emoticons, HTML tags, e-mails, XML tags, abbreviations, special characters etc.

At the next step, the code splits the corpus into sentences and words.
Then it counts how much sentences each user wrote and prints the messages of the most frequent users of each country.

## Sentences Generator
### Unigrams, Bigrams and Trigrams
### Laplace Smoothing, Backoff algorithm and Linear Interpolation

The corpus consisted of 5 TXT files from 5 different countries that are based on the output of the tokenized files from the tokenizer assignment:
Albania, Argentina, Cyprus, Georgia and Malta.

The assignment had 2 parts:
1. Calculating the probabilities of a few random sentences that were given to us:
	a. Unigram sentence probability calculation using Laplace Smoothing.
	b. Bigram sentence probability calculation using Backoff algorithm.
	c. Trigram aentence probability calculation using Linear Interpolation.
	
2. Generate random sentences using unigrams vs bigrams vs trigrams.

	Some examples of the results:
	
	#### Examples of randomized sentences that are made out of the full corpus that contains all 5 countries:
	
	A. Based on unigrams:
	
	![image](https://user-images.githubusercontent.com/49001453/99429709-09c4b000-2911-11eb-8adf-da1b4f49d39c.png)
	
	B. Based on bigrams:
	
	![image](https://user-images.githubusercontent.com/49001453/99429870-3d9fd580-2911-11eb-927a-7c34ec1655a1.png)
	
	C. Based on trigrams:
	
	![image](https://user-images.githubusercontent.com/49001453/99429959-5ad4a400-2911-11eb-9092-ef07a518376f.png)
	
	
	The unigrams are just random words that don't make up a coherent sentence.
	We can see a little progress in the bigrams, and the most of the pairs make sense.
	The best result is seen in the trigrams structure. 
	
	
	
	#### Examples of randomized sentences that are made out of partial corpus:
	
    A. Examples of randomized sentences that are made only out of the Albania Corpus.

	![image](https://user-images.githubusercontent.com/49001453/99433169-d9cbdb80-2915-11eb-89e9-2c213c762372.png)
	
	B. Examples of randomized sentences that are made only out of the Argentina Corpus.
	
	![image](https://user-images.githubusercontent.com/49001453/99433282-fc5df480-2915-11eb-914e-5c867d93a414.png)
	
	C. Examples of randomized sentences that are made only out of the Cyprus Corpus.

	![image](https://user-images.githubusercontent.com/49001453/99433794-a63d8100-2916-11eb-9f3c-c0ea3509f5f3.png)	
	
	D. Examples of randomized sentences that are made only out of the Georgia Corpus.

	![image](https://user-images.githubusercontent.com/49001453/99194884-18815a80-278b-11eb-9269-fce85fc03391.png)
	
	E. Examples of randomized sentences that are made only out of the Malta Corpus.
	
	![image](https://user-images.githubusercontent.com/49001453/99433411-26171b80-2916-11eb-9b2f-e9b034b59e82.png)

	
	
	
	You can see the improvement from bigrams sentences to trigrams sentences.
	On the trigrams structure, some of the sentences have a little more sense, and sometimes they are even fully coherent.
	Of course, some of them are could be just the original sentences.
	
	Note: Every randomized sentence is independent and doesn't rely on the sentence before it.
	


