import stanza
import sys
import subprocess
import os

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

punct_dict = {".":"period",",":"comma",";":"semi-colon",":":"colon"}

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
for data_unit in data_input:
        doc = nlp(data_unit.replace("-", " "))                
        for sent in doc.sentences :
                pos_tagged.write(sent.text + "\n")
                pos_morph_aligned.write(sent.text + "\n")
                word_id=1
                
                for word in sent.words :
                        analysis_success=1
                        #All the Puncts are marked here with PUNCT. There are no analysis for PUNCT from ThamizhiMorph
                        if word.upos == "PUNCT" :
                                pos_morph_aligned.write(str(word_id) + "\t" + word.text + "\t" + word.upos+ "\t" + word.text + "\t" + word.upos + "\t" + word.upos + "\n")
                        elif word.text.isnumeric() :
                                pos_morph_aligned.write(str(word_id) + "\t" + word.text + "\t" + word.upos+ "\t" + word.text + "\t" + word.upos + "\t" + word.upos + "\n")                                
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
                                                                        lables=analysis
                                                                else:
                                                                        lables=lables+","+analysis
                                                        counter=counter+1
                                                pos_morph = 0
                                                #this piece is to compare upos and the pos from ThamizhiMorph
                                                if word.upos.lower() == pos:
                                                        pos_morph=1
                                                elif word.upos.lower()=="det" and pos == "part":
                                                        pos_morph = 1
                                                elif word.upos.lower()=="num" and (pos == "ordinal" or pos == "cardinal"):
                                                        pos_morph = 1
                                                elif word.upos.lower()=="cconj" and pos == "conjunction":
                                                        pos_morph = 1
                                                elif word.upos.lower()=="adp" and (pos == "nmod" or pos == "casemarker" or pos =="cop"):
                                                        pos_morph = 1
                                                elif word.upos.lower()=="det" and pos == "dem":
                                                        pos_morph = 1                                                        
                                                elif word.upos.lower()== "propn" and pos == "noun":
                                                        pos_morph = 1
                                                if pos_morph==1:
                                                  pos_morph_aligned.write(str(word_id) + "\t" + word.text + "\t" + word.upos+ "\t" + lemma + "\t" + pos + "\t" + lables + "\n")
                                                else:
                                                  pos_tagged.write(str(word_id) + "\t" + word.text + "\t" + word.upos+ "\t" + lemma + "\t" + pos + "\t" + lables + "\n")
                                        
                                #if the given word is not found in lexicons, in this cases gussers will be applied
                                else:
                                        print(word.text)
                                        print("Guesser")
                                        gusses = guess_morphemes(word.text.strip(),gussers)
                                        
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
                                                                                lables=lables+","+analysis
                                                                counter=counter+1
                                                        pos_morph = 0
                                                #this piece is to compare upos and the pos from ThamizhiMorph
                                                        if word.upos.lower() == pos:
                                                                pos_morph=1
                                                        elif word.upos.lower()=="det" and pos == "part":
                                                                pos_morph = 1
                                                        elif word.upos.lower()=="num" and (pos == "ordinal" or pos == "cardinal"):
                                                                pos_morph = 1
                                                        elif word.upos.lower()=="cconj" and pos == "conjunction":
                                                                pos_morph = 1
                                                        elif word.upos.lower()=="adp" and (pos == "nmod" or pos == "casemarker" or pos =="cop"):
                                                                pos_morph = 1
                                                        elif word.upos.lower()=="det" and pos == "dem":
                                                                pos_morph = 1                                                        
                                                        elif word.upos.lower()== "propn" and pos == "noun":
                                                                pos_morph = 1
                                                        if pos_morph==1:
                                                          pos_morph_aligned.write(str(word_id) + "\t" + word.text + "\t" + word.upos+ "\t" + lemma + "\t" + pos + "\t" + lables + "\n")
                                                        else:
                                                          pos_tagged.write(str(word_id) + "\t" + word.text + "\t" + word.upos+ "\t" + lemma + "\t" + pos + "\t" + lables + "\n")
                                                  
#                                                        pos_tagged.write(str(word_id) + "\t" + word.text + "\t" + word.upos+ "\t" + lemma + "\t" + pos + "\t" + lables + "\n")
                        #this is a word counter
                        if(analysis_success !=0) :
                                word_id=word_id+1
pos_morph_aligned.close()
pos_tagged.close()
