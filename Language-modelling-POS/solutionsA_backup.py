import math
import nltk
import time
from collections import Counter
# Constants to be used by you when you fill the functions
START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
MINUS_INFINITY_SENTENCE_LOG_PROB = -1000

# TODO: IMPLEMENT THIS FUNCTION
# Calculates unigram, bigram, and trigram probabilities given a training corpus
# training_corpus: is a list of the sentences. Each sentence is a string with tokens separated by spaces, ending in a newline character.
# This function outputs three python dictionaries, where the keys are tuples expressing the ngram and the value is the log probability of that ngram
def calc_probabilities(training_corpus):
    unigram_p = {}
    bigram_p = {}
    trigram_p = {}
    total_unigram=0
    unigram_freq=Counter()
    bigram_freq=Counter()
    trigram_freq=Counter()
    u_freq=Counter()
    for line in training_corpus:
        line1=line+" "+STOP_SYMBOL
        unigram_tokens=line1.split()
        unigram_freq.update(unigram_tokens)
        total_unigram=total_unigram+len(unigram_tokens)
        sent=STOP_SYMBOL+" "+START_SYMBOL+" "+line+" "+STOP_SYMBOL+" "+START_SYMBOL
        tokens=sent.split()
        u_freq.update(tokens)
        bigram_tuples=list(nltk.bigrams(tokens))
        bigram_freq.update(bigram_tuples)
        trigram_tuples=list(nltk.trigrams(tokens))
        trigram_freq.update(trigram_tuples)

    for key in unigram_freq:
        unigram_p[(key,)]= math.log(unigram_freq[key]/float(total_unigram),2)

    for key in bigram_freq:
        bigram_p[key]= math.log(bigram_freq[key]/float(u_freq[key[0]]),2)
    
    for key in trigram_freq:
        trigram_p[key]=math.log(trigram_freq[key]/float(bigram_freq[key[0],key[1]]),2)

    
    return unigram_p, bigram_p, trigram_p

# Prints the output for q1
# Each input is a python dictionary where keys are a tuple expressing the ngram, and the value is the log probability of that ngram
def q1_output(unigrams, bigrams, trigrams, filename):
    # output probabilities
    outfile = open(filename, 'w')

    unigrams_keys = unigrams.keys()
    unigrams_keys.sort()
    for unigram in unigrams_keys:
        outfile.write('UNIGRAM ' + unigram[0] + ' ' + str(unigrams[unigram]) + '\n')

    bigrams_keys = bigrams.keys()
    bigrams_keys.sort()
    for bigram in bigrams_keys:
        outfile.write('BIGRAM ' + bigram[0] + ' ' + bigram[1]  + ' ' + str(bigrams[bigram]) + '\n')

    trigrams_keys = trigrams.keys()
    trigrams_keys.sort()    
    for trigram in trigrams_keys:
        outfile.write('TRIGRAM ' + trigram[0] + ' ' + trigram[1] + ' ' + trigram[2] + ' ' + str(trigrams[trigram]) + '\n')

    outfile.close()


# TODO: IMPLEMENT THIS FUNCTION
# Calculates scores (log probabilities) for every sentence
# ngram_p: python dictionary of probabilities of uni-, bi- and trigrams.
# n: size of the ngram you want to use to compute probabilities
# corpus: list of sentences to score. Each sentence is a string with tokens separated by spaces, ending in a newline character.
# This function must return a python list of scores, where the first element is the score of the first sentence, etc. 
def score(ngram_p,n,corpus):
    scores = []
    for sentence in corpus:
            sentence1= sentence +" "+STOP_SYMBOL
            sentence2 = START_SYMBOL +" "+sentence + " "+STOP_SYMBOL
            sentence3 = STOP_SYMBOL +" "+START_SYMBOL+" "+sentence +" "+STOP_SYMBOL+" "+START_SYMBOL
            if n==1:
                unigram_tokens = sentence1.split()
                score = 0
                for unigram in unigram_tokens:
                    try:
                        score +=  ngram_p[(unigram,)]
                    except:
                        score = MINUS_INFINITY_SENTENCE_LOG_PROB
                        break
                scores.append(score)
            if n==2:
                tokens = sentence2.split()
                bigram_list = list(nltk.bigrams(tokens))
                prob = 0
                for bigram in bigram_list:
                    try:
                        prob += ngram_p[bigram]
                    except:
                        prob = MINUS_INFINITY_SENTENCE_LOG_PROB
                        scores.append(prob)
                        break
                scores.append(prob)
            if n==3:
                tokens3 = sentence3.split()
                trigram_list = list(nltk.trigrams(tokens3))
                prob = 0
                for trigram in trigram_list:
                    try:
                        prob += ngram_p[trigram]
                    except:
                        prob = MINUS_INFINITY_SENTENCE_LOG_PROB
                        scores.append(prob)
                        break
                scores.append(prob)

    return scores
