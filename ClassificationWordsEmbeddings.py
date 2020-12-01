# -*- coding: utf-8 -*-
import sys
import glob
import os
import re
import random
from sklearn.feature_selection import SelectKBest
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from gensim.models import KeyedVectors

CHUNKSIZE = 20

inputDir = str(sys.argv[1])
preTraindWord2vec = str(sys.argv[2])
myWord2vec = str(sys.argv[3])
outputDir = str(sys.argv[4])
inputDir = glob.glob(inputDir + "/*.txt")

######################################################################################
# Loading Models
######################################################################################
MODEL_FILE = preTraindWord2vec
word2vec_pre_trained_model = KeyedVectors.load_word2vec_format(MODEL_FILE, binary=False)
MODEL_FILE = myWord2vec
word2vec_my_trained_model = KeyedVectors.load_word2vec_format(MODEL_FILE, binary=False)
######################################################################################


def findCountryName(address):
    m = re.search('(.+?).txt', address)
    if m:
        found = m.group(1)
    return found


def readFiles(inputDir):
    counter = 0
    objects = dict()
    classes = dict()
    for address in inputDir:
        file = open(address, "r", encoding="utf-8")
        fileName = os.path.basename(file.name)
        name = findCountryName(fileName)
        lines = 0

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
    return objects, classes


######################################################################################
# Merging every 'CHUNKSIZE' (default=20) sentences to sets and set a label to it in one country
######################################################################################
def mergeSentences(sentences, numOfClass):
    numofLines = 1
    dataset = []
    targets = []
    newSentence = ''
    for sentence in sentences:
        if numofLines < CHUNKSIZE:
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
def classifySentences(objects, classes):
    dataset = []
    targets = []
    for name in objects:
        # sets the number of the class by the name (of the user name ot the country)
        numOfClass = classes[name]
        mergedSet, mergedSentencesTargets = mergeSentences(objects[name], numOfClass)
        dataset.extend(mergedSet)
        targets.extend(mergedSentencesTargets)
    return dataset, targets


######################################################################################
# Arithmetic mean calculation functions
######################################################################################
def calculateSentenceArithmeticWeight(sentence,model):
    sentenceFeatureVector, weight = 0, 1
    words = sentence.split()
    for word in words:
        if word in model.vocab:
            wordVector = weight*model[word]
            sentenceFeatureVector += wordVector
    sentenceFeatureVector /= CHUNKSIZE
    return sentenceFeatureVector

def calculateSentencesWeight(dataset,model):
    datasetVectors = []
    for sentence in dataset:
        sentenceFeatureVector = calculateSentenceArithmeticWeight(sentence, model)
        datasetVectors.append(sentenceFeatureVector)
    return datasetVectors

def calculateScores(dataset, targets, model):
    lgClassifier = LogisticRegression(solver='liblinear', multi_class='auto', max_iter=1000)
    datasetVectors = calculateSentencesWeight(dataset, model)
    skf = StratifiedKFold(n_splits=10, shuffle=True)
    scores = cross_validate(lgClassifier, datasetVectors, targets, cv=skf, scoring=['accuracy', 'precision_macro', 'recall_macro', 'f1_macro'])
    return scores
##############################################################################################
# Random weights calculation functions
##############################################################################################
def calculateSentenceRandomWeight(sentence,model):
    sentenceFeatureVector = 0
    words = sentence.split()
    for word in words:
        if word in model.vocab:
                weight = random.random()
                wordVector = weight*model[word]
                sentenceFeatureVector += wordVector
    sentenceFeatureVector /= CHUNKSIZE
    return sentenceFeatureVector

def calculateSentencesRandomWeight(dataset,model):
    datasetVectors = []
    for sentence in dataset:
        sentenceFeatureVector = calculateSentenceRandomWeight(sentence, model)
        datasetVectors.append(sentenceFeatureVector)
    return datasetVectors

def calculateRandomScores(dataset, targets, model):
    lgClassifier = LogisticRegression(solver='liblinear', multi_class='auto', max_iter=1000)
    datasetVectors = calculateSentencesRandomWeight(dataset, model)
    skf = StratifiedKFold(n_splits=10, shuffle=True)
    scores = cross_validate(lgClassifier, datasetVectors, targets, cv=skf, scoring=['accuracy', 'precision_macro', 'recall_macro', 'f1_macro'])
    return scores
######################################################################################
# My Weights calculation functions
######################################################################################

