import random
from providedcode import dataset
from providedcode.transitionparser import TransitionParser
from providedcode.evaluate import DependencyEvaluator
from featureextractor import FeatureExtractor
from transition import Transition
# New import
import nltk

if __name__ == '__main__':
    data = dataset.get_swedish_train_corpus().parsed_sents()
    random.seed(1234)
    subdata = random.sample(data, 200)

    data_eng = dataset.get_english_train_corpus().parsed_sents()
    random.seed(1234)
    subdata_eng = random.sample(data_eng, 200)

    data_dan = dataset.get_danish_train_corpus().parsed_sents()
    random.seed(1234)
    subdata_dan = random.sample(data_dan, 200)

    try:

        # BAD MODEL ###########################################################
        tp = TransitionParser.load('badfeatures.model')
        testdata = dataset.get_swedish_test_corpus().parsed_sents()
        parsed = tp.parse(testdata)

        ev = DependencyEvaluator(testdata, parsed)
        print "Bad Features Model"
        print "UAS: {} \nLAS: {}".format(*ev.eval())

        # SWEDISH #############################################################
        tp = TransitionParser(Transition, FeatureExtractor)
        tp.train(subdata)
        tp.save('swedish.model')

        testdata = dataset.get_swedish_test_corpus().parsed_sents()
        # tp = TransitionParser.load('badfeatures.model')

        parsed = tp.parse(testdata)

        with open('swedish_test.conll', 'w') as f:
            for p in parsed:
                f.write(p.to_conll(10).encode('utf-8'))
                f.write('\n')

        ev = DependencyEvaluator(testdata, parsed)
        print "Swedish"
        print "UAS: {} \nLAS: {}".format(*ev.eval())

        # ENGLISH #############################################################
        tp = TransitionParser(Transition, FeatureExtractor)
        tp.train(subdata_eng)
        tp.save('english.model')

        testdata = dataset.get_english_dev_corpus().parsed_sents()

        parsed = tp.parse(testdata)

        with open('english_test.conll', 'w') as f:
            for p in parsed:
                f.write(p.to_conll(10).encode('utf-8'))
                f.write('\n')

        ev = DependencyEvaluator(testdata, parsed)
        print "English"
        print "UAS: {} \nLAS: {}".format(*ev.eval())

        # DANISH #############################################################
        tp = TransitionParser(Transition, FeatureExtractor)
        tp.train(subdata_dan)
        tp.save('danish.model')

        testdata = dataset.get_danish_test_corpus().parsed_sents()

        parsed = tp.parse(testdata)

        with open('danish_test.conll', 'w') as f:
            for p in parsed:
                f.write(p.to_conll(10).encode('utf-8'))
                f.write('\n')

        ev = DependencyEvaluator(testdata, parsed)
        print "Danish"
        print "UAS: {} \nLAS: {}".format(*ev.eval())

        # parsing arbitrary sentences (english):
        # sentence = DependencyGraph.from_sentence('Hi, this is a test')

        # tp = TransitionParser.load('english.model')
        # parsed = tp.parse([sentence])
        # print parsed[0].to_conll(10).encode('utf-8')
    except NotImplementedError:
        print """
        This file is currently broken! We removed the implementation of Transition
        (in transition.py), which tells the transitionparser how to go from one
        Configuration to another Configuration. This is an essential part of the
        arc-eager dependency parsing algorithm, so you should probably fix that :)

        The algorithm is described in great detail here:
            http://aclweb.org/anthology//C/C12/C12-1059.pdf

        We also haven't actually implemented most of the features for for the
        support vector machine (in featureextractor.py), so as you might expect the
        evaluator is going to give you somewhat bad results...

        Your output should look something like this:

            LAS: 0.23023302131
            UAS: 0.125273849831

        Not this:

            Traceback (most recent call last):
                File "test.py", line 41, in <module>
                    ...
                    NotImplementedError: Please implement shift!


        """
