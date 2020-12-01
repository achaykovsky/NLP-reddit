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

**1.** Calculating the probabilities of a few random sentences that were given to us:

	**a.** Unigram sentence probability calculation using Laplace Smoothing.
	
	**b.** Bigram sentence probability calculation using Backoff algorithm.
	
	**c.** Trigram aentence probability calculation using Linear Interpolation.
	
**2.** Generate random sentences using unigrams vs bigrams vs trigrams.

	Some examples of the results:
	
	#### Examples of randomized sentences that are made out of the full corpus that contains all 5 countries:
	
	**A.** Based on unigrams:
	
	![image](https://user-images.githubusercontent.com/49001453/99429709-09c4b000-2911-11eb-8adf-da1b4f49d39c.png)
	
	**B.** Based on bigrams:
	
	![image](https://user-images.githubusercontent.com/49001453/99429870-3d9fd580-2911-11eb-927a-7c34ec1655a1.png)
	
	**C.** Based on trigrams:
	
	![image](https://user-images.githubusercontent.com/49001453/99429959-5ad4a400-2911-11eb-9092-ef07a518376f.png)
	
	
	The unigrams are just random words that don't make up a coherent sentence.
	We can see a little progress in the bigrams, and the most of the pairs make sense.
	The best result is seen in the trigrams structure. 
	
	
	
	#### Examples of randomized sentences that are made out of partial corpus:
	
    **A.** Examples of randomized sentences that are made only out of the Albania Corpus.

	![image](https://user-images.githubusercontent.com/49001453/99433169-d9cbdb80-2915-11eb-89e9-2c213c762372.png)
	
	**B.** Examples of randomized sentences that are made only out of the Argentina Corpus.
	
	![image](https://user-images.githubusercontent.com/49001453/99433282-fc5df480-2915-11eb-914e-5c867d93a414.png)
	
	**C.** Examples of randomized sentences that are made only out of the Cyprus Corpus.

	![image](https://user-images.githubusercontent.com/49001453/99433794-a63d8100-2916-11eb-9f3c-c0ea3509f5f3.png)	
	
	**D.** Examples of randomized sentences that are made only out of the Georgia Corpus.

	![image](https://user-images.githubusercontent.com/49001453/99194884-18815a80-278b-11eb-9269-fce85fc03391.png)
	
	**E.** Examples of randomized sentences that are made only out of the Malta Corpus.
	
	![image](https://user-images.githubusercontent.com/49001453/99433411-26171b80-2916-11eb-9b2f-e9b034b59e82.png)

	
	
	
	You can see the improvement from bigrams sentences to trigrams sentences.
	On the trigrams structure, some of the sentences make a little more sense, and sometimes they are even fully coherent.
	Of course, some of them are could be just the original sentences.
	
	**Note:** Every randomized sentence is independent and doesn't rely on the sentence before it.
	
	
## Text Classification
	
This assignment has 2 parts:

**1.** Author Identification
**2.** Native Language Identification (NLI)

The output TXT files from the tokenizer assignment is the input files for this assignment.

### Author Identification
The input to this task are all the sentences of the 2 most frequent users from Argentina.
The purpose is to classify the sentences to identify which user wrote the sentence.
Each classification unit in this task is a sentence.

### Native Language Identification
The input to this task are 5 files: each file has all the sentences of the 10 most frequent users from one of the countries (Albania, Argentina, Cyprus, Georgia and Malta).
The purpose is to classify the sentences to identify the country of the author.
Each classification unit in this task is built from 20 sentences.


Each of the tasks classified by 3 three types of features:
**1.** Bag Of Words (all of the words in the corpus).
**2.** Manual features (features I chose manually to improve the accuracy)
**3.** 100 best words (100 best words to classify chosen automatically by k-best function).

The classifiers are Linear Regression and Multinomial Naive Bais.

After the classification, we make a ten fold cross validation to calculate the accuracy.

**The classification results:**

![classificationResults](https://user-images.githubusercontent.com/49001453/100139758-9b479b00-2e98-11eb-93ff-45e122fabb7c.PNG)


## Classification using Word Embeddings

The corpus in this task is devided to chuncks, where each chunk made from 20 sentences.

The classifier is Logistic Regression.

The task is to make a NLI (Native Language Identification) classification using word embeddings of 2 kinds:
	**1.** The first word embedding model is based on the 100K most frequent words in English that was trained on Wikipedia.
	**2.** The second word embedding model is the model that was trained on my corpus. 

The classification was made in 3 ways:
	**1.** Each word in the sentence gets the same weight (weight = 1)
	**2.** Each word in the sentence gets a random weight in the interval (0,1)
	**3.** Words that were chosen manually that give the biggest contribition, get higher weight (The words were chosen by k-best function).
	
The feature vector of each chunk is calculated by this formula:
![weightCalculation](https://user-images.githubusercontent.com/49001453/100552299-00333480-328f-11eb-806e-9c3cdca4cac4.PNG)
Wi - is the weight of the i word.
Vi - is the vector representing the i word in the word embedding model.
k - is the number of words in the chunk.

The purpose was to compare the classification methods with differenet weights using 4 measures with a ten fold cross validation:
	**1**. Accuracy
	**2.** Precision
	**3.** Recall
	**4.** f1

**Note:** The model was created using Word2Vec from the genism library:
`self_trained_model = Word2Vec(sentences, size=300, min_count=10) self_trained_model.wv.save_word2vec_format(f'{outputDir}\model.vec')`

### The classification results:
![classificationResults-hw4](https://user-images.githubusercontent.com/49001453/100552045-530bec80-328d-11eb-8b66-b1f386f23e09.PNG)