def calculatK100BestWordsNLI():
    kBestWords = ['aa', 'albania', 'albanian', 'albanians', 'argentina', 'argentinian', 'army', 'atx', 'bb', 'bbs', 'bipolar',
                  'british', 'chakra', 'countries', 'country', 'cpu', 'cum', 'cv', 'cvs', 'cypriot', 'cypriots', 'cyprus',
                  'damage', 'dds', 'dont', 'economy', 'english', 'eu', 'european', 'eurozone', 'fedora', 'fucking', 'game',
                  'georgia', 'georgian', 'georgians', 'government', 'gpu', 'greece', 'greek', 'greeks', 'island', 'israel', 'itachi',
                  'just', 'kakashi', 'kinda', 'konoha', 'linux', 'liverpool', 'malta', 'maltese', 'mate', 'michigan', 'military', 'minato',
                  'motherboard', 'ms', 'msu', 'naruto', 'nicosia', 'north', 'northern', 'obito', 'oh', 'osu', 'parliament', 'pcpartpicker',
                  'players', 'political', 'population', 'psu', 'pussy', 'ram', 'republic', 'rez', 'russia', 'russian', 'ryzen', 'sakura', 'sasuke',
                  'settlers', 'sharingan', 'smite', 'spanish', 'state', 't10', 'trnc', 'trp', 'turkey', 'turkish', 'turks', 'uchiha', 'uk', 'ukraine',
                  'ukrainian', 'united', 'war', 'women', 'ymir']
    return kBestWords

def calculatK300BestWordsNLI():
    kBestWords = ['8gb', 'aa', 'aires', 'akel', 'albania', 'albanian', 'albanians', 'amazon', 'amd', 'american', 'argentina', 'argentinian',
                  'armour', 'army', 'assassin', 'atx', 'b1g', 'bailout', 'bank', 'banks', 'bases', 'bb', 'bbs', 'beads', 'bipolar', 'boyfriend',
                  'britain', 'british', 'brits', 'buenos', 'build', 'buildapc', 'calories', 'candidate', 'cas', 'chakra', 'champion', 'citizens',
                  'citizenship', 'cock', 'college', 'communities', 'conflict', 'cooler', 'corsair', 'countries', 'country', 'coup', 'cpu', 'creed',
                  'crisis', 'cruisers', 'cum', 'cv', 'cvs', 'cypriot', 'cypriots', 'cyprus', 'damage', 'dd', 'ddr4', 'dds', 'debian', 'dems', 'didnt',
                  'discounts', 'doesnt', 'don', 'dont', 'dota', 'economic', 'economy', 'el', 'elections', 'enemy', 'english', 'enosis', 'ep', 'erdogan',
                  'ethnic', 'eu', 'euro', 'europe', 'european', 'euros', 'eurozone', 'fat', 'federal', 'fedora', 'females', 'forces', 'foreign', 'france',
                  'fsf', 'fuck', 'fucking', 'gaal', 'game', 'games', 'gems', 'genjutsu', 'georgia', 'georgian', 'georgians', 'germany', 'girls', 'gnu',
                  'gods', 'gop', 'government', 'gpu', 'greece', 'greek', 'greeks', 'guess', 'hashirama', 'hockey', 'hokage', 'idk', 'im', 'intel',
                  'invasion', 'iran', 'islam', 'islamist', 'island', 'israel', 'issue', 'itachi', 'just', 'jutsu', 'kakashi', 'kinda', 'konoha', 'kurdish',
                  'kurds', 'la', 'labour', 'latin', 'law', 'liberals', 'libre', 'limassol', 'linux', 'liverpool', 'll', 'ltr', 'lvg', 'madara', 'majority',
                  'malta', 'maltese', 'manic', 'mate', 'melo', 'merchant', 'michigan', 'military', 'minato', 'minister', 'mom', 'motherboard', 'moyes',
                  'ms', 'msi', 'msu', 'muscle', 'muslim', 'muslims', 'naruto', 'national', 'nationalist', 'nationalists', 'nato', 'newegg', 'nexus',
                  'nicosia', 'non', 'north', 'northern', 'obito', 'oc', 'oh', 'ok', 'okay', 'orbit', 'os', 'osu', 'palestinian', 'palestinians',
                  'parliament', 'parties', 'party', 'pc', 'pcpartpicker', 'ph', 'pill', 'pkk', 'play', 'players', 'playing', 'police', 'policies',
                  'policy', 'political', 'polls', 'population', 'price', 'primary', 'private', 'protein', 'psu', 'public', 'pussy', 'putin', 'pvp',
                  'que', 'quite', 'ram', 'range', 'rangers', 'rape', 'really', 'rebates', 'religious', 'republic', 'reunification', 'rez', 'rights',
                  'roc', 'rooney', 'russia', 'russian', 'russians', 'ryzen', 'sakura', 'sasuke', 'sata', 'sector', 'secular', 'senate', 'separatists',
                  'settlers', 'sharingan', 'shinobi', 'ship', 'shipping', 'ships', 'shit', 'shite', 'skin', 'smite', 'software', 'south', 'spanish',
                  'spank', 'ssd', 'state', 'storage', 'students', 'superbiiz', 'syria', 'syriza', 't10', 't8', 'tax', 'team', 'territories', 'thanks',
                  'tier', 'tiers', 'tobirama', 'torps', 'trnc', 'troops', 'trp', 'trump', 'tsunade', 'turkey', 'turkish', 'turks', 'uchiha', 'uk',
                  'ukraine', 'ukrainian', 'ukrainians', 'ult', 'unification', 'union', 'united', 've', 'war', 'weight', 'wg', 'windows', 'women',
                  'xfce', 'yeah', 'ymir', 'zao']
    return kBestWords


