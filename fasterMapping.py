
import numpy as np
from gensim.models import KeyedVectors
from moralWordsDict import moralWordsDict, morals
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from scipy.spatial.distance import cosine
import re

fname = 'word2vec.kv'
model = KeyedVectors.load(fname, mmap='r')
wordVectors = model.wv


moralWords = list(moralWordsDict.keys())
stop_words = set(stopwords.words('english'))

approxWordDict = {
        'sympath': 'sympathy',
        'warl': 'warlord',
        'violen': 'violence',
        'fair-': 'fair',
        'fairmind': 'fair',
        'justifi': 'justified',
        'reciproc': 'reciprocity',
        'egalitar': 'egalitarian',
        'unprejudice': 'unprejudiced',
        'discriminat': 'discrimination',
        'prejud': 'prejudice',
        'segregat': 'segregation',
        'exclud': 'exclude',
        'comrad': 'comradery',
        'collectiv': 'collective',
        'devot': 'devotion',
        'cliqu': 'clique',
        'enem': 'enemy',
        'treacher': 'treachery',
        'deceiv': 'deceive',
        'terroris': 'terrorism',
        'obedien': 'obedience',
        'duti': 'dutiful',
        'motherl': 'motherly',
        'authorit': 'authority',
        'complian': 'compliance',
        'submi': 'submission',
        'allegian': 'allegiance',
        'defere': 'deference',
        'venerat': 'veneration',
        'defian': 'defiance',
        'subver': 'subvert',
        'disobe': 'disobey',
        'sediti': 'sedition',
        'agitat': 'agitate',
        'insubordinat': 'insubordination',
        'steril': 'sterile',
        'chast': 'chastity',
        'celiba': 'celibacy',
        'abstinen': 'abstinence',
        'decen': 'decency',
        'deprav': 'depraved',
        'contagio': 'contagious',
        'indecen': 'indecency',
        'profan': 'profanity',
        'repuls': 'repulsive',
        'promiscu': 'promiscuous',
        'adulter': 'adultery',
        'debauche': 'debauchery',
        'prostitut': 'prostitution',
        'obscen': 'obscene',
        'desecrat': 'desecrate',
        'exploitat': 'exploitation'
    }

def get_moral_values(text, method, threshold):
    return


def getMoralCategoryVector(category):
    '''
    Inputs
    ____
    category: int (1-11)
        Integer corresponding to category (see moralWordsDict)
    '''
    moralWords = []
    for moralWord in morals[category - 1][0]:
        if "*" in moralWord:
            moralWord = moralWord[:-1]
        if moralWord not in wordVectors:
            moralWord = approxWordDict[moralWord]
        moralWords.append(moralWord)
    moralWordVectors = [wordVectors[moralWord] for moralWord in moralWords]
    avgMoralVector = np.average(moralWordVectors, axis=0)
    return avgMoralVector

moralCategoryVectors = [getMoralCategoryVector(category) for category in range(1, 12)]

def initializeMapping():
    '''
    By Index:
        0 = Harm
        1 = Fairness
        2 = Ingroup
        3 = Authority
        4 = Purity
        5 = Morality
    '''
    return np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

def getBagOWords(text):
    toks = word_tokenize(re.sub(r'[^a-zA-Z0-9 ]', '', text).lower())
    # return [w for w in toks if w not in stop_words]
    return [w for w in toks if w in moralWords or w in wordVectors.vocab]

def getBagMappingAvg(bagOWords):
    bagMapping = initializeMapping()
    bagOWords = [w for w in bagOWords if w in wordVectors.vocab]
    if(len(bagOWords) > 0):
        bagWordVectors = [wordVectors[word] for word in bagOWords]
        bagVector = np.average(bagWordVectors, axis=0)
        distancesToBag = {}
        i = 1
        for moralCategoryVector in moralCategoryVectors:
            distancesToBag[i] = cosine(bagVector, moralCategoryVector)
            i += 1

        for i in range(1,11, 2):
            distanceToPosCategory = distancesToBag[i]
            distanceToNegCategory = distancesToBag[i+1]
            value = distanceToPosCategory + -1 * distanceToNegCategory
            bagMapping = updateMapping(bagMapping, i, value)
    return bagMapping[:5]

