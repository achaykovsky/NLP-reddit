# -*- coding: utf-8 -*-
import sys
import glob
import os
import csv
import re
from operator import itemgetter

def readFileAndCreateDataStructure(csv_reader):
    users_dict = dict()
    #getting the line in the file
    for line in csv_reader:
        # defining the key
            key = line[0]
        # check if the key already present in dict
            if key not in users_dict:
                users_dict[key] = []
        # append the post
            else:
                users_dict[key].append(line[3])
    return users_dict
                
def findCountry(address):
    m = re.search('reddit.(.+?).clean.en.post', address)
    if m:
        found = m.group(1) 
    return found   

def createFileForUser(userName, countryName, sentences, outputDir):
    f = open(f'{outputDir}\{userName}_{countryName}.txt', 'w+', encoding="utf-8")
    for sentence in sentences:
        words = tokenToWords(sentence)
        for word in words:
                f.write(word)
        f.write("\n")
    f.close()
    
def createDictForSentences(new_users_dict):
    users_sentences = dict()
    for userName in new_users_dict:
        if userName not in users_sentences:
            users_sentences[userName] = []
        for message in new_users_dict.get(userName):
            sentences = splitToSentences(message)
            for sentence in sentences:
                sentence = removeOneCharSentence(sentence)       
                if(sentence!=''):
                    users_sentences[userName].append(sentence)
    return users_sentences
     
def removeUrl(text):
    output = re.sub(r'http[s]?://\S+\b.', "", text)
    return output

def replaceEM(g):
    return g.group(0).replace('!', '')

def replaceQM(g):
    return g.group(0).replace('?', '')

def replacePeriods(g):
    return g.group(0).replace('.', '')

def removeEMInParenthesses(text):
    return re.sub(r'\(.*?\)', replaceEM, text)

def removeQMInParenthesses(text):
    return re.sub(r'\(.*?\)', replaceQM, text)

def removePeriodsInParenthesses(text):
    return re.sub(r'\(.*?\)', replacePeriods, text)

def removePunctuationInParenthesses(text):
    text = removeQMInParenthesses(text)
    text = removePeriodsInParenthesses(text)
    text = removeEMInParenthesses(text)
    return text

def removeExtraPunctuation(text):
    return re.sub('(?<=[,.?!])[,.?!]+', '', text) 


def removeChars(text):
    output = re.sub('[-_~\=%$€\"^*¿/+@|\\#><]', ' ', text)
    return output
    
def removeParentheses(text):
    text = re.sub('\(\s*\)', '', text)
    text = text.replace('[', '')
    text = text.replace(']', '')
    text = text.replace('{', '')
    text = text.replace('}', '')
    return text

    
def removeEmoticonss(text):
    emoticonsList = [':‑)',':)',':-]',':]',':-3',':3',':->',':>','8-)','8)',	':-}',':}',':o)',':c)',':^)','=]','=)',':D',':,',':.',';)',
                     ':‑D',':D','8‑D','8D','x‑D','xD','X‑D','XD','=D','=3','B^D',':-))',':‑(',':(',':‑c',':c',':‑<',':<,',':c',':‑<',':<',':‑[',':[',':-||',
                     '>:[',':{',':@','>:(',';(','D:<','D:','D8','D;','D=','DX',':‑O',':O',':‑o',':o',':-0','8‑0','>:O',':-*', ':*',':× ',';‑)',';)','*-)','*)',';‑]',';]',';^)',':‑,',';D',':P','X‑P','XP','XP','x‑p','xp',':‑p',':p',':Þ',':‑Þ',':þ',':‑b',':b','d:','=p','>:P',':‑/',':/',':‑.','>:\\',':S',':‑|',':|',':$']
    for i in emoticonsList:
        text = text.replace(i, '')
    return text

     
def removEmptyLines(new_users_dict):
    for key in new_users_dict:
        new_users_dict[key].remove()
    return new_users_dict

def removeHTMLtags(text):
    output = re.sub(re.compile('<.*?>'), '', text)
    return output

def removeEmails(text):
    output = re.sub('\S+@\S+', '', text)
    return output

def removeNumbers(text):
    output = re.sub(r'\b\d+\b',' ',text)
    return output

def removeOnlySpecialCharater(text): 
    output = re.sub('/^[^a-zA-Z0-9]+$/','',text)
    return output

def removeXMLtags(text):
    return re.sub("&#?\w+;", ' ', text)

def removeflairs(text):
    return re.sub("/[a-z]{1}/", '', text)

def removeDupliacteSpaces(text):
   return re.sub(r"\s{2,}", ' ', text)