def calculateSentenceMyWeight(sentence,KBestWords, model):
        sentenceFeatureVector = 0
        words = sentence.split()
        weight = 1
        for word in words:
            if word in model.vocab:
                if word[0].isupper():
                    weight = 1.5
                # if word in KBestWords:
                #     weight = 2
                wordVector = weight * model[word]
                sentenceFeatureVector += wordVector
        sentenceFeatureVector /= CHUNKSIZE
        return sentenceFeatureVector

def calculateSentencesMyWeight(dataset,KBestWords, model):
        datasetVectors = []
        for sentence in dataset:
            sentenceFeatureVector = calculateSentenceMyWeight(sentence,KBestWords, model)
            datasetVectors.append(sentenceFeatureVector)
        return datasetVectors

def calculateMyWeightScores(dataset, targets, KBestWords, model):
        lgClassifier = LogisticRegression(solver='liblinear', multi_class='auto', max_iter=1000)
        datasetVectors = calculateSentencesMyWeight(dataset, KBestWords, model)
        skf = StratifiedKFold(n_splits=10, shuffle=True)
        scores = cross_validate(lgClassifier, datasetVectors, targets, cv=skf,
                                scoring=['accuracy', 'precision_macro', 'recall_macro', 'f1_macro'])
        return scores
        
