# ThamizhiMorph: Tamil Morphological Analyser
## Use it here: http://nlp-tools.uom.lk/thamizhi-morph/ 
Note, I am revamping the site, therefore, there may be outages time to time. Please bear with me. - November, 2020.


ThamizhiMorph is an open source Tamil morphological analyser cum generator, which handles primarily the inflectional morphology of Tamil verbs, nouns, and other types. This has been developed using a Finite-State Transducer (fomafst.github.io). 
A neural based tokeniser, and POS tagger have also been integrated to this tool so that given text can be analysed contextually to provide morphological analyses.

Nominal and verbal paradigms are used to implement this analyser cum generator. 

### Noun morphology

A lexicon of 80K nouns have been compiled from various sources, including books and the Internet. Out nominal paradigm has in total of 38 classes for nouns, 16 for regular nouns and rest are for pronouns that are irregular in Tamil.

In morphological analysis we have handled 220 conjugations, including the conjugations of post-positional particles, for each noun class.

In addition we have also implemented a python script to classify nouns according to our paradigm. This script can be found here: https://github.com/sarves/Tamil-Noun-Classifier

### Verb morphology

We used a paradigm of 18 classes to handle verbal morphology, which is derived from the famous Graul's classification for Tamil verbs. However, we have done some customisation to the paradigm to make the computational easy. 

We have handled 140 conjugational forms for each verbs. In addition to simple verbal roots, we have also included complex verbal roots which are formed by noun-verb and verb-verb formation.

In order to implement this in foma, we also have come up with a meta-morph rules (Meta-Morphological rules) to write inflections. Meta-morph is a markup language using which the inflectional morphology of morphologically regular languages can be captured. However, this needs bit more generalizations to capture other languages; this is on our future work. This is captured in the following paper:

Sarveswaran, K., Dias, G. and Butt, M., 2019. Using Meta-Morph Rules to develop Morphological Analysers: A case study concerning Tamil. In Proceedings of the 14th International Conference on Finite-State Methods and Natural Language Processing (pp. 76-86).

### Morphology of other particles

We have also handled adjectives, adverbs and other particles. Conjunctions, intensifier, post-positional forms, numbers, complimentisers etc are included in a class called particles. Lexicons for these types were collection from the web, primarily.

### Generations of words

Using ThamizhiMorph, surface forms or actucal words can be generated. This list would be very usefule for applications like spell checkers, machine translators, or any applications where you need data augmentation. Using the current version we can generate more than 15M verbs and 10M nouns, for instance. Some sample list of generated words can be found here: https://github.com/sarves/thamizhi-morph/tree/master/Generated-Verbs

### Why ThamizhiMorph
- The only morphological analyser which is currently maintained, and developed activily
- Open source, and available under Apache-2 licence
- Has good coverage or words, and more words can be added eality to the analyser
- Analyser is developed as a finate-state model, which is very efficient, and can be integrated to any other tools easily or can be accessed through any other programming languages
- The only analyser which handles Sandhi in its anlyses, Sandhi gives important clues for morphological/syntactical processes
- ThamizhiMorph is a transducer, there generations can also be done. 

### ThamizhiMorph - what are given