# Outputs a score to a file
# scores: list of scores
# filename: is the output file name
def score_output(scores, filename):
    outfile = open(filename, 'w')
    for score in scores:
        outfile.write(str(score) + '\n')
    outfile.close()

# TODO: IMPLEMENT THIS FUNCTION
# Calculates scores (log probabilities) for every sentence with a linearly interpolated model
# Each ngram argument is a python dictionary where the keys are tuples that express an ngram and the value is the log probability of that ngram
# Like score(), this function returns a python list of scores
def linearscore(unigrams, bigrams, trigrams, corpus):
    scores = []
    lamb=float(1)/3;
    for line in corpus:
        line= STOP_SYMBOL+" "+START_SYMBOL+" "+line+" "+STOP_SYMBOL
        tokens = line.split()
        trigram = list(nltk.trigrams(tokens))
        prob=0
        for t in trigram:
            c=t[2]
            b=t[1]
            a=t[0]
            tri= pow(2,trigrams[(a,b,c)])
            bi= pow(2,bigrams[(b,c)])
            uni= pow(2,unigrams[(c,)])
            prob= prob + math.log(lamb*(tri+bi+uni),2)
            
#         print prob
        scores.append(prob)
                

    return scores

DATA_PATH = 'data/'
OUTPUT_PATH = 'output/'

# DO NOT MODIFY THE MAIN FUNCTION
def main():
    # start timer
    time.clock()

    # get data
    infile = open(DATA_PATH + 'Brown_train.txt', 'r')
    corpus = infile.readlines()
    infile.close()

    # calculate ngram probabilities (question 1)
    unigrams, bigrams, trigrams = calc_probabilities(corpus)

    # question 1 output
    q1_output(unigrams, bigrams, trigrams, OUTPUT_PATH + 'A1.txt')

    # score sentences (question 2)
    uniscores = score(unigrams, 1, corpus)
    biscores = score(bigrams, 2, corpus)
    triscores = score(trigrams, 3, corpus)

    # question 2 output
    score_output(uniscores, OUTPUT_PATH + 'A2.uni.txt')
    score_output(biscores, OUTPUT_PATH + 'A2.bi.txt')
    score_output(triscores, OUTPUT_PATH + 'A2.tri.txt')

    # linear interpolation (question 3)
    linearscores = linearscore(unigrams, bigrams, trigrams, corpus)

    # question 3 output
    score_output(linearscores, OUTPUT_PATH + 'A3.txt')

    # open Sample1 and Sample2 (question 5)
    infile = open(DATA_PATH + 'Sample1.txt', 'r')
    sample1 = infile.readlines()
    infile.close()
    infile = open(DATA_PATH + 'Sample2.txt', 'r')
    sample2 = infile.readlines()
    infile.close() 

    # score the samples
    sample1scores = linearscore(unigrams, bigrams, trigrams, sample1)
    sample2scores = linearscore(unigrams, bigrams, trigrams, sample2)

    # question 5 output
    score_output(sample1scores, OUTPUT_PATH + 'Sample1_scored.txt')
    score_output(sample2scores, OUTPUT_PATH + 'Sample2_scored.txt')

    # print total time to run Part A
    print "Part A time: " + str(time.clock()) + ' sec'

if __name__ == "__main__": main()
