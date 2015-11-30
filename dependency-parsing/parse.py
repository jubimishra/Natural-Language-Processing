from providedcode.transitionparser import TransitionParser
from providedcode.dependencygraph import DependencyGraph
import sys
import nltk

if __name__ == '__main__':
    model = sys.argv[1]
    for line in sys.stdin:
        sentence = DependencyGraph.from_sentence(line)
        for key, dct in sentence.nodes.items():
           dct['ctag'] = nltk.tag.mapping.map_tag("en-ptb", "universal", dct['ctag'])
        tp = TransitionParser.load(model)
        parsed = tp.parse([sentence])
        print parsed[0].to_conll(10).encode('utf-8')
