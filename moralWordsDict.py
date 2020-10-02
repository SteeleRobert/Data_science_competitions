
from collections import defaultdict

harmVirtue = [['safe*', 'peace*', 'compassion*', 'empath*', 'sympath*', 'care',
                'caring', 'protect*', 'shield', 'shelter', 'amity', 'secur*',
                'benefit*', 'defen*', 'guard*', 'preserve'], 1]

harmVice = [['harm*', 'suffer*', 'war', 'wars', 'warl*', 'warring', 'fight*',
                'violen*', 'hurt*', 'kill', 'kills', 'killer*', 'killed',
                'killing', 'endanger*', 'cruel*', 'brutal*', 'abuse*', 'damag*',
                'ruin*', 'ravage', 'detriment*', 'crush*', 'attack*',
                'annihilate*', 'destroy', 'stomp', 'abandon*', 'spurn',
                'impair', 'exploit', 'exploits', 'exploited', 'exploiting',
                'wound*'], 2]

fairnessVirtue = [['fair', 'fairly', 'fairness', 'fair-*', 'fairmind*',
                    'fairplay', 'equal*', 'justice', 'justness', 'justifi*',
                    'reciproc*', 'impartial*', 'egalitar*', 'rights', 'equity',
                    'evenness', 'equivalent', 'unbias*', 'tolerant', 'equable',
                    'balance*', 'homologous', 'unprejudice*', 'reasonable',
                    'constant', 'honest*'], 3]

fairnessVice = [['unfair*', 'unequal*', 'bias*', 'unjust*', 'injust*',
                    'bigot*', 'discriminat*', 'disproportion*', 'inequitable',
                    'prejud*', 'dishonest', 'unscrupulous', 'dissociate',
                    'preference', 'favoritism', 'segregat*', 'exclusion',
                    'exclud*'], 4]

ingroupVirtue = [['together', 'nation*', 'homeland*', 'family', 'families',
                    'familial', 'group', 'loyal*', 'patriot*', 'communal',
                    'commune*', 'communit*', 'communis*', 'comrad*', 'cadre',
                    'collectiv*', 'joint', 'unison', 'unite*', 'fellow*',
                    'guild', 'solidarity', 'devot*', 'member', 'cliqu*',
                    'cohort', 'ally', 'insider', 'segregat*'], 5]

ingroupVice = [['foreign*', 'enem*', 'betray*', 'treason*', 'traitor*',
                    'treacher*', 'disloyal*', 'individual*', 'apostasy',
                    'apostate', 'deserted', 'deserter*', 'deserting', 'deceiv*',
                    'jilt*', 'imposter', 'miscreant', 'spy', 'sequester',
                    'renegade',	'terroris*', 'immigra*', 'abandon*'], 6]

authorityVirtue = [['obey*', 'obedien*', 'duty', 'law', 'lawful*', 'legal*',
                    'duti*', 'honor*', 'respect', 'respectful*', 'respected',
                    'respects', 'order*', 'father*', 'mother', 'motherl*',
                    'mothering', 'mothers',	'tradition*', 'hierarch*',
                    'authorit*', 'permit', 'permission', 'status*', 'rank*',
                    'leader*', 'class', 'bourgeoisie', 'caste*', 'position',
                    'complian*', 'command', 'supremacy', 'control', 'submi*',
                    'allegian*', 'serve', 'abide', 'defere*', 'defer',
                    'revere*', 'venerat*', 'comply', 'preserve', 'loyal*'], 7]

authorityVice = [['defian*', 'rebel*', 'dissent*', 'subver*', 'disrespect*',
                    'disobe*', 'sediti*', 'agitat*', 'insubordinat*',
                    'illegal*', 'lawless*', 'insurgent', 'mutinous', 'defy*',
                    'dissident', 'unfaithful', 'alienate', 'defector',
                    'heretic*', 'nonconformist', 'oppose', 'protest', 'refuse',
                    'denounce', 'remonstrate', 'riot*', 'obstruct', 'betray*',
                    'treason*', 'traitor*', 'treacher*', 'disloyal*',
                    'apostasy', 'apostate', 'deserted', 'deserter*',
                    'deserting'], 8]

purityVirtue = [['piety', 'pious', 'purity', 'pure*', 'clean*', 'steril*',
                    'sacred*', 'chast*', 'holy', 'holiness', 'saint*',
                    'wholesome*', 'celiba*', 'abstention', 'virgin', 'virgins',
                    'virginity', 'virginal', 'austerity', 'integrity',
                    'modesty', 'abstinen*', 'abstemiousness', 'upright',
                    'limpid', 'unadulterated', 'maiden', 'virtuous', 'refined',
                    'decen*', 'immaculate', 'innocent',	'pristine', 'church*',
                    'preserve'], 9]

purityVice = [['disgust*', 'deprav*', 'disease*', 'unclean*', 'contagio*',
                'indecen*', 'sin', 'sinful*', 'sinner*', 'sins', 'sinned',
                'sinning', 'slut*', 'whore', 'dirt*', 'impiety', 'impious',
                'profan*', 'gross', 'repuls*', 'sick*', 'promiscu*', 'lewd*',
                'adulter*', 'debauche*', 'defile*', 'tramp', 'prostitut*',
                'unchaste', 'intemperate', 'wanton', 'profligate', 'filth*',
                'trashy', 'obscen*', 'lax', 'taint*', 'stain*', 'tarnish*',
                'debase*', 'desecrat*',	'wicked*', 'blemish', 'exploitat*',
                'pervert', 'wretched*', 'ruin*', 'exploit', 'exploits',
                'exploited', 'exploiting', 'apostasy', 'apostate', 'heretic*'],
                10]

moralityGeneral = [['righteous*', 'moral*', 'ethic*', 'value*', 'upstanding',
                        'good', 'goodness', 'principle*', 'blameless',
                        'exemplary', 'lesson', 'canon', 'doctrine', 'noble',
                        'worth*', 'ideal*', 'praiseworthy', 'commendable',
                        'character', 'proper', 'laudable', 'correct', 'wrong*',
                        'evil', 'immoral*', 'bad', 'offend*', 'offensive*',
                        'transgress*', 'honest*', 'lawful*', 'legal*', 'piety',
                        'pious', 'wholesome*', 'integrity', 'upright',
                        'decen*', 'indecen*', 'wicked*', 'wretched*'], 11]

morals = [harmVirtue, harmVice, fairnessVirtue, fairnessVice, ingroupVirtue,
            ingroupVice, authorityVirtue, authorityVice, purityVirtue,
            purityVice, moralityGeneral]

moralWordsDict = defaultdict(list)
for moral in morals:
    value = moral[1]
    words = moral[0]
    for word in words:
        if "*" in word:
            word = word[:-1]
        moralWordsDict[word].append(value)
