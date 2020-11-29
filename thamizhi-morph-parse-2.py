import stanza
import sys
import subprocess
import os
import json

def isEnglish(text):
        try:
                text.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
                return 0
        else:
                return 1


def find_morphemes(word,fsts):

        analyses=[]
        for fst in fsts:
                p1 = subprocess.Popen(["echo", word], stdout=subprocess.PIPE)
                file_name="fsts/"+fst
                p2 = subprocess.Popen(["flookup", file_name], stdin=p1.stdout, stdout=subprocess.PIPE)
                p1.stdout.close()
                output,err = p2.communicate()
                #print(output.decode("utf-8"))

                #1st analysis is broken by new line to tackle cases with multiple analysis
                #then analysis with one output is handled
                #1st each line is broken by tab to find lemma and analysis
                #then those are store in a list and returned back to main

                lines=output.decode("utf-8").strip().split("\n")
                if len(lines) > 1:
                        for line in lines:
                                analysis=line.split("	")
                                if len(analysis) > 1:
                                        if "?" in output.decode("utf-8"):
                                                results=0
                                        else:
                                                #print(analysis[1].strip().split("+"))
                                                analyses.append(analysis[1].strip().split("+"))
                                else:
                                        return 0

                #this is to handle cases with one output, 1st each line is broken by tab to
                #find lemma and analysis
                #then those are store in a list and returned back to main
                analysis=output.decode("utf-8").split("	")
                if len(analysis) > 1:
                        if "?" in output.decode("utf-8"):
                                results=0
                        else:
                                #print(analysis[1].strip().split("+"))
                                analyses.append(analysis[1].strip().split("+"))
                else:
                        return 0
        if analyses :
                return analyses
        else:
                return 0

def guess_morphemes(word,fsts):
        analyses=[]
        for fst in fsts:
                p1 = subprocess.Popen(["echo", word], stdout=subprocess.PIPE)
                file_name="fsts/"+fst
                p2 = subprocess.Popen(["flookup", file_name], stdin=p1.stdout, stdout=subprocess.PIPE)
                p1.stdout.close()
                output,err = p2.communicate()
                #print(output.decode("utf-8"))

                #1st analysis is broken by new line to tackle cases with multiple analysis
                #then analysis with one output is handled
                #1st each line is broken by tab to find lemma and analysis
                #then those are store in a list and returned back to main

                lines=output.decode("utf-8").strip().split("\n")
                if len(lines) > 1:
                        for line in lines:
                                analysis=line.split("	")
                                if len(analysis) > 1:
                                        if "?" in output.decode("utf-8"):
                                                results=0
                                        else:
                                                #print(analysis[1].strip().split("+"))
                                                analyses.append(analysis[1].strip().split("+"))
                                else:
                                        return 0

                #this is to handle cases with one output, 1st each line is broken by tab to
                #find lemma and analysis
                #then those are store in a list and returned back to main
                analysis=output.decode("utf-8").split("	")
                if len(analysis) > 1:
                        if "?" in output.decode("utf-8"):
                                results=0
                        else:
                                #print(analysis[1].strip().split("+"))
                                analyses.append(analysis[1].strip().split("+"))
                else:
                        return 0
        if analyses :
                return analyses
        else:
                return 0


#here Stanza models are listed for pos tagging     
config = {
	'processors': 'tokenize,pos', # Comma-separated list of processors to use
	'lang': 'ta', # Language code for the language to build the Pipeline in
	'tokenize_model_path': './models/ta_ttb_tokenizer.pt', 
	'pos_model_path': './models/ta_amr_tagger.pt',
	'pos_pretrain_path': './models/ta_amr.pretrain.pt',
}
nlp = stanza.Pipeline(**config)

punct_dict = """{".":"period",",":"comma",";":"semi-colon",":":"colon","-":"hyphen","(":"open-bracket",")":"close-bracket"}"""
punct_json = json.loads(punct_dict)

