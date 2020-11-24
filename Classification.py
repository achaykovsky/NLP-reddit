# -*- coding: utf-8 -*-
import sys
import glob
import os
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.feature_selection import SelectKBest


def findUserName(address):
    m = re.search('(.+?)_Argentina.txt', address)
    if m:
        found = m.group(1) 
    return found

def findCountryName(address):
    m = re.search('(.+?).txt', address)
    if m:
        found = m.group(1) 
    return found 

def readFiles(inputDir, authorIdentification):
    counter = 0    
    objects = dict()
    classes = dict()
    for address in inputDir:
        file = open(address,"r", encoding = "utf-8")
        fileName = os.path.basename(file.name)
        # finds the user name if it is the author auditification 
        if (authorIdentification == True):
            name = findUserName(fileName)
        # finds the country name otherwise(the NLI exercise)
        else:
            name = findCountryName(fileName)
        lines = 0
        numLines = []
        
        for line in file:
                        if name not in objects: 
                            objects[name] = []
                            classes[name] = counter
                            objects[name].append(line.strip().lower())
                            counter += 1
                        else:
                            objects[name].append(line.strip().lower())
                        lines += 1
        file.close()
        numLines.append(lines)
    return objects, classes

######################################################################################
# Merging every 20 sentences to sets and set a label to it in one country
######################################################################################
def mergeSentences(sentences, numOfClass):
    numofLines = 1
    dataset = []
    targets = []
    newSentence = ''
    for sentence in sentences:       
        if numofLines < 20:
            newSentence = newSentence + ' ' + sentence
            numofLines += 1
        else:
            newSentence = newSentence + ' ' + sentence
            dataset.append(newSentence)            
            targets.append(numOfClass)
            numofLines = 1            
            newSentence = ''
    return dataset, targets

######################################################################################
# classifying the sentences for both tasks
######################################################################################
def classifySentences(objects, classes, authorIdentification):
    index = 0
    dataset = []
    targets = []
    if authorIdentification == True:
            for name in objects:
                # sets the number of the class by the name (of the user name ot the country)
                numOfClass = classes[name]
                for index in range(len(objects[name])):
                    dataset.append(objects[name][index])
                    targets.append(numOfClass)
                    index += 1                    
    else:
            for name in objects:
                # sets the number of the class by the name (of the user name ot the country)
                numOfClass = classes[name]
                mergedSet, mergedSentencesTargets = mergeSentences(objects[name], numOfClass)
                dataset.extend(mergedSet)
                targets.extend(mergedSentencesTargets)                                  
    return dataset, targets

######################################################################################
# Calculates the Naive Bais and Logistic Regression accuracy    
######################################################################################
def calculateNBandLR(dataset, targets):
    nbScores = cross_val_score(MultinomialNB(), dataset, targets, cv = 10)
    lgScores = cross_val_score(LogisticRegression(solver = 'liblinear', multi_class = 'auto', max_iter = 1000) , dataset, targets, cv = 10)
    nbAccuracy = nbScores.mean()*100
    lgAccuracy = lgScores.mean()*100  
    return nbAccuracy, lgAccuracy

######################################################################################
# Counting how much unique words there are in the corpus (Phase 1, q.1)
# Counting the tf-idf of all the words in the corpus
######################################################################################

def calculateBagOfWords(authorIdentification, dataset):   
    count_vect = CountVectorizer(stop_words = 'english', decode_error = 'ignore', strip_accents = 'unicode', lowercase = 'true')                                         
    wordsCountVector = count_vect.fit_transform(dataset)
    tfidf_transformer=TfidfTransformer(smooth_idf = True, use_idf = True)
    tf_idf_values = tfidf_transformer.fit_transform(wordsCountVector)
    featureNames = count_vect.get_feature_names()
    return tf_idf_values, featureNames

##############################################################################################
# Best Words calculations, Kbest Vectors for the sentences and printing Kbest words to a file
##############################################################################################
def calculateKBestWords(wordsCountVector, targets, featureNames, n):
    KBestWords = []
    KBest = SelectKBest(k = n)
    KBest.fit_transform(wordsCountVector, targets)
    indices = KBest.get_support(indices = 'True')
    for i in indices:
        KBestWords.append(featureNames[i])
    return KBestWords   

