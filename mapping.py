
import numpy as np
from gensim.models import KeyedVectors
from moralWordsDict import moralWordsDict


moralWords = list(moralWordsDict.keys())

fname = '/Users/samdeverett/Documents/Citadel_Datathon/word2vec.kv'
model = KeyedVectors.load(fname, mmap='r')


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

def getBagMapping(bagOfWords):
    bagMapping = initializeMapping()
    for word in bagOfWords:
        bagMapping += getWordMapping(word)
    bagMapping /= len(bagOfWords)
    return bagMapping

def getWordMapping(word):
    wordMapping = initializeMapping()
    # Moral Dictionary
    for moralWord in moralWords:
        ### Is this valid? (ex: does 'suffer$%/@' == 'suffer'?)
        if word.find(moralWord) == 0:
            morals = moralWordsDict[moralWord]
            for moral in morals:
                if moral % 2 == 1:
                    value = 1
                else:
                    value = -1
                wordMapping = updateMapping(wordMapping, moral, value)
            break
    # Word2Vec
    else:
        ### THRESHOLD???
        wordVectors = model.wv
        if word in wordVectors:
            distancesToWord = {}
            for moralWord in moralWords:
                if moralWord not in wordVectors:
                    moralWord = approxWordDict[moralWord]
                distancesToWord[moralWord] = model.similarity(moralWord, word)
            closestWordVector = max(distancesToWord, key=distancesToWord.get)
            distToClosestWV = distancesToWord[closestWordVector]
            if closestWordVector not in moralWords:
                for k, v in approxWordDict.items():
                    if v == closestWordVector:
                        closestWordVector = k
                        break
            morals = moralWordsDict[closestWordVector]
            for moral in morals:
                if moral % 2 == 1:
                    value = 1 * distToClosestWV
                else:
                    value = -1 * distToClosestWV
                wordMapping = updateMapping(wordMapping, moral, value)
    return wordMapping

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


# print(getWordMapping('pain'))
# print(getWordMapping('suffering'))
# print(getBagMapping(['pain', 'suffering']))