#reading fsts, fsts in fst_list has to be placed in a priority order in which look up should happen
#this needs to be passed to the function using which morphemes are extracted
fsts=[]
f1=open("fsts/fst-list","r")
for line in f1:
        fsts.append(line.strip())
f1.close()

#reading guesser file names, these will be used when a word is not found in fsts
gussers=[]
f1=open("fsts/guesser-list","r")
for line in f1:
        gussers.append(line.strip())
f1.close()


#read data to be passed, and keep it in an array
data_input=[]
f1=open("sentence.txt","r")
for line in f1:
        data_input.append(line.strip())
f1.close()


#open up a file to write results
pos_tagged=open('pos-tagged-sentence.txt', 'w')
pos_morph_aligned=open('pos-morph_aligned.txt', 'w')
pos_morph_aligned.write("#This file was annotated using ThamizhiMorph morphological analyser, http://nlp-tools.uom.lk/thamizhi-morph/" +
                                        ", in CoNLL-U format. \n")      
for data_unit in data_input:
        doc = nlp(data_unit.replace("-", " - ").replace("("," ( ").replace(")"," ) "))                
        for sent in doc.sentences :
                #this is to print the sentence text 1st on both aligned and not aligned files
                pos_tagged.write(sent.text + "\n" + "\n")          
                pos_morph_aligned.write("\n" + sent.text + "\n")
                #initialing word count, this will be reset when start a new sentence
                word_id=1
                #iterate for each word of a sentence
                for word in sent.words :
                        #this is set to 0, and when an analysis is found, it will be set to 1
                        analysis_success=0
                        #print(word.text)
                        #All the Puncts are marked here with PUNCT. There are no analysis for PUNCT from ThamizhiMorph
                        #if word.upos == "PUNCT" :
                        #        pos_morph_aligned.write(str(word_id) + "\t" + word.text + "\t" + word.text + "\t" + word.upos+ "\t" + "_" + "\n")
                        if word.text in punct_json:
                                pos_morph_aligned.write(str(word_id) + "\t" + word.text + "\t" + "_" + "\t" + "PUNCT" + "\t" + punct_json[word.text] + "\n")                                
                        #All numeric will take default annotations given by the POS tagger
                        elif word.text.isnumeric() :
                                pos_morph_aligned.write(str(word_id) + "\t" + word.text + "\t" + word.text + "\t" + word.upos+ "\t" + "_" + "\n")
                        elif isEnglish(word.text) == 1 :
                                pos_morph_aligned.write(str(word_id) + "\t" + word.text + "\t" + "non-Tamil" + "\t" + "_" + "\t" + "_" + "\n")
                        else:      
                                #if a word is found in lexicons
                                analyses = find_morphemes(word.text.strip(),fsts)
                                analysis_success=analyses
                                if analyses != 0 :
                                        for each_analysis in analyses:
                                                lemma=""
                                                lables=""
                                                pos=""                                                
                                                counter=0
                                                #print(len(analyses))
                                                for analysis in each_analysis:
                                                        #In the analysis, 1st what we get is lemma
                                                        #second would be the POS category
                                                        #3rd will be analysis
                                                        if counter==0:
                                                                lemma=analysis
                                                        elif counter==1:
                                                                pos=analysis
                                                        else:
                                                                if counter==2:
                                                                        lables=analysis.split("=")[0]
                                                                else:
                                                                        if "=" in analysis:
                                                                                lable_new=analysis.split("=")[0]
                                                                                if lable_new=="3sghe" or lable_new=="3sghe" or lable_new=="3sghe":
                                                                                        lables=lables+","+"3e"+",hon"
                                                                                elif lable_new=="soc" or lable_new =="loc":
                                                                                        lables=lables+","+"loc"
                                                                                elif lable_new=="gen" or lable_new =="loc":
                                                                                        lables=lables+","+"loc"
                                                                                else:
                                                                                        lables=lables+","+lable_new
                                                                        else:
                                                                                lables=lables+","+analysis
                                                        counter=counter+1
                                                pos_morph = 0
                                                #since there are two analysis, there we decide which one to choose
                                                #since number (sg/pl) does not have any effect, it is neglected here
                                                #though is comes as part of the analysis
                                                if word.upos.lower()=="verb" and pos =="verb" and (lables == "nonfin,sim,futANDadjpart=உம்" or lables =="fin,sim,strong,fut=உம்,3pln=∅" or lables == "fin,sim,strong,fut=உம்,3sgn=∅"):
                                                        if word.text+ "." in sent.text:
                                                                lables="fin,sim,strong,fut,3n"
                                                        else:
                                                                lables="nonfin,sim,futANDadjpart"
                                                        pos_morph=1
                                                elif word.upos.lower()=="verb" and pos =="verb" and (lables == "fin,sim,past,3ple" or lables =="fin,sim,past,3sghe"):
                                                        lables="fin,sim,past,3e,hon"
                                                        pos_morph=1                                                
                                                elif ((word.upos.lower()=="noun" or word.upos.lower()=="propn") and pos =="noun") and (lables == "gen" or lables =="abl"):
                                                        lables="gen"
                                                        pos_morph=1
                                                elif ((word.upos.lower()=="noun" or word.upos.lower()=="propn") and pos =="noun") and (lables == "gen" or lables =="loc"):
                                                        lables="loc"
                                                        pos_morph=1                                                
                                                elif word.upos.lower() == pos:
                                                        pos_morph=1
                                                elif word.upos.lower()=="det" and (pos == "part" or pos == "dem"):
                                                        pos_morph = 1
                                                elif word.upos.lower()=="num" and (pos == "ordinal" or pos == "cardinal"):
                                                        pos_morph = 1
                                                elif word.upos.lower()=="cconj" and pos == "conjuction":
                                                        pos_morph = 1
                                                elif word.upos.lower()=="adp" and (pos == "nmod" or pos == "casemarker" or pos =="cop"):
                                                        pos_morph = 1
                                                elif word.upos.lower()== "propn" and pos == "noun":
                                                        pos_morph = 1
                                                if pos_morph==1:
                                                        if lables=="":
                                                                lables="_"
                                                        #'-'.join(list(set(lables.split(",")))) this is to remove duplicate lables, and convert the list to a string
                                                        pos_morph_aligned.write(str(word_id) + "\t" + word.text + "\t" + lemma + "\t" + word.upos+ "\t" +  '-'.join(list(set(lables.split(","))))  + "\n")
                                                        break;
                                                else:
                                                        if lables=="":
                                                                lables="_"
                                                        pos_morph_aligned.write(str(word_id) + "\t" + word.text + "\t" + lemma + "\t" + pos.upper()+ "\t" + '-'.join(list(set(lables.split(",")))) + "\n")
                                                        pos_tagged.write(str(word_id) + "\t" + word.text + "\t" + word.upos+ "\t" + lemma + "\t" + pos + "\t" + '-'.join(list(set(lables.split(",")))) + "\n")
                                        
                                #if the given word is not found in lexicons, in this cases gussers will be applied
                                else:
                                        #print(word.text)
                                        #print("Guesser")
                                        #here it is assumed that UPOS is correct, and a guesser is chosen based on the UPOS
                                        guesser_list=[]
                                        if word.upos == "ADJ":
                                                guesser_list.append("adj-guess.fst")
                                        elif word.upos == "ADV":
                                                guesser_list.append("adv-guess.fst")
                                        elif word.upos == "NOUN" or word.upos == "PROPN" or word.upos == "PRON" :
                                                guesser_list.append("noun-guess.fst")                                                
                                        elif word.upos == "VERB" or word.upos == "AUX" :
                                                guesser_list.append("verb-guess.fst")
                                        else:
                                                #if the given word is a particle, then no further analysis will be done as currently, there are no gusser for particles
                                                pos_morph_aligned.write(str(word_id) + "\t" + word.text + "\t" + "_" + "\t" + word.upos+ "\t" + "_" + "\n")
                                                pos_tagged.write(str(word_id) + "\t" + word.text + "\t" + word.upos+ "\t" + "_" + "\t" + "_" + "\n")
                                                word_id=word_id+1
                                                continue
                                                
                                        gusses = guess_morphemes(word.text.strip(),guesser_list)
                                        analysis_success=gusses
                                        if gusses != 0 :
                                                for each_guess in gusses:
                                                        counter=0
                                                        lemma=""
                                                        lables=""
                                                        pos=""                                                        
                                                        for analysis in each_guess:
                                                                #print(analysis)
                                                                if counter==0:
                                                                        lemma=analysis
                                                                        
                                                                elif counter==1:
                                                                        pos=analysis
                                                                else:
                                                                        if counter==2:
                                                                                lables=analysis
                                                                        else:
                                                                                #if the analysis has =, which means if Morph information are there.
                                                                                if "=" in analysis:
                                                                                        lable_new=analysis.split("=")[0]
                                                                                        if lable_new=="3sghe" or lable_new=="3sghe" or lable_new=="3sghe":
                                                                                                lables=lables+","+"3e"+",hon"
                                                                                        elif lable_new=="soc" or lable_new =="loc":
                                                                                                lables=lables+","+"loc"
                                                                                        elif lable_new=="gen" or lable_new =="loc":
                                                                                                lables=lables+","+"loc"
                                                                                        else:
                                                                                                lables=lables+","+lable_new
                                                                                else:
                                                                                        lables=lables+","+analysis
                                                                                
                                                                counter=counter+1
                                                        pos_morph = 0
                                                        
                                                        #this piece is to compare upos and the pos from ThamizhiMorph
                                                        if word.upos.lower()=="verb" and pos =="verb" and (lables == "nonfin,sim,futANDadjpart=உம்" or lables =="fin,sim,strong,fut=உம்,3pln=∅" or lables == "fin,sim,strong,fut=உம்,3sgn=∅"):
                                                                if word.text+ "." in sent.text:
                                                                        lables="fin,sim,strong,fut,3n"
                                                                else:
                                                                        lables="nonfin,sim,futANDadjpart"
                                                                pos_morph=1
                                                        elif ((word.upos.lower()=="noun" or word.upos.lower()=="propn") and pos =="noun") and (lables == "gen" or lables =="abl"):
                                                                lables="gen"
                                                                pos_morph=1                                                        
                                                        elif word.upos.lower() == pos:
                                                                pos_morph=1
                                                        elif word.upos.lower()== "propn" and pos == "noun":
                                                                pos_morph = 1
                                                        elif word.upos.lower()== "pron" and pos == "noun":
                                                                pos_morph = 1                                                                
                                                        if pos_morph==1:
                                                                if lables=="":
                                                                        lables="_"
                                                                pos_morph_aligned.write(str(word_id) + "\t" + word.text + "\t" + lemma + "\t" + word.upos+ "\t" + '-'.join(list(set(lables.split(",")))) + "\n")
                                                                break;
                                                        else:
                                                                if lables=="":
                                                                        lables="_"
                                                                pos_morph_aligned.write(str(word_id) + "\t" + word.text + "\t" + "_" + "\t" + word.upos+ "\t" + "_" + "\n")
                                                                pos_tagged.write(str(word_id) + "\t" + word.text + "\t" + word.upos+ "\t" + lemma + "\t" + pos + "\t" + '-'.join(list(set(lables.split(",")))) + "\n")
                                                                break;
                                        else:
                                                if lables=="":
                                                        lables="_"
                                                pos_morph_aligned.write(str(word_id) + "\t" + word.text + "\t" + "Unknown" + "\t" + word.upos+ "\t" + "Unknown" + "\n")
                                                pos_tagged.write(str(word_id) + "\t" + word.text + "\t" + "Unknown" + "\t" + word.upos+ "\t" + "Unknown" + "\n")

                                        
                        #this is a word counter
                        #if(analysis_success !=0) :
                        word_id=word_id+1
pos_morph_aligned.close()
pos_tagged.close()