def calculateKBestVectors(KBestWords, dataset):
    count_vect = CountVectorizer(vocabulary = KBestWords, stop_words = 'english',  decode_error = 'ignore', strip_accents = 'unicode', lowercase = 'true')
    wordsCountVector = count_vect.fit_transform(dataset)
    tfidf_transformer=TfidfTransformer(smooth_idf = True, use_idf = True)
    tfidf_values = tfidf_transformer.fit_transform(wordsCountVector)
    return tfidf_values

def printBestWords(KBestWords, outputDir):
    f = open(f'{outputDir}/bestWords.txt', 'w+', encoding = "utf-8")
    for word in KBestWords:
            f.write(word)
            f.write("\n")
    f.close()
    
######################################################################################
#My Features
######################################################################################    
def calculatMyFeaturesAuthIden(dataset):
    myFeatures = ['life','support','love','saying','person','years','thanks','video','women','guess','won',
                  'care','buy','kind','team','friends','day','gods','lol','kill','post','old',
                  'white','watch','ymir','talking','skin','wrong','feel','understand','left','sub',
                  'stop','hate','sorry','agree','aren','live','movie','match','black','read','joke','believe',
                  'ago','looks','comment','internet','family','called','sounds','imagine','works','germany',
                  'basically','means','power','fight','attack','usually','gives','france','case','tried',
                  'units','land','single','sense','plus','small','example','interesting','deal','trade','cost',
                  'combat','build','countries','tanks','focus','army','argentina','naval','province','tech',
                  'half','bigger','kinda','able','weird','que','ships','china','especially','issue','second',
                  'paradox','japan','needs','map']
    tfidf_values = calculateKBestVectors(myFeatures, dataset)
    return tfidf_values    

def getTopNWords(corpus, n):
    count = CountVectorizer(stop_words = 'english',  decode_error = 'ignore', strip_accents = 'unicode', lowercase = 'true').fit(corpus)
    bagOfWords = count.transform(corpus)
    sumWords = bagOfWords.sum(axis = 0) 
    wordsFreq = [(word, sumWords[0, index]) for word, index in count.vocabulary_.items()]
    wordsFreq = sorted(wordsFreq, key = lambda x: x[1], reverse = True)
    return wordsFreq[:n]

def calculatMyFeaturesNLI(dataset):
    myFeatures = ['albania', 'albanian', 'albanians', 'argentina', 'argentinian', 'british','american',
                  'cypriot', 'cypriots', 'cyprus', 'eu', 'euro', 'europe', 'european', 'eurozone', 'euros',
                  'georgia', 'georgian', 'georgians', 'greece', 'greek', 'greeks', 'island', 'israel',
                  'malta', 'maltese', 'nicosia' ,'russia', 'russian', 'russians', 'spanish', 'turkey', 'kurds',
                  'turkish', 'turks', 'uk', 'ukraine', 'ukrainian','que', 'ship','ships', 'manchester',
                  'shipping','el','la','ve', 'muslim','nationalist', 'nationalists', 'germany', 'putin', 'cruisers',
                  'macedonia', 'united', 'liberal', 'liberals','buenos', 'aires', 'state', 'chelsea', 'college',
                  'police', 'policies', 'policy', 'senate','latin', 'republican','jungle','democratic', 'democrats',
                  'zao', 'torps', 'rebates', 'moyes', 'rooney', 'football', 'liverpool', 'hockey', 'rangers','islam',
                  'muslims', 'east', 'economic', 'economy', 'elections', 'south', 'western', 'union','conflict',
                  'citizens', 'communities', 'usa', 'trump', 'native', 'ca', 'military', 'army', 'bank', 'secular', 'settlers']
    tfidf_values = calculateKBestVectors(myFeatures, dataset)
    return tfidf_values


######################################################################################
#MAIN PROGRAM STARTS HERE:
######################################################################################
    
inputDir1 = str(sys.argv[1])
inputDir2 = str(sys.argv[2])
outputDir = str(sys.argv[3])
bestWordsPath1 = str(sys.argv[4])
bestWordsPath2 = str(sys.argv[5])
inputDir1 = glob.glob(inputDir1 + "/*.txt")
inputDir2 = glob.glob(inputDir2 + "/*.txt")
        

