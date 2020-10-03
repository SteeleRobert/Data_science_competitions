
import numpy as np
from gensim.models import KeyedVectors
from moralWordsDict import moralWordsDict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

### DOWNLOAD STOP WORDS - NLTK - FOR LOOP

### ALSO, FUNCTION TAKES IN LIST OF WORDS (EX: ["I", "LOVE", "CITADEL"])
### MAYBE IT SHOULD BE MORE FLEXIBLE (I.E. TAKE IN DATAFRAME (BAG OF WORDS))


moralWords = list(moralWordsDict.keys())
stop_words = set(stopwords.words('english'))

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

def getBagOWords(text):
    toks = word_tokenize(text)
    return [w for w in toks if not w in stop_words]


def getBagMapping(bagOfWords):
    bagMapping = initializeMapping()
    for word in bagOfWords:
        bagMapping += getWordMapping(word)
    bagMapping /= np.sum(np.abs(bagMapping))
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
        wordVectors = model.wv
        if word in wordVectors:
            distancesToWord = {}
            for moralWord in moralWords:
                if moralWord not in wordVectors:
                    moralWord = approxWordDict[moralWord]
                distancesToWord[moralWord] = model.similarity(moralWord, word)
            closestWordVector = max(distancesToWord, key=distancesToWord.get)
            distToClosestWV = distancesToWord[closestWordVector]
            if distToClosestWV > 0.9:
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

