import random
import sys
import copy
sys.path.append('../data')
from musicData import *

# -----------------------------------------------------------------------------
# NGramModel class ------------------------------------------------------------
# Core functions to implement: prepData, weightedChoice, and getNextToken
# Reach functions to implement: getNextNote

class NGramModel(object):

    def __init__(self):
        """
        Requires: nothing
        Modifies: self (this instance of the NGramModel object)
        Effects:  This is the NGramModel constructor. It sets up an empty
                  dictionary as a member variable. It is called from the
                  constructors of the NGramModel child classes. This
                  function is done for you.
        """
        self.nGramCounts = {}

    def __str__(self):
        """
        Requires: nothing
        Modifies: nothing
        Effects:  returns the string to print when you call print on an
                  NGramModel object. This function is done for you.
        """
        return 'This is an NGramModel object'

    def prepData(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: nothing
        Effects:  returns a copy of text where each inner list starts with
                  the symbols '^::^' and '^:::^', and ends with the symbol
                  '$:::$'. For example, if an inner list in text were
                  ['hello', 'goodbye'], that list would become
                  ['^::^', '^:::^', 'hello', 'goodbye', '$:::$'] in the
                  returned copy.
                  Make sure you are not modifying the original text
                  parameter in this function.
        """

        textCopy = []

        # creating a deep copy of text, so all elements in original list are copied
        textCopy = copy.deepcopy(text)

        length = len(textCopy)

        # adds ^::^ followed by ^:::^ to beginning of each sentence
        # adds $:::$ to end of sentence
        for i in range(length):
            textCopy[i].insert(0, '^:::^')
            textCopy[i].insert(0, '^::^')
            textCopy[i].append('$:::$')

        return textCopy

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts
        Effects:  this function populates the self.nGramCounts dictionary.
                  It does not need to be modified here because you will
                  override it in the NGramModel child classes according
                  to the spec.
        """

        return

    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns a bool indicating whether or not this n-gram model
                  can be used to choose the next token for the current
                  sentence. This function does not need to be modified because
                  you will override it in NGramModel child classes according
                  to the spec.
        """
        return False

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. This function does not need to be
                  modified because you will override it in the NGramModel child
                  classes according to the spec.
        """
        return {}

    def weightedChoice(self, candidates):
        """
        Requires: candidates is a dictionary; the keys of candidates are items
                  you want to choose from and the values are integers
        Modifies: nothing
        Effects:  returns a candidate item (a key in the candidates dictionary)
                  based on the algorithm described in the spec.
        """

        countValues = []
        tokenKeys = []

        # taking the keys and values from candidates and placing them in lists
        for key in candidates:
            tokenKeys.append(key)
            countValues.append(candidates[key])

        # creating a cumulative list
        cumulative = [countValues[0]]

        # calculates cumulative count list and adds it to dictionary
        for i in range(1, len(countValues)):
          cumulative.append(cumulative[i - 1] + countValues[i])

        # compares random value with cumulative list values
        randomNum = random.randrange(0, cumulative[-1] + 1)
        j = 0

        # calculates index while random number is greater than cumulative count
        while randomNum > cumulative[j]:
          j = j + 1

        # returns the first token at index whose corresponding cumulative count is larger than random number
        return tokenKeys[j]


    def getNextToken(self, sentence):
        """
        Requires: sentence is a list of strings, and this model can be used to
                  choose the next token for the current sentence
        Modifies: nothing
        Effects:  returns the next token to be added to sentence by calling
                  the getCandidateDictionary and weightedChoice functions.
                  For more information on how to put all these functions
                  together, see the spec.
        """

        # getting a list of candidate next words for the sentence
        # by choosing next word for the sentence based on weights of candidate word
        # returns chosen word
        return self.weightedChoice(self.getCandidateDictionary(sentence))


    def getNextNote(self, musicalSentence, possiblePitches):
        """
        Requires: musicalSentence is a list of PySynth tuples,
                  possiblePitches is a list of possible pitches for this
                  line of music (in other words, a key signature), and this
                  model can be used to choose the next note for the current
                  musical sentence
        Modifies: nothing
        Effects:  returns the next note to be added to the "musical sentence".
                  For details on how to do this and how this will differ
                  from the getNextToken function from the core, see the spec.
                  Please note that this function is for the reach only.
        """

        allCandidates = self.getCandidateDictionary(musicalSentence)

        constrainedCandidates = {}
        # finish constrainedCandidates
        for key in allCandidates:
          if key == '$:::$':
            #add to constrainedCandidates
            constrainedCandidates[key] = allCandidates[key]

          else:
            for pitch in possiblePitches:
              compKey = key[0][:-1]
              if pitch == compKey:
                constrainedCandidates[key] = allCandidates[key]

        if len(constrainedCandidates) != 0:
          return self.weightedChoice(constrainedCandidates)

        else:
          # first item in tuple
          firstItem = (random.choice(possiblePitches))
          firstItem.join('4')

          # second item
          secondItem = (random.choice(NOTE_DURATIONS))

        return (firstItem, secondItem)

    def getNextGoodNote(self, musicalSentence, possiblePitches):
        """
        Requires: musicalSentence is a list of PySynth tuples,
                  possiblePitches is a list of possible pitches for this
                  line of music (in other words, a key signature), and this
                  model can be used to choose the next note for the current
                  musical sentence
        Modifies: nothing
        Effects:  returns the next note to be added to the "musical sentence".
                  For details on how to do this and how this will differ
                  from the getNextToken function from the core, see the spec.
                  Please note that this function is for the reach only.
        """

        allCandidates = self.getCandidateDictionary(musicalSentence)

        constrainedCandidates = {}
        # finish constrainedCandidates
        for key in allCandidates:
          if key == '$:::$':
            #add to constrainedCandidates
            constrainedCandidates[key] = allCandidates[key]

          else:
            for pitch in possiblePitches:
              compKey = key[0][:-1]
              compOct = key[0][-1:]
              if pitch == compKey and ((key[1] == 8) or (key[1] == 4)) and compOct == 3:
                constrainedCandidates[key] = allCandidates[key]

        if len(constrainedCandidates) != 0:
          return self.weightedChoice(constrainedCandidates)

        else:
          # first item in tuple
          firstItem = (random.choice(possiblePitches))
          firstItem.join('4')

          # second item
          secondItem = (random.choice(OTHER_NOTE_DURATIONS))

        return (firstItem, secondItem)

    def getSlowNote(self, musicalSentence, possiblePitches):
        """
        Requires: musicalSentence is a list of PySynth tuples,
                  possiblePitches is a list of possible pitches for this
                  line of music (in other words, a key signature), and this
                  model can be used to choose the next note for the current
                  musical sentence
        Modifies: nothing
        Effects:  returns the next note to be added to the "musical sentence".
                  For details on how to do this and how this will differ
                  from the getNextToken function from the core, see the spec.
                  Please note that this function is for the reach only.
        """

        allCandidates = self.getCandidateDictionary(musicalSentence)

        constrainedCandidates = {}
        # finish constrainedCandidates
        for key in allCandidates:
          if key == '$:::$':
            # add to constrainedCandidates
            constrainedCandidates[key] = allCandidates[key]

          else:
            for pitch in possiblePitches:
              compKey = key[0][:-1]
              if pitch == compKey and key[1] == 2:
                constrainedCandidates[key] = allCandidates[key]

        if len(constrainedCandidates) != 0:
          return self.weightedChoice(constrainedCandidates)

        else:
          # first item in tuple
          firstItem = (random.choice(possiblePitches))
          firstItem.join('4')

          # second item
          secondItem = (random.choice(SLOW_DURATIONS))

        return (firstItem, secondItem)

# -----------------------------------------------------------------------------
# Testing code ----------------------------------------------------------------

if __name__ == '__main__':
    text = [ ['the', 'quick', 'brown', 'fox'], ['the', 'lazy', 'dog'] ]
    choices = { 'the': 2, 'quick': 1, 'brown': 1 }
    choices1 = { 'the': 2, 'quick': 1, 'brown': 1, 'hello': 3, 'hi': 5 }
    sentence = ['the']
    pitches = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
    nGramModel = NGramModel()

    #print nGramModel.getNextNote(sentence, pitches)
