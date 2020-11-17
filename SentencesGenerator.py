# -*- coding: utf-8 -*-
import sys
import glob
import os
import re
import math
from random import choices


def findCountry(address):
    m = re.search('(.+?).txt', address)
    if m:
        found = m.group(1) 
    return found   

def createOutput(completeDict, countryList, outputDir):
    f = open(f'{outputDir}\output.txt', 'w+', encoding="utf-8")
    index = 0
    countryNames = [0 for x in range(2)]
    for key in countryList:
        countryNames[index] = key
        if (index<1):
            index += 1
    f.write("Unigrams model based on complete dataset:\n")
    unigramsFreqDict = createFrequencyDictForWords(completeDict)    
    for i in range(3):
        sentence = makeRandomizedUnigramSentence(unigramsFreqDict)
        f.write(sentence)
        f.write("\n")
    f.write("\nBigrams model based on complete dataset:\n")
    bigrams = wordsToNgrams(completeDict, 2," ")
    bigramsFreqDict = makeBigramsFrequencyDict(completeDict)
    for i in range(3):
        sentence = makeRandomizedBigramSentence(unigramsFreqDict, bigramsFreqDict)
        f.write(sentence)
        f.write("\n")
    f.write("\nTrigrams model based on complete dataset:\n")
    trigramsFreqDict = makeTrigramsFrequencyDict(completeDict)
    for i in range(3):
        sentence = makeRandomizedTrigramSentence(unigramsFreqDict, bigramsFreqDict,trigramsFreqDict, bigrams)
        f.write(sentence)
        f.write("\n")
    f.write("\nTrigrams model based on text written by users from " + countryNames[0] + ":\n")
    firstCountryDataSet = createListForWords(countryList.get(countryNames[0]))
    firstCountryBigrams = wordsToNgrams(firstCountryDataSet, 2," ")
    firstCountryUnigramsDict = createFrequencyDictForWords(firstCountryDataSet)
    firstCountryBigramsDict = makeBigramsFrequencyDict(firstCountryDataSet)
    firstCountryTrigramsDict = makeTrigramsFrequencyDict(firstCountryDataSet)
    for i in range(3):
        sentence = makeRandomizedTrigramSentence(firstCountryUnigramsDict, firstCountryBigramsDict, firstCountryTrigramsDict, firstCountryBigrams)
        f.write(sentence)
        f.write("\n")
    f.write("\nTrigrams model based on text written by users from " + countryNames[1] + ":\n")
    secondCountryDataSet = createListForWords(countryList.get(countryNames[1]))
    secondCountryBigrams = wordsToNgrams(secondCountryDataSet, 2," ")
    secondCountryUnigramsDict = createFrequencyDictForWords(secondCountryDataSet)
    secondCountryBigramsDict = makeBigramsFrequencyDict(secondCountryDataSet)
    secondCountryTrigramsDict = makeTrigramsFrequencyDict(secondCountryDataSet)
    for i in range(3):
        sentence = makeRandomizedTrigramSentence(secondCountryUnigramsDict, secondCountryBigramsDict, secondCountryTrigramsDict, secondCountryBigrams);
        f.write(sentence)
        f.write("\n")
    f.close()


def removeBeginningTag(line):
    return re.sub("<s>", '', line)

def removeEndingTag(line):
    return re.sub("</s>", '', line)

def insertSpacesBetweenTokens(sentence):
    chars = re.compile(r"([.,()!?:])")
    sentence = chars.sub(" \\1 ", sentence)
    return sentence

def removeOneCharSentence(text):
    return re.sub("^.{1}$", '', text)

def createListForWords(sentencesList):
    tokensList = []
    for sentence in sentencesList:
        sentence = insertSpacesBetweenTokens(sentence)
        sentence = removeOneCharSentence(sentence)  
        sentence = sentence.lower()
        tokens = sentence.split()
        tokensList.extend(tokens)
    return tokensList

def marksRules(word, n, i):
    if (n != 1):
        if((word=="</s>") and (i+1 != n)):
            return False
        elif ((word=="<s>") and (i+1 != 1)):
            return False
    return True

# calculating the ngrams 
def wordsToNgrams(tokens, n, sep = " "):
    ngrams = [sep.join(tokens[i : i + n])  for i in range(len(tokens) - n + 1) if marksRules(tokens[i], n, i%n)]
    return ngrams


######################################################################################
# Functions for creating the Frequency Dictionaries for all the three models
###################################################################################### 
def createFrequencyDictForWords(words):
    wordsDictionary = {}
    for word in words:
        # when we count the words, we don't want the beginning and the ending marks to be counted
            wordsDictionary[word] = wordsDictionary.get(word, 0) + 1
    return wordsDictionary

######################################################################################
       
