from main import replace_accented
from sklearn import svm
from sklearn import neighbors
from operator import itemgetter
import nltk
import string

# don't change the window size
window_size = 10

# A.1
def build_s(data):
    '''
    Compute the context vector for each lexelt
    :param data: dict with the following structure:
        {
			lexelt: [(instance_id, left_context, head, right_context, sense_id), ...],
			...
        }
    :return: dict s with the following structure:
        {
			lexelt: [w1,w2,w3, ...],
			...
        }

    '''
    s = {}

    # implement your code here
    for key,value in data.items():
      for i in value:
        tokens_left = nltk.word_tokenize(i[1])
        tokens_right = nltk.word_tokenize(i[3])
        left = [w for w in tokens_left if w not in string.punctuation][-window_size:]
        right = [w for w in tokens_right if w not in string.punctuation][:window_size]
        context = left + right
        if key not in s:
          s[key]=[]
        for word in context:
          if word not in s[key]:
            s[key].append(word)            
          
    return s


# A.1
def vectorize(data, s):
    '''
    :param data: list of instances for a given lexelt with the following structure:
        {
			[(instance_id, left_context, head, right_context, sense_id), ...]
        }
    :param s: list of words (features) for a given lexelt: [w1,w2,w3, ...]
    :return: vectors: A dictionary with the following structure
            { instance_id: [w_1 count, w_2 count, ...],
            ...
            }
            labels: A dictionary with the following structure
            { instance_id : sense_id }

    '''
    vectors = {}
    labels = {}
    instance_data=[]
    
    for i in data:
      tokens_left = nltk.word_tokenize(i[1])
      tokens_right = nltk.word_tokenize(i[3])
      left = [w for w in tokens_left][-window_size:]
      right = [w for w in tokens_right][:window_size]
      context = left + right
      #instance_data.append([i[0], context, i[4]])
      labels[i[0]] = i[4]
      
      if i[0] not in vectors.keys():
        vectors[i[0]]=[]
      for wordlist in s:
        count=0
        for word in context:
          if wordlist==word:
            count+=1
        vectors[i[0]].append(count)
        
        
    # implement your code here

    return vectors, labels


# A.2
def classify(X_train, X_test, y_train):
    '''
    Train two classifiers on (X_train, and y_train) then predict X_test labels

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

    :return: svm_results: a list of tuples (instance_id, label) where labels are predicted by LinearSVC
             knn_results: a list of tuples (instance_id, label) where labels are predicted by KNeighborsClassifier
    '''

    svm_results = []
    knn_results = []
    
    svm_clf = svm.LinearSVC()
    knn_clf = neighbors.KNeighborsClassifier()
    
    svm_clf.fit(X_train.values(), y_train.values())
    svm_labels = svm_clf.predict(X_test.values())
    
    knn_clf.fit(X_train.values(), y_train.values())
    knn_labels = knn_clf.predict(X_test.values())
    
    #knn_results.append([(X_test.keys(), svm_clf.predict(X_test.keys()))])
    # implement your code here
    i=0
    for key in X_test.keys():
      svm_results.append((key, svm_labels[i]))
      knn_results.append((key, knn_labels[i]))
      i+=1
    
    return svm_results, knn_results

# A.3, A.4 output
def print_results(results ,output_file):
    '''

    :param results: A dictionary with key = lexelt and value = a list of tuples (instance_id, label)
    :param output_file: file to write output

    '''
    output=[]
    for key,values in results.items():
      for i in values:
        lexelt_item = replace_accented(key)
        instance_id = replace_accented(i[0])
        label = i[1]
        output.append((lexelt_item, instance_id, label))
        
    output_sorted= sorted(output, key = itemgetter(0,1))
    out=open(output_file, 'w')
    for item in output_sorted:
      out.write(item[0]+" "+item[1]+" "+item[2]+"\n")
    out.close()
    #ut.write([item for item in output_sorted])
      
      
    # implement your code here
    # don't forget to remove the accent of characters using main.replace_accented(input_str)
    # you should sort results alphabetically by lexelt_item, then on 
    # instance_id before printing

# run part A
def run(train, test, language, knn_file, svm_file):
    s = build_s(train)
    svm_results = {}
    knn_results = {}
    for lexelt in s:
        X_train, y_train = vectorize(train[lexelt], s[lexelt])
        X_test, _ = vectorize(test[lexelt], s[lexelt])
        svm_results[lexelt], knn_results[lexelt] = classify(X_train, X_test, y_train)

    print_results(svm_results, svm_file)
    print_results(knn_results, knn_file)



