import random
from nGramModel import *


# -----------------------------------------------------------------------------
# TrigramModel class ----------------------------------------------------------
# Core functions to implement: trainModel, trainingDataHasNGram, and
# getCandidateDictionary

class TrigramModel(NGramModel):

    def __init__(self):
        """
        Requires: nothing
        Modifies: self (this instance of the NGramModel object)
        Effects:  this is the TrigramModel constructor, which is done
                  for you. It allows TrigramModel to access the data
                  from the NGramModel class.
        """
        super(TrigramModel, self).__init__()

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts, a three-dimensional dictionary. For
                  examples and pictures of the TrigramModel's version of
                  self.nGramCounts, see the spec.
        Effects:  this function populates the self.nGramCounts dictionary,
                  which has strings as keys and dictionaries as values,
                  where those inner dictionaries have strings as keys
                  and dictionaries of {string: integer} pairs as values.

                  Note: make sure to use the return value of prepData to
                  populate the dictionary, which will allow the special
                  symbols to be included as their own tokens in
                  self.nGramCounts. For more details, see the spec.
        """
        
        # builds a dictionary of potential trigrams and their counts

        text = self.prepData(text)
        for sentence in text:
            for i in range(len(sentence) - 2):
                if sentence[i] not in self.nGramCounts:
                    self.nGramCounts[sentence[i]] = {}
                if sentence[i + 1] not in self.nGramCounts[sentence[i]]:
                    self.nGramCounts[sentence[i]][sentence[i + 1]] = {}
                if sentence[i + 2] not in (self.nGramCounts[sentence[i]][sentence[i + 1]]):
                    self.nGramCounts[sentence[i]][sentence[i+1]][sentence[i + 2]] = 0
                self.nGramCounts[sentence[i]][sentence[i+1]][sentence[i + 2]] += 1

        return self.nGramCounts


    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings, and len(sentence) >= 2
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. For explanations of how this
                  is determined for the TrigramModel, see the spec.
        """
        # returns true if model has seen the second to last and last words in current sentence at start of trigram
        if sentence[-2] in self.nGramCounts:
          if sentence[-1] in self.nGramCounts:
            return True
        else:
            return False

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. For details on which words the
                  TrigramModel sees as candidates, see the spec.
        """
        return self.nGramCounts[sentence[-2]][sentence[-1]]


# -----------------------------------------------------------------------------
# Testing code ----------------------------------------------------------------

if __name__ == '__main__':
    text = [ ['the', 'quick', 'brown', 'fox'], ['the', 'lazy', 'dog'] ]
    sentence = [ 'the', 'quick', 'brown' ]
    trigramModel = TrigramModel()
    # add your own testing code here if you like
    # print trigramModel.trainModel(text)
    # print trigramModel.trainingDataHasNGram(sentence)
    # print trigramModel.getCandidateDictionary(sentence)
