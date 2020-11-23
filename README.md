# ThamizhiMorph: Tamil Morphological Analyser and Generator

ThamizhiMorph is an open source Tamil morphological analyser cum generator, which handles primarily the inflectional morphology of Tamil verbs, nouns, and other types. This has been developed using a Finite-State Transducer (fomafst.github.io). 
A neural based tokeniser, and POS tagger have also been integrated to this tool so that given text can be analysed contectually to provide morphological analyses.

Nominal and verbal paradigms are used to implement this analyser cum generator. 

### Noun morphology



### Verb morphology



### Morphology of other particles

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