def makeBigramsFrequencyDict(tokens):
    bigrams = wordsToNgrams(tokens, 2," ")
    bigramsFrequencyDict = {}
    for bigram in bigrams:
                word1, word2 = bigram.split(" ")
                if word1 in bigramsFrequencyDict:
                        if word2 in bigramsFrequencyDict[word1]:
                            bigramsFrequencyDict[word1][word2] += 1
                        else:
                            bigramsFrequencyDict[word1][word2] = 1
                else:
                        bigramsFrequencyDict[word1] = {}
                        bigramsFrequencyDict[word1][word2] = 1
    return bigramsFrequencyDict 
   
######################################################################################
    
def makeTrigramsFrequencyDict(tokens):
    trigrams = []
    trigramsFrequencyDict = {}
    index = 0
    while(index != len(tokens) - 2):
        trigrams.append(tokens[index] + ' ' + tokens[index+1] + ' ' + tokens[index+2])
        index += 1
 
    for trigram in trigrams:      
        if trigram in trigramsFrequencyDict:
                
            trigramsFrequencyDict[trigram] += 1
        else:
            trigramsFrequencyDict[trigram] = 1
    return trigramsFrequencyDict 


######################################################################################
# Unigrams Language Model - Generating a random sentence
######################################################################################      

def makeRandomizedUnigramSentence(unigrams):
    tokens = []
    wordsFrequency = []
    sentence = ''
    for value in unigrams.values():
        wordsFrequency.append(value)
    for key in unigrams.keys():
        tokens.append(key)
    nextWord = choices(tokens, wordsFrequency, k = 1)
    currWord = ''.join(nextWord)
    while (currWord!='</s>'):
                nextWord = choices(tokens, wordsFrequency, k = 1)
                sentence = sentence + ' '.join(nextWord) + ' '
                currWord = ''.join(nextWord)
    # removing the ending mark of the sentence
    sentence = removeEndingTag(sentence)
    # removing the begnning mark of the sentence    
    sentence = removeBeginningTag(sentence)            
    return sentence

######################################################################################
# Bigrams Language Model - Generating a random sentence
######################################################################################
    
def calcBigramProbability(bigram, unigramsFreqDict, bigramsFreqDict, bigrams):
    bigramProbabilityDict = {}
    for currBigram in bigrams:
        word1, word2 = currBigram.split(" ")
        bigramProbabilityDict[currBigram] = bigramsFreqDict[word1][word2]/unigramsFreqDict[word1]
    if bigram in bigramProbabilityDict:
        return bigramProbabilityDict[bigram]
    return 0

      
def makeRandomizedBigramSentence(unigrams, bigrams):
    # setting the first word as the beginning mark <s>
    nextWord = '<s>'    
    sentence = nextWord
    lastWord = nextWord
    while (nextWord != '</s>'):
            if lastWord in bigrams:
                values = bigrams[lastWord]
                nextWord = choices(list(values), values.values(), k = 1)                
            else:
                nextWord = choices(list(unigrams.keys()), unigrams.values(), k = 1)
            sentence = sentence + ' '.join(nextWord) + ' '
            nextWord = ''.join(nextWord)
            lastWord = nextWord                
    # removing the ending mark of the sentence
    sentence = removeEndingTag(sentence)
    # removing the begnning mark of the sentence    
    sentence = removeBeginningTag(sentence)
    return sentence

######################################################################################
# Trigrams Language Model - Generating a random sentence
###################################################################################### 
     
def makeRandomizedTrigramSentence(unigramsFreqDict, bigramsFreqDict,trigramsFreqDict, bigrams):
    words = []
    probabilities = []
    lastWord = "<s>"
    for bigram in bigrams:
        word1, word2 = bigram.split(" ")
        if (word1=='<s>'):
            words.append(word2)
            bigramProbability = bigramsFreqDict[word1][word2]/unigramsFreqDict[word1]
            probabilities.append(bigramProbability)          
    sentence = ''
    randomWord=choices(words, probabilities)
    while(randomWord[0] != "</s>"):
        sentence += randomWord[0] + ' '
        nextWord = randomWord[0]
        words = []
        probabilities = []
        for trigram in trigramsFreqDict:
            word1, word2, word3 = trigram.split(" ") 
            if word1==lastWord and word2==nextWord:
                words.append(word3)
                trigramProbability = trigramsFreqDict[trigram]/bigramsFreqDict[word1][word2]
                probabilities.append(trigramProbability)       
        randomWord = choices(words,probabilities)
        lastWord = nextWord
    return sentence
              
            
######################################################################################
# Unigram Sentence Probability Calculation with laplace smoothing
###################################################################################### 
    
def calctUnigramProbability(tokens, word, unigramFrequencyDict):
    wordProbabilityNumerator = unigramFrequencyDict.get(word, 0)
    wordProbabilityDenominator = sum(unigramFrequencyDict.values())
    unigramTypes  = len(tokens)
    # making laplace smoothing to the words that are not existing 
    if word not in tokens:
        wordProbabilityNumerator += 1
        wordProbabilityDenominator += unigramTypes + 1
    unigramProbability = float(wordProbabilityNumerator/wordProbabilityDenominator)
    return unigramProbability

