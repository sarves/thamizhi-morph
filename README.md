# ThamizhiMorph: Tamil Morphological Analyser and Generator

ThamizhiMorph is an open source Tamil morphological analyser cum generator, which handles primarily the inflectional morphology of Tamil verbs, nouns, and other types. This has been developed using a Finite-State Transducer (fomafst.github.io). 
A neural based tokeniser, and POS tagger have also been integrated to this tool so that given text can be analysed contectually to provide morphological analyses.

Nominal and verbal paradigms are used to implement this analyser cum generator. 

### Noun morphology

A lexicon of 80K nouns have been compiled from various sources, including books and the Internet. Out nominal pradigm has in total of 38 classes for nouns, 16 for regular nouns and rest are for pronouns that are irrular in Tamil.

In morphological analysis we have handled 220 conjugations, including the conjugations of post-positional particles, for each noun class.

In addition we have also implemented a python script to classify nouns according to our paradigm. This script can befound here: XXXX

### Verb morphology

We used a paradigm of 18 classes to handle verbal morphology, which is derived from the famous Graul's classification for Tamil verbs. However, we have done some customisation to the paradigm to make the computational easy. 

We have handled 140 conjugational forms for each verbs. In addition to simple verbal roots, we have also included complex verbal roots which are formed by noun-verb and verb-verb formation.

In order to implement this in foma, we also have come up with a meta-morph rules (Meta-Morphological rules) to write inflections. Meta-morph is a markup language using which the inflectional morphology of morphologically regular languages can be captured. However, this needs bit more generalisations to capture other languages; this is on our future work. This is captured in the following paper:

Sarveswaran, K., Dias, G. and Butt, M., 2019. Using Meta-Morph Rules to develop Morphological Analysers: A case study concerning Tamil. In Proceedings of the 14th International Conference on Finite-State Methods and Natural Language Processing (pp. 76-86).

### Morphology of other particles

We have also handled adjectives, adverbs and other paricles. Conjuctions, intensifier, post-positional forms, numbers, complumentisers etc are included in a class called particles. Lexicons for these types were collection from the web, primarily.

### Generations of words

Using ThamizhiMorph, surface forms or actucal words can be generated. This list would be very usefule for applications like spell checkers, machine translators, or any applications where you need data augmentation. Using the current version we can generate more than 15M verbs and 10M nouns, for instance. Some sample list of generated words can be found here: XXXXXX

### Why ThamizhiMorph
- The only morphological analyser which is currently maintained, and developed activily
- Open source, and available under Apache-2 licence
- Has good coverage or words, and more words can be added eality to the analyser
- Analyser is developed as a finate-state model, which is very efficient, and can be integrated to any other tools easily or can be accessed through any other programming languages
- The only analyser which handles sandhi in its anlyses, sandhi gives important clues for morphological/syntactical processes
- ThamizhiMorph is a transducer, there generations can also be done. 

### How ThamizhiMorph works
There are two ways in which we can use ThamizhiMorph:
- Web portal: http://nlp-tools.uom.lk/thamizhi-morph/
Using this portal, given text cn be analysed word by word, without considering any contextual information. Currently, there are no POS integrated to the version avilable here.

- Terminal version / standalone version: This is a python version of the tagger, available for the download in this repo. This is a python programme which integrates a tokeniser, POS tagger and ThamizhiMorph. This analyse the data given in a text file called sentences.txt in the given folder, and provide two documents. One of which consists the contextual analyses by considering POS tagger informtion and morphological information. The other file captures the analyses where POS and ThamizhiMorph deviate. Since POS tagger is also does not have the 100% accuracy, we did not through anything data analysed by ThamizhiMorph.



### How to set ThamizhiMorph up

You can use the website version without needing of any special requirements. All the data to this tool has to be fed in Unicode format. The other version 

# Challenges
Tamil is morphologically rich, and has evolved over several thousand years. This makes the task a challeging in terms of coverage and understanding. Further, even with a POS tagger which captures the context, disambiguation was not possible, and there are syntactical clues are required at sometimes. As an analyser, this tool provide all the analyses when it cannot be disambigurated. 

Noun


- FST models (https://github.com/sarves/thamizhi-morph/tree/master/FST-Models)
- Lexicons (https://github.com/sarves/thamizhi-morph/tree/master/Lexicons)
- Generated verbs (https://github.com/sarves/thamizhi-morph/tree/master/Generated-Verbs) 
> Readme files in the respective directories ellaborate more about content.

An online version of the tool can be find here: http://nlp-tools.uom.lk/thamizhi-morph/parse-sentence.php
>I am revamping this tool, therefore, there may be outages time to time. 
Please use the Github version for further development. 