text = '''A boy called Andy Davis (voice: John Morris) uses his toys to act out a bank robbery. The bank is a cardboard box, the robber is Mr. Potato Head (voice: Don Rickles) assisted by Slinky Dog (voice: Jim Varney), and the bystanders include Bo Peep (voice: Annie Potts) and her sheep. The day is saved by cowboy doll Woody (voice: Tom Hanks) playing the sheriff, with help from Rex the dinosaur (voice: Wallace Shawn). Woody is the only toy who gets to say his own lines because he has a pull-string that makes him say things like "Reach for the sky!" and "You're my favorite deputy!"

During the opening credits (soundtrack: Randy Newman's "You've Got a Friend in Me"), Andy takes Woody downstairs to find his mother (voice: Laurie Metcalf) decorating the dining room for his birthday party. He asks if they can leave the decorations up until they move, and his mom agrees. She says the guests will arrive soon and sends him back upstairs to get his baby sister Molly (voice: Hannah Unkrich), whose crib is in his room. Andy tosses Woody onto his bed before he pulls Molly out of her crib and carries her away.

Woody and the other toys have seemed limp and inanimate up to this point, but as soon as Andy leaves the room, Woody sits up and expresses surprise that the birthday party is today. He calls "Ok, everybody, the coast is clear," and the other toys come to life too. Woody calls a staff meeting and tells Slinky Dog to spread the word. Within a few minutes (during which Bo Peep makes a date with Woody for that evening), all the toys are assembled. Woody starts by reminding them all to find a moving buddy so they don't get lost when the Davis family moves to their new house, which will happen in a week. Then he tries to downplay the news that Andy's birthday party is happening today, but it causes a commotion as the toys know that Andy's actual birthday isn't till next week. Rex worries that someone will give Andy another dinosaur, and many of the toys have similar concerns. Woody points out that it makes sense to have the party before the move, then tries to calm them down. He's interrupted when Hamm (voice: John Ratzenberger) the piggybank, stationed near the window, announces that the guests are arriving. The toys rush to the window to see the presents the kids are bringing; the bigger boxes make them especially nervous. Hamm predicts "we're next month's garage sale fodder for sure." Woody finally says, "If I send out the troops, will you all calm down?"

Sending out the troops means that the little green plastic soldiers, led by Sarge (voice: R. Lee Ermey), lower the baby monitor to the first floor and hide with it in a potted plant, where they can observe the opening of the gifts and report back to the toys in Andy's room. At first, the presents seem nonthreatening &mdash; a lunchbox, bed sheets ("who invited that kid?" wonders Mr. Potato Head), a Battleship game. But Andy's mom pulls a surprise present from the closet. Andy's very excited about it, but before they hear what it is, Rex knocks the speaker off the table and the batteries fall out. Sarge warns that the kids are headed upstairs, but the toys barely have time to resume their previous positions before the stampede thunders in. One of the kids (Andy?) sweeps Woody off the bed, saying "make a space, this is where the spaceship lands!" They put something down where Woody was, then Andy's mom calls them back down to play games and suddenly the room is empty again. The toys creep out of their hiding places to see the new toy, pausing in surprise when Woody crawls out from under the bed. The new toy has taken Woody's place on the bed, which causes consternation. Woody reminds them that no one is being replaced, and they look up to see what's on the bed.

It's Buzz Lightyear (voice: Tim Allen), space ranger, Universe Protection unit. Buzz believes he's crash landed on a strange planet on the way to sector 12, and his ship (his box) is damaged. Woody welcomes Buzz to Andy's room and tries to explain that Buzz has landed in Woody's usual spot. The other toys climb up on the bed to meet Buzz and ask him about the buttons and gadgets on his space suit. They're impressed with Buzz's voice recordings &mdash; "a quality sound system" &mdash; not like Woody's pull-string-activated voice, which "sounds like a car ran over it." Buzz also has a laser ("a little light bulb that blinks," grumbles Woody), and wings. Buzz takes exception to being called a toy, and when Woody says he can't really fly, Buzz climbs the bedpost, shouts "to infinity and beyond!", and dives. He bounces off a rubber ball, does a loop-de-loop on the racetrack, and gets stuck for a few rotations on the toy plane tethered to the ceiling before flipping down and landing neatly back on the bed. All the toys are dazzled except Woody, who says "that wasn't flying, that was falling with style!"

In the montage that follows (soundtrack: Randy Newman's "Strange Things Are Happening to Me"), Andy has Buzz shoot Woody, then puts on a cardboard replica of Buzz's helmet and wings. A western-themed poster in Andy's room is replaced by two Buzz Lightyear posters, and drawings of Woody on the bulletin board are covered with drawings of Buzz. The western-style bedspread disappears; the new one is emblazoned with Buzz's image and his name. In the final indignity, Andy takes Buzz to bed and leaves Woody in the covered wagon toy chest.

Some alarming noises draw the toys to the open window, where they can see the neighbor kid, Sid (voice: Erik von Detten), who's about to blow up a Combat Carl action figure. Sid's dog Scud, a brown and white bull terrier, is tied up nearby and barking like crazy. Buzz thinks Sid, who's laughing maniacally, is "a happy child;" the others explain that he tortures toys. Buzz wants to help the doomed toy soldier, but Sid lights the fuse and Andy's toys duck as debris goes flying. When they look again, there's no sign of Carl. "The sooner we move, the better," says Bo Peep.

Andy's mom suggests dinner at Pizza Planet (a space-themed restaurant) and tells Andy he can bring one toy. Doubting that Andy will choose him unless Buzz is unavailable, Woody plans to trap Buzz in a gap behind Andy's desk. The plan backfires and Buzz falls out the window into the bushes below. The other toys accuse Woody of pushing Buzz out the window out of jealousy, but as they are about to punish him, Andy returns. Failing to find Buzz, he grabs Woody and the family drives off &mdash; but not before Buzz crawls out of his bush and climbs on the back of the minivan.

While Andy's mother refuels the car at a Dinoco station, Woody wonders how he can convince the other toys that Buzz's fall was an accident. Suddenly Buzz appears. Woody is delighted, though more for his own sake than Buzz's ("I'm saved!"), but Buzz is very bitter over what Woody did to him. The two fight and roll out of the car, which drives off and leaves them stranded. Luckily, Woody sees another vehicle heading for Pizza Planet and knows that they can meet Andy there. He tricks Buzz into coming with him (but only because if he came home without Buzz, the other toys would attack him). Buzz insists on riding in the "cockpit" (the front seat) so he can wear a seatbelt; Woody climbs in the back and gets thrown about by the driver's erratic maneuvers. They reach Pizza Planet and hide in discarded food packaging so they can sneak through the front door. Woody quickly spots the Davises, but Buzz climbs into a claw-crane machine shaped like a spaceship, thinking it's the ship home Woody promised him. The machine is filled with three-eyed green aliens (voices: Debi Derryberry, Jeff Pidgeon) who believe the claw is a god. Woody climbs in to get Buzz out, but Woody and Buzz are captured by Sid, along with one of the little aliens.

Sid takes them back to his house and immediately gives the three-eyed alien to Scud, who starts chewing on it. Then Sid takes a doll away from his little sister Hannah (voice: Sarah Freeman) and runs upstairs to operate on her. ("No one's ever attempted a double-bypass brain transplant before!") Woody and Buzz, still in Sid's backpack, look on in horror as Sid replaces the doll's head with the head of a toy pterodactyl and gleefully gives it back to Hannah, who shrieks for her mother and runs away. Sid follows.

Woody tries to get out of Sid's room, but the door's locked. He's frightened by Sid's nightmarish mutant toys, which Sid has butchered and reconstructed a la Frankenstein. There's an erector-set spider with a one-eyed baby head, a jack-in-the-box whose jack has been replaced by a green rubber hand, a fishing pole with legs, and other horrors. Buzz thinks they're cannibals. Meanwhile, Andy's toys are searching for Buzz from Andy's window. They have to stop when the car pulls into the driveway. Andy can't find Woody and many of the toys think he ran away, which they interpret as evidence of his guilt. But Bo Peep hopes he's ok.

Next morning, Sid interrogates Woody about the location of a "rebel base." When Woody remains silent, Sid uses a magnifying glass to concentrate the sunlight on a spot between Woody's eyebrows, which starts to smoke. Woody is saved when Sid is called away to eat his Pop-tarts. Buzz compliments Woody for not succumbing to Sid's torture. Woody notices that Sid has left the door open, but before he and Buzz get out, the mutant toys block the way. Buzz tries his laser on them and is puzzled when it doesn't work. Woody pushes the button that activates Buzz's karate-chop action and frog-marches him through the crowd of toys, which parts to let them through. Woody drops Buzz as soon as they reach the door and runs down the stairs saying "there's no place like home, there's no place like home," a la Dorothy in The Wizard of Oz (1939).

On the landing, he finds Scud, scary even in his sleep. He backs up, then Buzz grabs him and leads him down the hall past the head of the stairs. But the ring on Woody's pull-string catches on the wrought-iron stair railing, and he says (involuntarily) "Yee-haw! Giddyap, partner &mdash; we got to get this wagon train a-movin!" Of course the dog wakes up and comes to investigate. Buzz says "Split up!" and runs through an open door; Woody pulls another door closed behind him. Buzz sees someone asleep in a recliner and notices that the television is on. A voice is saying "Come in, Buzz Lightyear! This is Star Command!" At first Buzz thinks Star Command is really trying to reach him, and fiddles with the radio on his suit. But as the commercial enumerates his features and adds a disclaimer that Buzz is not a flying toy, Buzz begins to believe that he really is, as Woody keeps telling him, only a child's plaything. He's despondent. Then he spots an open window in the stairwell (apparently nobody in this neighborhood bothers with window screens) and tries to prove himself wrong by flying through it. He bounces off the stairs and lands in the hall, losing an arm in the process (soundtrack: Randy Newman's "I Will Go Sailing No More").

Hannah picks Buzz up and carries him off to her room, where Woody finds him playing the part of Mrs. Nesbitt at a tea party. ("What a lovely hat, Mrs. Nesbitt. It goes quite well with your head.") Woody imitates Hannah's mother's voice to lure Hannah out of the room so he can rescue Buzz. Buzz is raving and depressed, but when he wails that he can't even fly out the window, it gives Woody an idea. He opens the window in Sid's room and calls over to Andy's room, where Hamm is beating Mr. Potato Head at Battleship. Most of the toys seem glad to see him. He tosses a string of Christmas lights across and tells them to tie it to something, but Mr. Potato Head says "How 'bout we don't?" and tries to convince the other toys that they should leave Woody where he is. Woody tells them Buzz is with him, but Buzz won't come to the window where the toys in Andy's room can see him, though he does throw Woody his detached arm. Woody uses the arm to make the toys think Buzz is standing next to him, but eventually slips up and they see that the arm isn't attached to Buzz. They react pretty much the way people would react to a severed human arm, with horror and disgust. They let go of the string of lights, which falls to the ground. When Woody begs them to listen, they leave the window, except for Slink, who closes the blinds. Woody cries.

Down on the floor, Sid's mutant toys have surrounded Buzz. When Woody tries to drive them off, the baby-headed spider comes at him and takes away Buzz's arm. Woody can't break through the group around Buzz, but he's sure they're killing him until the crowd of toys breaks up and reveals Buzz with his arm re-attached. "But they're cannibals," Woody says; "we saw them eat those other toys" ... then he looks at Sid's toys again, and notices that Hannah's doll and the pterodactyl have their own heads back. Realizing hes misjudged them, he's trying to apologize when they all disappear under the bed and Sid comes back.

Sid has a rocket. His first thought is to use it on Woody, but Woody's hiding, so he picks up Buzz instead. "I've always wanted to put a space man into orbit," he says malevolently. A rainstorm forces him to delay the rocket launch until morning.

Next door, it's Andy's bedtime and he's mourning the loss of his two favorite toys. His mom comes in and says she's looked everywhere, and all she can find is his hat, which she gives him. (This is the white-laced red cowboy hat that looks like the had worn by Jessie, a character we meet in the next movie.) Andy's mom reassures him that they'll find Woody and Buzz before they move out &mdash; tomorrow.

That night, Woody convinces Buzz that even if he's not a space ranger, life as Andy's toy is still worth living, though Woody himself despairs that he'll ever be Andy's favorite toy again. Buzz regains his spirit in time to see the moving truck pull up to Andy's house. But before they can escape, Sid wakes up and takes Buzz (still strapped to the rocket) out into the back yard. He starts working on something ominous with a big empty water jug while doing newscaster-style narration of the preparations for the approaching rocket launch.

Woody pleads with the mutant toys to help him rescue Buzz and they hesitantly join him. (None of Sid's toys talk.) Woody outlines a plan and assigns tasks to each toy. Ducky and Legs go into the heating ducts to avoid Scud, who saw Woody trying to follow Sid and is still growling outside the bedroom door. Ducky and Legs get outside by removing the light fixture on the front porch, then ring the doorbell. When he hears the doorbell, Woody releases a wind-up frog from Sid's room; the frog scoots under Scud and zooms down the hall. Scud gives chase and follows the frog downstairs, where Hannah's answering the door. The frog goes out, Ducky grabs it, and they're both reeled up by Legs (who's part fishing pole) before Scud catches up. Hannah, exasperated, shuts the door, leaving Scud outside. The porch light fixture drops back into place before anyone notices it's gone.

As soon as Hannah's out of the front hall, Woody and his cadre of toys come down the stairs, roll through the kitchen, and exit through the cat flap in the back door. They land in the bushes, where they have a good view of the launch site. Sid's newscaster voice is asking his mission control voice if launch pad construction is complete; mission control says it is. Sid himself is out of sight, apparently rummaging around in the shed looking for matches. Ducky, Legs, and the wind-up frog pop out of a down-spout as Sid prepares to start the count-down.

The launch pad looks very strange. Buzz and his rocket are standing on a dart board on a milk crate. Nearby is an orange-striped traffic horse with a rake leaning on it and the empty water jug propped underneath. The jug is connected with vacuum-cleaner hose to a red funnel, which is aimed at Buzz's feet.

Woody approaches Buzz, who's happy to see him and asks for help getting loose. Woody says "Everything's under control," and falls to the ground in the manner of a toy expecting a human on the scene. Sure enough, Sid comes out of the shed using his mission control voice ("all systems are go, requesting permission to launch") &mdash; and then notices Woody. He tosses Woody on the charcoal grill and says "You and I can have a cookout later." He puts a match in Woody's holster and turns back to his rocket launch, where he lights another match and starts counting down from 10. While he's focused on this, toys are taking up positions all around the yard.

Before Sid can light Buzz's fuse, Woody's voice recordings start playing, one after another: "Reach for the sky! This town ain't big enough for the two of us! Somebody's poisoned the waterhole!" Sid is distracted and comes over to pick Woody up off the grill. His string hasn't been pulled.

"It's busted!" he says disgustedly.

"Who are you callin' busted, buster?" says Woody. "That's right, I'm talking to you, Sid Phillips. We don't like being blown up, Sid." Sid begins to look terrified. "... or smashed, or ripped apart," continues Woody.

"W-we?" Sid stutters.

"That's right!" replies Woody. "Your toys!" A rag doll climbs out of the sandbox and walks across the yard saying "ma-ma ... ma-ma." A large toy pickup truck emerges from a pile of sand while a couple of partially dismembered soldier action figures rise out of a puddle. They all advance on Sid, who backs away and jumps when the three-eyed alien from Pizza Planet pops out from under Scud's red water bowl. Sid backs toward the clothes line and the baby-headed spider drops down on his head. He shrieks and shakes it off, but the toys have him surrounded now. Woody says, "You must take good care of your toys, because if you don't, we'll find out, Sid. We toys can see everything!" Woody's head spins all the way around (think The Exorcist (1973)). "So play nice."

Sid is panic-stricken. He screams, throws Woody in the air, and runs into the house, where he tells Hannah the toys are alive. When he sees the doll she's carrying, he says "nice toy," and backs away. She waves the doll at him. He screams again and runs upstairs crying; she chases him.

Outside, Woody and other toys are celebrating. "We did it!" As Buzz thanks Woody, they hear a honk from next door. Andy's mom tells the kids to say goodbye to their old house and the minivan starts to move. Woody and Buzz rush over and Woody climbs on the back of the car, but Buzz, still burdened with the rocket, can't get through the fence. He tells Woody he'll catch up, but Woody comes back for him. They manage to get on the back of the moving van, but Scud runs after them and gets hold of Woody's leg. Woody can't hold on to the truck and tells Buzz to take care of Andy for him. Buzz, sacrificing himself to save Woody, jumps on Scud's head, making him let go of Woody. Woody climbs back on the truck and pries open the cargo door as the truck comes to a stoplight. Woody pulls out RC, the remote controlled car, and sends him to get Buzz, who's under a parked car where Scud can't reach him.

The toys in the van think Woody is murdering another toy and try to stop him. This is a problem because Woody's controlling RC. The angry toys pick up Woody and Rocky, the strong-man, spins him around, which causes RC to drive in circles around Scud (who's still barking furiously). They throw Woody against a box; RC's path straightens out. Hamm jumps on Woody. RC, with Buzz still precariously aboard, approaches a busy intersection. The traffic light is not in their favor. RC scoots under a moving car, but two other cars collide while trying to avoid Scud. The wrecked cars cut the dog off from his quarry and RC pulls away.

On the truck, Woody tries to tell the toys that Buzz is out there and they have to save him, but Mr. Potato Head isn't buying it. "Toss him overboard," he says, and they do &mdash; but Woody holds on to RC's controller. RC sweeps Woody off his feet and Woody turns RC up to turbo so they can catch up to the moving truck.

Lenny (voice: Joe Ranft), the binoculars, notices RC and his passengers gaining on them and alerts the other toys. Bo Peep confirms that Buzz is there &mdash; "Woody was telling the truth!"

"What have we done?" wail the toys. Bo Peep tells Rocky to lower the truck's cargo ramp. Slink stretches out and Woody is able to grab his paw just as RC's batteries begin to lose strength.

In the Davises' car, they're listening to "Hakuna Matata." Molly can see RC in the side mirror and laughs, but she can't talk, so no one else notices. RC is swerving dangerously. Slink, stretched past his limit, loses his grip and RC coughs to a stop in the middle of the road as the moving van disappears in the distance. Then Buzz remembers he still has a rocket strapped to his back, and Woody remembers he still has the match Sid put in his holster. He strikes it and is about to light Buzz's fuse when the wind of a passing car puts out the match. Despair. But when Woody's hand starts to smoke, he realizes that Buzz's helmet concentrates the sunlight just as Sid's magnifying glass did. They use it to light the fuse. The rocket catches them up to the truck and lifts them off the ground. As they go by Woody drops RC, who lands in the truck. Buzz and Woody go straight up with the rocket. Buzz opens his wings, which apparently break the tape holding him to the rocket, and zooms downward. He's still clutching Woody, who says "Buzz, you're flying!"

"This isn't flying, this is falling with style!" retorts Buzz, repeating Woody's earlier line. They pass the truck again and fall through the minivan's sunroof, landing neatly in the box next to Andy, who finds them and gleefully tells his mom. She assumes they've been in the car the whole time.

On Christmas Eve at the new house, Andy, Molly, and their mom are gathered around the Christmas tree. The army men are hiding in the tree with the baby monitor; the other toys are in Andy's room gathered around the speaker. Bo Peep pulls Woody under some mistletoe (held by her sheep) and kisses him. Andy's bed still sports a Buzz Lightyear bedspread, but one of the pillowcases and the comforter at the foot of the bed are western style. Drawings of Woody are again prominent on the bulletin board. There are two Buzz Lightyear posters, but also a cowboy poster. Balance and harmony reign.

All the toys seem happy and relaxed; instead of fretting that Andy might get another dinosaur, Rex hopes for a leaf-eater so he can play the dominant predator.

The first report comes in from Sarge: Molly's first present is a Mrs. Potato Head, to Mr. Potato Head's delight. He says he'd better shave and yanks off his mustache.

Woody, a bit lipstick-stained and woozy, joins Buzz on Andy's bed. They're still friends. Sarge announces that Andy's opening his first present, but there's a burst of static and Buzz whacks the speaker a few times. Woody asks Buzz if he's worried and Buzz denies it, then says, "Are you?"

"Now Buzz," Woody teases, "what could Andy possibly get that is worse than you?."

Then they hear a bark downstairs, and Andy's joyous cry of "wow, a puppy!" Woody and Buzz exchange nervous smiles. The credits roll to the reprise of "You've Got a Friend in Me," a duet featuring Randy Newman and Lyle Lovett.'''

print(getBagMapping(getBagOWords(re.sub(r'[^a-zA-Z0-9_. ]', '', text))))
