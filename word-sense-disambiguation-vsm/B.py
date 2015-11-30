import A
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm
from sklearn import neighbors
from operator import itemgetter
import nltk
import string
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import nltk.tag
from nltk.data import load
from collections import Counter
import math
import sys
from sklearn.feature_selection import SelectPercentile, chi2

# You might change the window size
window_size = 15

# B.1.a,b,c,d
def extract_features(data):
    '''
    :param data: list of instances for a given lexelt with the following structure:
        {
			[(instance_id, left_context, head, right_context, sense_id), ...]
        }
    :return: features: A dictionary with the following structure
             { instance_id: {f1:count, f2:count,...}
            ...
            }
            labels: A dictionary with the following structure
            { instance_id : sense_id }
    '''
    features = {}
    labels = {}
    if sys.argv[6]== "English":
      stop_words = stopwords.words('english');
      stemmer = SnowballStemmer("english", ignore_stopwords=True);
      
#	  if sys.argv[6] == 'Spanish':
#      stop_words = stopwords.words('spanish')
#      stemmer = SnowballStemmer("spanish", ignore_stopwords=True)
   

    sense_list= set([])
    temp = []
    # implement your code here
    for i in data:
      instance_id = i[0]
      sense_id = i[4]
      labels[instance_id]=i[4]
      head = i[2]
      tokens_left = nltk.word_tokenize(i[1])
      tokens_right = nltk.word_tokenize(i[3])
      main = nltk.word_tokenize(i[2])

      left = [w for w in tokens_left if w not in string.punctuation][-window_size:]
      right = [w for w in tokens_right if w not in string.punctuation][:window_size]
#      left =  [stemmer.stem(w.lower()) for w in tokens_left if w not in string.punctuation and w not in stop_words][-window_size:]
#      right = [stemmer.stem(w.lower()) for w in tokens_right if w not in string.punctuation and w not in stop_words][:window_size]
      context = left + right
      
      
      left_tag = [tup[1] for tup in nltk.pos_tag(left)[-window_size:]]
      for tup in nltk.pos_tag(main):
        head_tag = tup[1]
      right_tag = [tup[1] for tup in nltk.pos_tag(left)[:window_size]]
            
      sense_list.add(sense_id)
      if sense_id!="":
        temp.append([sense_id, context, instance_id])
        
#------------> SYNSET SYNONYM IMPLEMENTATION   
      if instance_id not in features.keys():
        features[instance_id] = {}
        
#      if sys.argv[6] == "Spanish":
#        syn_word_head = wn.synsets(head, lang = "spa")
#        syn_word_left = wn.synsets(left[-1], lang = "spa")
#        syn_word_right = wn.synsets(right[1], lang = "spa")
#      
#      elif sys.argv[6] == "Catalan":
#        syn_word_head = wn.synsets(head, lang = "cat")
#        syn_word_left = wn.synsets(left[-1], lang = "cat")
#        syn_word_right = wn.synsets(right[1], lang = "cat")
#
#      else:
#        syn_word_head = wn.synsets(head)
#        syn_word_left = wn.synsets(left[-1])
#        try:
#          syn_word_right = wn.synsets(right[1])
#        except:
#          pass
#        
#
#      try:
#        features[instance_id]["head0"] =  syn_word_head[0].name()
#      except:
#        features[instance_id]["head0"] =  ""
#      try:
#        features[instance_id]["head1"] =  syn_word_head[1].name()
#      except:
#        features[instance_id]["head1"] =  ""
#      try:
#        features[instance_id]["head2"] =  syn_word_head[2].name()
#      except:
#        features[instance_id]["head2"] =  ""
#      try:
#        features[instance_id]["left0"] =  syn_word_left[0].name()
#      except:
#        features[instance_id]["left0"] =  ""
#      try:
#        features[instance_id]["left1"] =  syn_word_left[1].name()
#      except:
#        features[instance_id]["left1"] =  ""
#      try:
#        features[instance_id]["left2"] =  syn_word_left[2].name()
#      except:
#        features[instance_id]["left2"] =  ""
#      
#      try:
#        features[instance_id]["right0"] =  syn_word_right[0].name()
#      except:
#        features[instance_id]["right0"] =  ""
#      try:
#        features[instance_id]["right1"] =  syn_word_right[1].name()
#      except:
#        features[instance_id]["right1"] =  ""
#      try:
#        features[instance_id]["right2"] =  syn_word_right[2].name()
#      except:
#        features[instance_id]["right2"] =  ""