######################################################################################
# MAIN PROGRAM STARTS HERE:
######################################################################################
# Loading the data from both tasks into the program
######################################################################################
objects, classes = readFiles(inputDir)
datasetNLI, targetsNLI = classifySentences(objects, classes)
###########################################################################
# Arithmetic mean:
###########################################################################
f = open(f'{outputDir}\output.txt', 'w+', encoding="utf-8")
scores = calculateScores(datasetNLI, targetsNLI, word2vec_pre_trained_model)
accuracy = scores['test_accuracy'].mean()*100
precision = scores['test_precision_macro'].mean()*100
recall = scores['test_recall_macro'].mean()*100
f1 = scores['test_f1_macro'].mean()*100
f.write("Arithmetic mean:\nPre-trained word2vec model performance:\n")
f.write("Accuracy: ")
f.write("{:.2f}%".format(accuracy))
f.write("\n")
f.write("Precision: ")
f.write("{:.2f}%".format(precision))
f.write("\n")
f.write("Recall: ")
f.write("{:.2f}%".format(recall))
f.write("\n")
f.write("F1: ")
f.write("{:.2f}%".format(f1))
f.write("\n")
scores = calculateScores(datasetNLI, targetsNLI, word2vec_my_trained_model)
accuracy = scores['test_accuracy'].mean()*100
precision = scores['test_precision_macro'].mean()*100
recall = scores['test_recall_macro'].mean()*100
f1 = scores['test_f1_macro'].mean()*100
f.write("My word2vec model performance:\n")
f.write("Accuracy: ")
f.write("{:.2f}%".format(accuracy))
f.write("\n")
f.write("Precision: ")
f.write("{:.2f}%".format(precision))
f.write("\n")
f.write("Recall: ")
f.write("{:.2f}%".format(recall))
f.write("\n")
f.write("F1: ")
f.write("{:.2f}%".format(f1))
f.write("\n")
f.write("---------------------------------------------------------------\n")
#########################################################################
# Random weights:
#########################################################################
scores = calculateRandomScores(datasetNLI, targetsNLI, word2vec_pre_trained_model)
accuracy = scores['test_accuracy'].mean()*100
precision = scores['test_precision_macro'].mean()*100
recall = scores['test_recall_macro'].mean()*100
f1 = scores['test_f1_macro'].mean()*100
f.write("Random weights:\nPre-trained word2vec model performance:\n")
f.write("Accuracy: ")
f.write("{:.2f}%".format(accuracy))
f.write("\n")
f.write("Precision: ")
f.write("{:.2f}%".format(precision))
f.write("\n")
f.write("Recall: ")
f.write("{:.2f}%".format(recall))
f.write("\n")
f.write("F1: ")
f.write("{:.2f}%".format(f1))
f.write("\n")
scores = calculateScores(datasetNLI, targetsNLI, word2vec_my_trained_model)
accuracy = scores['test_accuracy'].mean()*100
precision = scores['test_precision_macro'].mean()*100
recall = scores['test_recall_macro'].mean()*100
f1 = scores['test_f1_macro'].mean()*100
f.write("My word2vec model performance:\n")
f.write("Accuracy: ")
f.write("{:.2f}%".format(accuracy))
f.write("\n")
f.write("Precision: ")
f.write("{:.2f}%".format(precision))
f.write("\n")
f.write("Recall: ")
f.write("{:.2f}%".format(recall))
f.write("\n")
f.write("F1: ")
f.write("{:.2f}%".format(f1))
f.write("\n")
f.write("---------------------------------------------------------------\n")
############################################################################
# My weights:
############################################################################
KBestWords = calculatK300BestWordsNLI()#isn't used - to try, remove the comments in the function calculateSentenceMyWeight.
scores = calculateMyWeightScores(datasetNLI, targetsNLI, KBestWords, word2vec_pre_trained_model)
accuracy = scores['test_accuracy'].mean()*100
precision = scores['test_precision_macro'].mean()*100
recall = scores['test_recall_macro'].mean()*100
f1 = scores['test_f1_macro'].mean()*100
f.write("My weights:\nPre-trained word2vec model performance:\n")
f.write("Accuracy: ")
f.write("{:.2f}%".format(accuracy))
f.write("\n")
f.write("Precision: ")
f.write("{:.2f}%".format(precision))
f.write("\n")
f.write("Recall: ")
f.write("{:.2f}%".format(recall))
f.write("\n")
f.write("F1: ")
f.write("{:.2f}%".format(f1))
f.write("\n")
scores = calculateMyWeightScores(datasetNLI, targetsNLI, KBestWords, word2vec_my_trained_model)
accuracy = scores['test_accuracy'].mean()*100
precision = scores['test_precision_macro'].mean()*100
recall = scores['test_recall_macro'].mean()*100
f1 = scores['test_f1_macro'].mean()*100
f.write("My word2vec model performance:\n")
f.write("Accuracy: ")
f.write("{:.2f}%".format(accuracy))
f.write("\n")
f.write("Precision: ")
f.write("{:.2f}%".format(precision))
f.write("\n")
f.write("Recall: ")
f.write("{:.2f}%".format(recall))
f.write("\n")
f.write("F1: ")
f.write("{:.2f}%".format(f1))
f.write("\n")
f.write("---------------------------------------------------------------\n")
f.close()
######################################################################################

print("Done!")


# ######################################################################################
# # Examples for using the similarity for the wikipedia model
# ######################################################################################
# print(word2vec_pre_trained_model.similarity('cat', 'cats'))
# print(word2vec_pre_trained_model.similarity('cat', 'dog'))
# print(word2vec_pre_trained_model.similarity('small', 'big'))
# ######################################################################################
# # Examples for using the most_similar for the wikipedia model
# ######################################################################################
# print(word2vec_pre_trained_model.most_similar(positive=['animal', 'cute'], negative=['big']))
# print(word2vec_pre_trained_model.most_similar(positive=['jewish', 'religion']))
# print(word2vec_pre_trained_model.most_similar(positive=['beatles', 'songs']))
# ######################################################################################
# # Examples for using the similarity for my model
# ######################################################################################
# print(word2vec_my_trained_model.similarity('cat', 'cats'))
# print(word2vec_my_trained_model.similarity('cat', 'dog'))
# print(word2vec_my_trained_model.similarity('small', 'big'))
# ######################################################################################
# # Examples for using the most_similar for my model
# ######################################################################################
# print(word2vec_my_trained_model.most_similar(positive=['animal', 'cute'], negative=['big']))
# print(word2vec_my_trained_model.most_similar(positive=['jewish', 'religion']))
# print(word2vec_my_trained_model.most_similar(positive=['beatles', 'songs']))
# ######################################################################################