######################################################################################
# Loading the data from both tasks into the program
######################################################################################
authorIdentification = True
objects, classes = readFiles(inputDir1, authorIdentification)
datasetAuthIden, targetsAuthIden = classifySentences(objects, classes, authorIdentification)
datasetAuthIdenVectors, featureNamesAuthIden = calculateBagOfWords(authorIdentification, datasetAuthIden)
#The code I used to print the 200 words with
# for i in classes:
#     topNWords = getTopNWords(objects[i], n = 200)
#     print(topNWords)

 
authorIdentification = False  
objects, classes = readFiles(inputDir2, authorIdentification)
datasetNLI, targetsNLI = classifySentences(objects, classes, authorIdentification)
datasetNLIVectors, featureNamesNLI = calculateBagOfWords(authorIdentification, datasetNLI)

###########################################################################
# Phase 1 - Bag Of Words
###########################################################################
f = open(f'{outputDir}\output.txt', 'w+', encoding = "utf-8")
multinomialNBAccuracy, logRegAccuracy = calculateNBandLR(datasetAuthIdenVectors, targetsAuthIden)        
f.write("Phase 1 (Bag of Words):\nAuthor Identification:\n")
f.write("Naive Bayes: ")
f.write("{:.2f}%".format(multinomialNBAccuracy))
f.write("\n")
f.write("Logistic Regression: ")
f.write("{:.2f}%".format(logRegAccuracy))
f.write("\n")
multinomialNBAccuracy, logRegAccuracy = calculateNBandLR(datasetNLIVectors, targetsNLI)
f.write("Native Language Identification:\n")
f.write("Naive Bayes: ")
f.write("{:.2f}%".format(multinomialNBAccuracy))
f.write("\n")
f.write("Logistic Regression: ")
f.write("{:.2f}%".format(logRegAccuracy))
f.write("\n\n")
f.write("---------------------------------------------------------------\n")
###########################################################################
# Phase 2 - My features
###########################################################################
myFeatures = calculatMyFeaturesAuthIden(datasetAuthIden)
multinomialNBAccuracy, logRegAccuracy = calculateNBandLR(myFeatures, targetsAuthIden) 
f.write("Phase 2 (My features):\nAuthor Identification:\n")
f.write("Naive Bayes: ")
f.write("{:.2f}%".format(multinomialNBAccuracy))
f.write("\n")
f.write("Logistic Regression: ")
f.write("{:.2f}%".format(logRegAccuracy))
f.write("\n")
myFeatures = calculatMyFeaturesNLI(datasetNLI)
multinomialNBAccuracy, logRegAccuracy = calculateNBandLR(myFeatures, targetsNLI)
f.write("Native Language Identification:\n")
f.write("Naive Bayes: ")
f.write("{:.2f}%".format(multinomialNBAccuracy))
f.write("\n")
f.write("Logistic Regression: ")
f.write("{:.2f}%".format(logRegAccuracy))
f.write("\n\n")
f.write("---------------------------------------------------------------\n")
############################################################################
# Phase 3 - Best Features
############################################################################ 
KBestWords = calculateKBestWords(datasetAuthIdenVectors, targetsAuthIden, featureNamesAuthIden, 100)
printBestWords(KBestWords, bestWordsPath1)
kBestdatasetAuthIden = calculateKBestVectors(KBestWords, datasetAuthIden)
multinomialNBAccuracy, logRegAccuracy = calculateNBandLR(kBestdatasetAuthIden, targetsAuthIden)
f.write("Phase 3 (Best Features):\nAuthor Identification:\n")
f.write("Naive Bayes: ")
f.write("{:.2f}%".format(multinomialNBAccuracy))
f.write("\n")
f.write("Logistic Regression: ")
f.write("{:.2f}%".format(logRegAccuracy))
f.write("\n")
KBestWords = calculateKBestWords(datasetNLIVectors, targetsNLI, featureNamesNLI, 100)
printBestWords(KBestWords, bestWordsPath2)
kBestdatasetNLI = calculateKBestVectors(KBestWords, datasetNLI)
multinomialNBAccuracy, logRegAccuracy = calculateNBandLR(kBestdatasetNLI, targetsNLI)
f.write("Native Language Identification:\n")
f.write("Naive Bayes: ")
f.write("{:.2f}%".format(multinomialNBAccuracy))
f.write("\n")
f.write("Logistic Regression: ")
f.write("{:.2f}%".format(logRegAccuracy))
f.write("\n\n")
f.write("---------------------------------------------------------------\n")
f.close()    


print("Done!")