def removeDupliacteChars(text):
   return re.compile(r'([^a-zA-Z0-9])\1{1,}', re.IGNORECASE).sub(r'\1',text)

def removeDupliacteAlphabet(text):
    return re.compile(r'(.)\1{2,}', re.IGNORECASE).sub(r'\1',text)

def removeOneCharSentence(text):
    return re.sub("^.{1}$", '', text)

def removeAbbreviations(text):
    return re.sub(r"\b[A-Z\.]{2,}\b", '', text)

def removeBlankrParentheses(text):
    return re.sub(r"\b()\b", '', text)

def containsNotAscii(s):
    return any(ord(i)>127 for i in s)
    
def removeNotEnglishWords(text):
    words = text.split()
    cleanedWords = [word for word in words if not containsNotAscii(word)]
    cleanedText = ' '.join(cleanedWords)
    return cleanedText


def splitToSentences(post):
    post = " " + post + "  "
    post = post.replace("\n"," ")
    if "”" in post:
        post = post.replace(".”","”.")
    if "\"" in post:
        post = post.replace(".\"","\".")
    if "!" in post:
        post = post.replace("!\"","\"!")
    if "?" in post:
        post = post.replace("?\"","\"?")
    post = post.replace(".",".<stop>")
    post = post.replace("?","?<stop>")
    post = post.replace("!","!<stop>")
    sentences = post.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences
   


def countSentencesInPost(post):
  sentencesList = splitToSentences(post)
  return len(sentencesList)

#gets a value for certain key(messages list of the same user)
def countSentencesPerUser(userMessageList):
    postSentences, userSentences = 0, 0
    for post in userMessageList:
        postSentences = countSentencesInPost(post)
        userSentences += postSentences
    return userSentences

def createFrequencyDict(sentencesDict):
    sentencesFrequencyDict = dict()
    for user in sentencesDict:
            sentencesFrequencyDict[user] = countSentencesPerUser(sentencesDict[user])
    return sentencesFrequencyDict

def findNlargest(sentencesFrequencyDict):
    sortedDict = sorted(sentencesFrequencyDict.items(), key = itemgetter(1), reverse = True)
    NlargestDict = dict(sortedDict[:numOfUsers])
    return NlargestDict

    #method to create the files with the users who posted the most
def createNMostFrequentUsersPerFile(address,sentencesFrequencyDict,sentencesDict):
    countryName = findCountry(address)
    NlargestDict = findNlargest(sentencesFrequencyDict)
    for userName in NlargestDict.keys():
                createFileForUser(userName, countryName, sentencesDict[userName],outputDir)

def tokenToWords(sentence):
    splitedSentenceToWords = []
    sentence = insertSpacesBetweenTokens(sentence)
    words = sentence.split()
    splitedSentenceToWords.append('' + ' '.join(words) + '')
    return splitedSentenceToWords

def insertSpacesBetweenTokens(sentence):
    pat = re.compile(r"([.,()!?:])")
    sentence = pat.sub(" \\1 ", sentence)
    return sentence

#MAIN PROGRAM STARTS HERE:
  

inputDir = str(sys.argv[1])
numOfUsers = int(sys.argv[2])
outputDir = str(sys.argv[3])
inputDir = glob.glob(inputDir + "/*.csv")
for address in inputDir:
                csv_file =  open(address, encoding="utf8")
                csv_reader = csv.reader(csv_file, delimiter=',')
                users_dict = readFileAndCreateDataStructure(csv_reader)
                new_users_dict = dict()
                for key in users_dict.keys():
                        for message in users_dict.get(key):
                            message = removeUrl(message)
                            message = removeExtraPunctuation(message)                           
                            message = removeNumbers(message)
                            message = removeEmails(message)
                            message = removeflairs(message)            
                            message = removeHTMLtags(message)
                            message = removeXMLtags(message)
                            message = removeChars(message)
                            message = removeEmoticonss(message)
                            message = removePunctuationInParenthesses(message)                    
                            message = removeParentheses(message)                    
                            message = removeOnlySpecialCharater(message)
                            message = removeNotEnglishWords(message)
                            message = removeBlankrParentheses(message)
                            message = removeDupliacteChars(message)
                            message = removeDupliacteAlphabet(message)
                            message = removeDupliacteSpaces(message)
                    # creating a clean dictionary
                            if key not in new_users_dict:
                                new_users_dict[key] = []
                            else:
                                new_users_dict[key].append(message)
                       
                sentencesDict = createDictForSentences(new_users_dict)
                sentencesFrequencyDict = createFrequencyDict(sentencesDict)
                createNMostFrequentUsersPerFile(address,sentencesFrequencyDict,sentencesDict)
                csv_file.close()
                print("Done!")