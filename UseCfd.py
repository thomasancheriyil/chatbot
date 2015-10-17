import nltk
import BuildCfd
import re,commands
#from BuildCfd import frequency
cfd = BuildCfd.getCfd()

def BuildAnswerDict(inpToken):
    bestSentDict = {}
    for word in inpToken:
        if word not in cfd.keys():
            continue
        freqObj = cfd[word]
        cfdDict = freqObj.getSentDict()
        sumFreq = freqObj.getSum()
        for sentence,freq in cfdDict.iteritems():
            if sentence not in bestSentDict.keys():
                bestSentDict[sentence] = float(freq/sumFreq)
            else:
                bestSentDict[sentence] = bestSentDict[sentence] + float(freq/sumFreq)
    return bestSentDict

def BuildBestAnswer(inpToken):
    ansDict = BuildAnswerDict(inpToken)
    maxFreq = 0
    bestAnswer = ""
    for sentence, freq in ansDict.iteritems():
        if freq>=maxFreq:
            maxFreq = freq
            bestAnswer = sentence
    return bestAnswer

            
	    
def getOutput(inp):
    inp = re.sub("[^A-Za-z]"," ",inp)
    inp = inp.lower()
    inpToken = nltk.word_tokenize(inp)
    result = BuildBestAnswer(inpToken)
    return result


if __name__ == '__main__':
    #bestAnswers = BuildBestAnswer()

    inp ="pos"
    while not inp.lower()=="bye":
	    inp = raw_input('Enter Query:')
	    inp = re.sub("[^A-Za-z]"," ",inp)
	    inp = inp.lower()
	    inpToken = nltk.word_tokenize(inp)
    	    result = BuildBestAnswer(inpToken)
	    #print commands.getoutput("/usr/bin/espeak -v en+f4 -p 99 -s 160 \"" + result + "\"")
	    print result
    	    
