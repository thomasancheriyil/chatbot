import nltk
import re
#import aiml
import commands
import os
#from nltk import wordnet as wn

cfd={}

#Mapping from Nltk's Pos tags to Wordnet's Pos tag
#morphy_tag = {'NN':wn.NOUN,'JJ':'a','VB':'v','RB':'r'}


#TO learn more add more sentences to this list
#input=['What do you like doing', 'Tell about yourself']


#reading the input from file q.txt
f=open("q.txt","r");
input= f.readlines();
#Increase frequency of the particular word
class frequent:
    sentDict={}
    probSum=0.0
#defining the initialisation condition
    def __init__(self,sent,prob):
        self.sentDict={}
        self.probSum=0.0
        for i in xrange(0,len(sent)):
            if sent[i] in self.sentDict.keys():
                #self.probSum = self.probSum+prob
                self.sentDict[sent[i]] = self.sentDict[sent[i]]+prob
                #print self.sentDict[sent[i]]
            else:
                self.sentDict[sent[i]] = prob
                #self.probSum = prob
                #print sent,self.sentDict[sent[i]]
    def appendList(self,sent,prob):
        for i in xrange(0,len(sent)):
            if sent[i] in self.sentDict.keys():
                #self.probSum = self.probSum+prob
                self.sentDict[sent[i]] = self.sentDict[sent[i]]+prob
                #print sent,self.sentDict[sent[i]]
            else:
                self.sentDict[sent[i]] = prob
                #self.probSum = prob
                #print sent,self.sentDict[sent[i]]
    def getSum(self):
        if self.probSum>0:
            return self.probSum
        for key,val in self.sentDict.iteritems():
            self.probSum = self.probSum+val
        return self.probSum
    def getSentDict(self):
        return self.sentDict


def ProcessInput(inpStr):
	tokens = nltk.word_tokenize(inpStr)
	posTag = nltk.pos_tag(tokens)
	for i in xrange(0,len(posTag)):
            posTag = tags[i][1][0:2]
            if(pos in morphy_tag.keys()):
                morph = wn.morphy(posTag[i][0],morphy_tag[pos])
                if not morph:
                    del tokens[i]
                else:
                    tokens[i]=tokens[i]+"##"+pos # Using ## as a delimiter to identify
            else:
                del tokens[i]
                
        return tokens

def homework(inp):
    k = aiml.Kernel()
    k.learn("std-startup.xml")
    k.respond("load aiml b")
    os.system("clear")
    k.setBotPredicate("name", "Chatty")
    response = k.respond(inp)
    return response

def BuildCfd(filename="cfd.dat"):

#reading the q.txt file
    File = open(filename,"r")
    cfdLines = File.readlines()
    for Line in cfdLines:
        cfdList = Line.split("::")
        key = cfdList[0]
        for i in xrange(1,len(cfdList)-1):
            if i%2==0:
                continue
            if key in cfd.keys():
                cfd[key].appendList([cfdList[i]],float(cfdList[i+1]))
            else:
                cfd[key] = frequent([cfdList[i]],float(cfdList[i+1]))
    #print cfd

def writeFile():
    File = open("cfd.dat","w")
    for key,freqObj in cfd.iteritems():
        File.write(key+'::')
        sentDict = freqObj.getSentDict();
        for sentence,frequency in sentDict.iteritems():
            File.write(sentence+'::'+str(frequency)+'::')
        File.write(str(freqObj.getSum())+'\n');
    File.close()

    #Questions chatbot asks the Trainer
if __name__ == '__main__':
    BuildCfd()
    #k = aiml.Kernel()
    #k.learn("std-startup.xml")
    #k.respond("load aiml b")
    #os.system("clear")
    #k.setBotPredicate("name", "Chatty")
    for inp in input:
	if not inp:
	    continue
        print inp #'Chatbot>'+inp+'\n'
        opList=[]
        #Keep getting responses and store them in opList
        
        #print 'Wish to Say? Y/N'
        #while raw_input()=='Y':
        #    opList.append(raw_input('You>'))
        #    print 'Wish to Say more? Y/N'
        #opList.append(k.respond(inp))
        op=raw_input('Your answer:')
	opList.append(op)
        inp = re.sub("[^A-Za-z]"," ",inp)
        inp = inp.lower()
        inpToken = nltk.word_tokenize(inp)
	if len(inpToken)==0:
	    continue
        #For each token, append the result sentence and its share in the result

	#this line actually appends the result to the file cfd.dat
        probToken =1.0/len(inpToken)
        for each in inpToken:
            #print probToken
            if each in cfd.keys():
                cfd[each].appendList([op for op in opList],probToken)
                #print type(cfd[each])
            else:
                cfd[each] = frequent([op for op in opList],probToken)
                
    writeFile()


def getCfd():
    BuildCfd()
    return cfd