##-----------------> Neighbouring words 
      features[instance_id]["w0"] = head
      try:
        features[instance_id]["w1"] = right[0]
      except:
        features[instance_id]["w1"] = ""
      try:
        features[instance_id]["w2"] = right[1]
      except:
         features[instance_id]["w2"] = ""
      try:
        features[instance_id]["w3"] = right[2]
      except:
         features[instance_id]["w3"] = ""
      
      try:
        features[instance_id]["w-1"] = left[-1]
      except:
         features[instance_id]["w-1"] = ""
      try:
        features[instance_id]["w-2"] = left[-2]
      except:
        features[instance_id]["w-2"] = ""
      try:
        features[instance_id]["w-3"] = left[-3]
      except:
        features[instance_id]["w-3"] = ""
      
#-----------> POS Tagging
       
#      features[instance_id]["pos0"] = head_tag
#      try:
#        features[instance_id]["pos1"] = right_tag[1]
#      except:
#        features[instance_id]["pos1"] = ""
#      try:
#        features[instance_id]["pos2"] = right_tag[2]
#      except:
#        features[instance_id]["pos2"] = ""
#      try:
#        features[instance_id]["pos3"] = right_tag[3]
#      except:
#        features[instance_id]["pos3"] = ""
#      try:
#        features[instance_id]["pos-1"] = left_tag[-1]
#      except:
#        features[instance_id]["pos-1"] = ""
#      try:
#        features[instance_id]["pos-2"] = left_tag[-2] 
#      except:
#        features[instance_id]["pos-2"] = ""
#      try:
#        features[instance_id]["pos-3"] = left_tag[-3]
#      except:
#        features[instance_id]["pos-3"] = ""

#----------> Relevancy Score Implementation      
#    x={}    
#    for sense in sense_list:
#      if sense not in x.keys():
#        x[sense]=[]
#      for t in temp:
#        if t[0]==sense:
#          x[sense].append(t[1])
#    p={}
#    rel={}
#    m=Counter()
#    n=[]
#    for sense, context in x.items():
#        m= Counter(sum(context,[]))
#        for c, value in m.items():
#            n.append([c, sense, value])
#            if c not in p.keys():
#                p[c]=[]
#            p[c].append([sense, value])
#    
#    
#    for key, values in p.items():
#      total=0
#      for value in values:
#          total= total+value[1]
#      for i in n:
#  #         i[1] is sense, i[0] is word in context
#          if i[0]==key:
#              prob = i[2]/(total*1.0)
#              if i[1] not in rel.keys():
#                  rel[i[1]]= {}
#              if 1-prob == 0:
#                  rel[i[1]][key]= 32767
#              elif prob ==0:
#                  rel[i[1]][key] = -32767
#              else:
#                  rel[i[1]][key] =  math.log((float)(prob)/(1 - prob))
#    
#
#    top_words=[]
#    for inst, sense_id in labels.items():
#        if inst not in features.keys():
#            features[inst] = {}
#        for sense, words in rel.items():
#          top = sorted(words.items(), key =  lambda x: -x[1])
#          top_words = [tup[0] for tup in top if tup[1]>0.0]
#          if labels[inst]==sense:
#            for i in range(0,5):
#              try:
#                features[inst]['topword'+str(i)] = top_words[i]
#              except:
#                features[inst]['topword'+str(i)] = ""           
      
    return features, labels