All the data used to develop ThamizhiMorph are given, including lexicons, finite-state models, meta-morph rules, scripts for noun classifications and data cleaning.
- FST models (https://github.com/sarves/thamizhi-morph/tree/master/FST-Models)
- Lexicons (https://github.com/sarves/thamizhi-morph/tree/master/Lexicons)
- Generated verbs (https://github.com/sarves/thamizhi-morph/tree/master/Generated-Verbs) 
> Readme files in the respective directories ellaborate more about the content.

### How ThamizhiMorph works

There are two ways in which we can use ThamizhiMorph:
- Web portal: http://nlp-tools.uom.lk/thamizhi-morph/
Using this portal, given text cn be analysed word by word, without considering any contextual information. Currently, there are no POS integrated to the version avilable here.

- Terminal version / standalone version: This is a python version of the tagger, available for the download in this repo here: *thamizhi-morph-parse-2.py*. This is a python program which integrates a tokeniser, ThamizhiPOSt (a POS tagger) to ThamizhiMorph. This analyse the data given in a text file called sentences.txt in the given folder, and provide two documents. One of them consists the contextual analyses by considering POS tagger informtion and morphological information. The other file captures the analyses where POS and ThamizhiMorph deviate. Since POS tagger is also does not have the 100% accuracy, we could not completely relay on it and ignore what is provided by ThamizhiMorph. You can read more about the ThamizhiPOSt here: https://github.com/sarves/thamizhi-pos

### How to set ThamizhiMorph up

You can use the website version without needing of any special requirements. All the data to this tool has to be fed in Unicode format. 

In order to run the terminal version you need to install the following tools as the pre-requisite:
- foma - https://fomafst.github.io/
- stanza - https://stanfordnlp.github.io/stanza/

After setting up these two libraries, you can do the following command to get the analysis in your terminal:
```
echo <word> | flookup <fst-file>
```
For instance, if you want to analyse a noun - say தமிழ் , you can do the following:
```
echo தமிழ் | flookup tamil-nouns.fst 
```
and this would give you the following output. Where, the 1st token gives the surface form which you passed, the second token has lemma, pos, and analysis, which are separated by ‘+’, respectively 
```
தமிழ்	தமிழ்+noun+nom
```

If you want to do the morphological parsing along with the POS tagger, you can used the python script *thamizhi-morph-parse-2.py*. Make sure you keep the POS model, Tokenizer model (these two models you can get it from https://github.com/sarves/thamizhi-pos) and Facebook's fastext model under a directory called models, and all the fsts files from https://github.com/sarves/thamizhi-morph/tree/master/FST-Models in a folder called fsts. Further, you also need to ensure that all the FST models have executable permission. Anyway the python script is self explonary. Feel free to reach out me if you have any issues.

### Challenges and future work

Tamil is morphologically rich, and has evolved over several thousand years. This makes the task a challenging in terms of coverage and understanding. Further, even with a POS tagger which captures the context, disambiguation was not possible, and there are syntactical clues are required at sometimes. As an analyser, this tool provide all the analyses when it cannot be disambiguated. 
We are in the process of develop a neural based morphological analyser based on the data we generated from ThamizhiMorph. Further, we are also exploring ways in which we can do more disambiguation, may be using syntactical clues if we can get them. 

### Cite please

- Sarveswaran, K., Dias, G. and Butt, M.,"ThamizhiMorph: A Morphological Parser for the Tamil Language", Special Issue on Machine Translation for Low-Resource Languages, Machine Translation, 2020 [accepted] - This gives very detail description of how we developed ThamizhiMorph, what were our design decisions etc.
- Sarveswaran, K., Dias, G. and Butt, M.: “Using Meta-Morph Rules to develop Morphological Analysers: A case study concerning Tamil”, 14th International Conference on Finite-State Methods and Natural Language Processing,Dresden, Germany, September 23–25, 2019.
- Sarveswaran, K., Dias, G. and Butt, M.: “ThamizhiFST: A Morphological Analyser and Generator for Tamil Verbs,” 3rd International Conference on Information Technology Research (ICITR), pp. 1-6, Moratuwa, Sri Lanka, 2018.

### Acknowledgment

This research was supported by the Accelerating Higher Education Expansion and Development (AHEAD) Operation of the Ministry of Higher Education, Sri Lanka funded by the World Bank, and also supported by the DAAD (German Academic Exchange Office)


### Developer / point of contact

K. Sarveswaran, 
Department of Computer Science and Engineering |
National Languages Processing Centre,
University of Moratuwa.
iamsarves@gmail.com
sarvesk@uom.lk