def calcUnigramSentenceProbability(sentence, tokens, unigramFrequencyDict):
    sentence = ' <s> ' + sentence + ' </s> '
    sentence = sentence.lower()
    wordSentence = sentence.split(' ')
    sentenceProbabilityLogSum = 0
    for word in wordSentence:
            wordProbability = calctUnigramProbability(tokens, word, unigramFrequencyDict)
            sentenceProbabilityLogSum += math.log(wordProbability, 2)
    return math.pow(2, sentenceProbabilityLogSum)


######################################################################################
# Bigram Sentence Probability Calculation with backoff algorithm
###################################################################################### 

def calcBigramSentenceProbability(sentence, unigramFreqDict, bigramFreqDict):
    prevWord = '<s>'
    currWord = ''
    sentence = sentence.lower()
    wordSentence = sentence.split(' ')
    bigramSentenceProbabilityLogSum = 0.0
    total = sum(unigramFreqDict.values())
    for word in wordSentence:
     	currWord = word
     	bigramsCounts = bigramFreqDict.get((prevWord,currWord), 0)
     	if (bigramsCounts > 0):
     	    bigramSentenceProbabilityLogSum += math.log(bigramsCounts)
     	    bigramSentenceProbabilityLogSum -= math.log(unigramFreqDict.get(prevWord, 0))
     	else:
     	    bigramSentenceProbabilityLogSum += math.log(0.4) + math.log(unigramFreqDict.get(currWord, 0)+1)
     	    bigramSentenceProbabilityLogSum -= math.log(total + (len(unigramFreqDict)))
    prevWord = word
    currWord = '</s>'
    bigramsCounts =  bigramFreqDict.get((prevWord,currWord), 0)
    if (bigramsCounts > 0):
     	bigramSentenceProbabilityLogSum += math.log(bigramsCounts)
     	bigramSentenceProbabilityLogSum -= math.log(unigramFreqDict.get(prevWord, 0))
    else:
     	bigramSentenceProbabilityLogSum += math.log(0.4) + math.log(unigramFreqDict.get(currWord, 0)+1)
     	bigramSentenceProbabilityLogSum -= math.log(total + (len(unigramFreqDict)))
    return math.pow(2, bigramSentenceProbabilityLogSum)

#######################################################################################
# Trigram Sentence Probability Calculation using Linear Interpolation
####################################################################################### 
def calcTrigramProbability(trigram, trigramFreqDict):
    trigramProbabilityDict = {}
    trigram = trigram.lower()
    numTrigrams = len(trigramFreqDict)
    for trigrams in trigramFreqDict:
        trigramProbabilityDict[trigrams] = trigramFreqDict[trigrams]/numTrigrams
    if trigram in trigramProbabilityDict:
        return trigramProbabilityDict[trigram]
    return 0

def calcLinearInterpolation(sentence, unigramsFreqDict, bigramsFreqDict, trigramsFreqDict, tokens):
    sentence = ' <s> ' + sentence + ' </s> '
    sentence = sentence.lower()
    words = sentence.split(" ") 
    sentenceTrigrams = wordsToNgrams(words, 3,' ')
    lamda = 1/3.0
    linearInterpolatedProbability = 0
    i = 0
    for trigram in sentenceTrigrams:
            bigram = ' '.join(words[i:i+2])
            unigram = words[i]
            i += 1
            #looking for a trigram, returns 0 if doesn't find
            p3 = calcTrigramProbability(trigram, trigramsFreqDict)
            # calculate the probability in bigrams using backoff
            p2 = calcBigramSentenceProbability(bigram, unigramsFreqDict, bigramsFreqDict)
            p1 = calctUnigramProbability(tokens, unigram, unigramsFreqDict)
            linearInterpolatedProbability += lamda * (p3 + p2 + p1)
    return linearInterpolatedProbability
#######################################################################################    

     
#MAIN PROGRAM STARTS HERE:
inputDir = str(sys.argv[1])
outputDir = str(sys.argv[2])
inputDir = glob.glob(inputDir + "/*.txt")

countryList = dict()
completeDict = []
for address in inputDir:
    file = open(address,"r")
    fileName = os.path.basename(file.name)
    countryName = findCountry(fileName)
        
    for line in file:
                if countryName not in countryList: 
                    countryList[countryName] = []
                else:
                        # adding every line with beginning and ending mark
                    countryList[countryName].append(" <s> " + line.strip() + " </s> ")
                                                       
    tokens = createListForWords(countryList.get(countryName))
    
    file.close()
    completeDict.extend(tokens)

createOutput(completeDict, countryList, outputDir)
print("Done!")