def getAvgDocVectors(bagOWords):
    bagMapping = initializeMapping()
    bagOWords = [w for w in bagOWords if w in wordVectors.vocab]
    bagWordVectors = [np.zeros(300)]
    if(len(bagOWords) > 0):
        bagWordVectors = [wordVectors[word] for word in bagOWords]
    bagVector = np.average(bagWordVectors, axis=0)
    return bagVector

                

def getBagMapping(bagOWords):
    bagMapping = initializeMapping()
    # Moral dictionary words
    moralBagWords = []
    wordsUsed = []
    for word in bagOWords:
        for moralWord in moralWords:
            if word.find(moralWord) == 0:
                moralBagWords.append(moralWord)
                wordsUsed.append(word)
    for moralWord in moralBagWords:
        morals = moralWordsDict[moralWord]
        for moral in morals:
            if moral % 2 == 1:
                value = 1
            else:
                value = -1
            bagMapping = updateMapping(bagMapping, moral, value)
    # Bag2Vec
    otherBagWords = [word for word in bagOWords if word not in wordsUsed and word in wordVectors.vocab]
    if otherBagWords:
        bagWordVectors = [wordVectors[word] for word in otherBagWords]
        bagVector = np.average(bagWordVectors, axis=0)
        # Distances from bag vector to moral vectors
        distancesToBag = {}
        categories = np.arange(1, 12)
        i = 0
        for moralCategoryVector in moralCategoryVectors:
            distancesToBag[categories[i]] = cosine(bagVector, moralCategoryVector)
            i += 1
        # Update bag mapping
        for category in categories:
            distanceToCategory = distancesToBag[category]
            if category % 2 == 1:
                value = 1 * (1-distanceToCategory)
            else:
                value = -1 * (1-distanceToCategory)
            bagMapping = updateMapping(bagMapping, category, value)
    # Scale bag mapping
    bagMapping /= np.sum(np.abs(bagMapping))
    return bagMapping[:5]

def getBagMappingThresh(bagOWords, threshold=0.9):
    bagMapping = initializeMapping()
    # Moral dictionary words
    moralBagWords = []
    wordsUsed = []
    for word in bagOWords:
        for moralWord in moralWords:
            if word.find(moralWord) == 0:
                moralBagWords.append(moralWord)
                wordsUsed.append(word)
    for moralWord in moralBagWords:
        morals = moralWordsDict[moralWord]
        for moral in morals:
            if moral % 2 == 1:
                value = 1
            else:
                value = -1
            bagMapping = updateMapping(bagMapping, moral, value)
    # Bag2Vec

    otherBagWords = [word for word in bagOWords if word not in wordsUsed and word in wordVectors.vocab]
    if otherBagWords:

        for word in otherBagWords:
            wordvec = wordVectors[word]
            # Distances from bag vector to moral vectors
            distancesToBag = {}
            categories = np.arange(1, 12)
            i = 0
            for moralCategoryVector in moralCategoryVectors:
                distancesToBag[categories[i]] = cosine(wordvec, moralCategoryVector)
                i += 1
            # Update bag mapping
            for category in categories:
                distanceToCategory = distancesToBag[category]
                if distanceToCategory < 1-threshold:
                    if category == 10:
                        print(str(distanceToCategory) + '   ' + word + '   ' + str(category))
                        print(str(cosine(wordvec, wordVectors['lewd'])))
                    if category % 2 == 1:
                        value = 1 * (1-distanceToCategory)
                    else:
                        value = -1 * (1-distanceToCategory)
                    bagMapping = updateMapping(bagMapping, category, value)
    # Scale bag mapping

    bagMapping /= np.sum(np.abs(bagMapping))
    return bagMapping[:5]

def get_category_distance(word, category):
    if word in wordVectors.vocab:
        wordvec = wordVectors[word]
        moralvec = moralCategoryVectors[category]
        return cosine(wordvec,moralvec)

def updateMapping(mapping, moral, value):
    # Harm
    if moral == 1 or moral == 2:
        mapping[0] += value
    # Fairness
    elif moral == 3 or moral == 4:
        mapping[1] += value
    # Ingroup
    elif moral == 5 or moral == 6:
        mapping[2] += value
    # Authority
    elif moral == 7 or moral == 8:
        mapping[3] += value
    # Purity
    elif moral == 9 or moral == 10:
        mapping[4] += value
    # Morality
    elif moral == 11:
        mapping[5] += value
    return mapping