# implemented for you
def vectorize(train_features,test_features):
    '''
    convert set of features to vector representation
    :param train_features: A dictionary with the following structure
             { instance_id: {f1:count, f2:count,...}
            ...
            }
    :param test_features: A dictionary with the following structure
             { instance_id: {f1:count, f2:count,...}
            ...
            }
    :return: X_train: A dictionary with the following structure
             { instance_id: [f1_count,f2_count, ...]}
            ...
            }
            X_test: A dictionary with the following structure
             { instance_id: [f1_count,f2_count, ...]}
            ...
            }
    '''
    X_train = {}
    X_test = {}

    vec = DictVectorizer()
    vec.fit(train_features.values())
    for instance_id in train_features:
        X_train[instance_id] = vec.transform(train_features[instance_id]).toarray()[0]

    for instance_id in test_features:
        X_test[instance_id] = vec.transform(test_features[instance_id]).toarray()[0]

    return X_train, X_test

#B.1.e
def feature_selection(X_train,X_test,y_train):
    '''
    Try to select best features using good feature selection methods (chi-square or PMI)
    or simply you can return train, test if you want to select all features
    :param X_train: A dictionary with the following structure
             { instance_id: [f1_count,f2_count, ...]}
            ...
            }
    :param X_test: A dictionary with the following structure
             { instance_id: [f1_count,f2_count, ...]}
            ...
            }
    :param y_train: A dictionary with the following structure
            { instance_id : sense_id }
    :return:
    '''
#    chi =  SelectPercentile(chi2, 50)
#    xtrain = []
#    ytr = []
#
#    for instance_id, value in X_train.items():
#      xtrain.append(value)
#      ytr.append(y_train[instance_id])
#      
#    for instance_id, value in X_test.items():
#      xtest.append(value)
#      
#    X_train_new = chi.fit_transform(xtrain, ytr)

#    return X_train_new, X_test
    # implement your code here

    #return X_train_new, X_test_new
    # or return all feature (no feature selection):
    return X_train, X_test

# B.2
def classify(X_train, X_test, y_train):
    '''
    Train the best classifier on (X_train, and y_train) then predict X_test labels

    :param X_train: A dictionary with the following structure
            { instance_id: [w_1 count, w_2 count, ...],
            ...
            }

    :param X_test: A dictionary with the following structure
            { instance_id: [w_1 count, w_2 count, ...],
            ...
            }

    :param y_train: A dictionary with the following structure
            { instance_id : sense_id }

    :return: results: a list of tuples (instance_id, label) where labels are predicted by the best classifier
    '''

    results = []
    
#    svm_clf = svm.LinearSVC()
#
#    svm_clf.fit(X_train.values(), y_train.values())
#    svm_labels = svm_clf.predict(X_test.values())
#    i=0
#    for key in X_test.keys():
#      results.append((key, svm_labels[i]))
#      i+=1

    # implement your code here
    xtrain = []
    ytrain = []
    xtest = []
    for instance_id, value in X_train.items():
      xtrain.append(value)
      ytrain.append(y_train[instance_id])

    for instance_id, value in X_test.items():
      xtest.append(value)
    
    svm_clf = svm.LinearSVC()
    svm_clf.fit(xtrain, ytrain)
    svm_labels = svm_clf.predict(xtest)
    i=0
    for key in X_test.keys():
      results.append((key, svm_labels[i]))
      i+=1  

      
    return results

# run part B
def run(train, test, language, answer):
    results = {}

    for lexelt in train:

        train_features, y_train = extract_features(train[lexelt])
        test_features, _ = extract_features(test[lexelt])

        X_train, X_test = vectorize(train_features,test_features)
        X_train_new, X_test_new = feature_selection(X_train, X_test,y_train)
        results[lexelt] = classify(X_train_new, X_test_new,y_train)

    A.print_results(results, answer)