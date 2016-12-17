#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('./language-models')
sys.path.append('./data')
sys.path.append('./pysynth')
import pysynth
import random
from dataLoader import *
from unigramModel import *
from bigramModel import *
from trigramModel import *
from musicData import *

# -----------------------------------------------------------------------------
# Core ------------------------------------------------------------------------
# Functions to implement: trainLyricsModels, selectNGramModel,
# generateSentence, and runLyricsGenerator

def trainLyricsModels(lyricsDirectory):
    """
    Requires: nothing
    Modifies: nothing
    Effects:  loads lyrics data from the data/lyrics/<lyricsDirectory> folder
              using the pre-written DataLoader class, then creates an
              instance of each of the NGramModel child classes and trains
              them using the text loaded from the data loader. The list
              should be in tri-, then bi-, then unigramModel order.

              Returns the list of trained models.
    """

    dataLoader = DataLoader()

    # loading lyrics stored in dataLoader.lyrics
    dataLoader.loadLyrics(lyricsDirectory)
    models = [TrigramModel(), BigramModel(), UnigramModel()]

    # creating instance of each NGramModel child class
    unigram = UnigramModel()
    bigram = BigramModel()
    trigram = TrigramModel()

    # training each nGramModel child class using text loaded from data loader
    unigram.trainModel(dataLoader.lyrics)
    bigram.trainModel(dataLoader.lyrics)
    trigram.trainModel(dataLoader.lyrics)

    # returning list in correct order
    models = [trigram, bigram, unigram]

    return models

def selectNGramModel(models, sentence):
    """
    Requires: models is a list of NGramModel objects sorted by descending
              priority: tri-, then bi-, then unigrams.
    Modifies: nothing
    Effects:  starting from the beginning of the models list, returns the
              first possible model that can be used for the current sentence
              based on the n-grams that the models know. (Remember that you
              wrote a function that checks if a model can be used to pick a
              word for a sentence!)
    """

    #returns best model to be used in descending priority
    if models[0].trainingDataHasNGram(sentence):
        return models[0]

    elif models[1].trainingDataHasNGram(sentence):
        return models[1]

    else:
        return models[2]


def sentenceTooLong(desiredLength, currentLength):
    """
    Requires: nothing
    Modifies: nothing
    Effects:  returns a bool indicating whether or not this sentence should
              be ended based on its length. This function has been done for
              you.
    """
    STDEV = 1
    val = random.gauss(currentLength, STDEV)
    return val > desiredLength

def generateSentence(models, desiredLength):
    """
    Requires: models is a list of trained NGramModel objects sorted by
              descending priority: tri-, then bi-, then unigrams.
              desiredLength is the desired length of the sentence.
    Modifies: nothing
    Effects:  returns a list of strings where each string is a word in the
              generated sentence. The returned list should NOT include
              any of the special starting or ending symbols.

              For more details about generating a sentence using the
              NGramModels, see the spec.
    """
    sentence = ['^::^', '^:::^']
    length = 0
    newtoken = ''

    # if sentence is too long, sentence is done
    while not sentenceTooLong(desiredLength, length):
    	modelchoice = selectNGramModel(models, sentence)
    	newtoken = modelchoice.getNextToken(sentence)
      # if next token is $:::$, sentence is done
    	if newtoken != '$:::$':
    		sentence.append(newtoken)
        # subtract 2 to not count special symbols
        length = len(sentence) - 2

    # making sure final list doesn't contain the starting or ending symbols
    sentence.remove("^::^")
    sentence.remove('^:::^')
    # '$:::$' is never added so it doesn't need to be removed

    return sentence

def printSongLyrics(title, verseOne, verseTwo, chorus):
    """
    Requires: verseOne, verseTwo, and chorus are lists of lists of strings
    Modifies: nothing
    Effects:  prints the song. This function is done for you.
    """

    print 'Song Title: ' + ' '.join(word.capitalize() for word in title)

    verses = [verseOne, chorus, verseTwo, chorus]
    print '\n',
    for verse in verses:
        for line in verse:
            print (' '.join(line)).capitalize()
        print '\n',

def runLyricsGenerator(models):
    """
    Requires: models is a list of a trained nGramModel child class objects
    Modifies: nothing
    Effects:  generates a verse one, a verse two, and a chorus, then
              calls printSongLyrics to print the song out.
    """
    verseOne = []
    verseTwo = []
    chorus = []

    # each verse/chorus contains four sentences of desired length 6
    verseOne.append(generateSentence(models, 6))
    verseOne.append(generateSentence(models, 6))
    verseOne.append(generateSentence(models, 6))
    verseOne.append(generateSentence(models, 6))

    verseTwo.append(generateSentence(models, 6))
    verseTwo.append(generateSentence(models, 6))
    verseTwo.append(generateSentence(models, 6))
    verseTwo.append(generateSentence(models, 6))

    chorus.append(generateSentence(models, 6))
    chorus.append(generateSentence(models, 6))
    chorus.append(generateSentence(models, 6))

    lastLine = generateSentence(models, 6)
    length = len(lastLine)
    chorus.append(lastLine)

    title1 = lastLine[-2:]
    title2 = lastLine[-3:]

    title3 = [title1, title2]

    title = random.choice(title3)

    printSongLyrics(title, verseOne, verseTwo, chorus)

    return



# -----------------------------------------------------------------------------
# Reach -----------------------------------------------------------------------
# Functions to implement: trainMusicModels, generateMusicalSentence, and
# runMusicGenerator

def trainMusicModels(musicDirectory):
    """
    Requires: nothing
    Modifies: nothing
    Effects:  works exactly as trainLyricsModels from the core, except
              now the dataLoader calls the DataLoader's loadMusic() function
              and takes a music directory name instead of an artist name.
              Returns a list of trained models in order of tri-, then bi-, then
              unigramModel objects.
    """
    dataLoader = DataLoader()
    dataLoader.loadMusic(musicDirectory) # music stored in dataLoader.songs
    models = [TrigramModel(), BigramModel(), UnigramModel()]

    # add rest of trainMusicModels implementation here
    # add rest of trainLyricsModels implementation here
    unigram = UnigramModel()
    bigram = BigramModel()
    trigram = TrigramModel()

    # gotta train 'em all
    unigram.trainModel(dataLoader.songs)
    bigram.trainModel(dataLoader.songs)
    trigram.trainModel(dataLoader.songs)

    models = [trigram, bigram, unigram]
    return models

def generateMusicalSentence(models, desiredLength, possiblePitches):
    """
    Requires: possiblePitches is a list of pitches for a musical key
    Modifies: nothing
    Effects:  works exactly like generateSentence from the core, except
              now we call the NGramModel child class' getNextNote()
              function instead of getNextToken(). Everything else
              should be exactly the same as the core.
    """
    sentence = ['^::^', '^:::^']

    # add rest of generateMusicalSentence implementation here
    newnote = ()
    length = 0
    while not sentenceTooLong(desiredLength, length):
    	modelchoice = selectNGramModel(models, sentence)
    	newnote = modelchoice.getNextNote(sentence, possiblePitches)

    	if newnote != '$:::$':
        	sentence.append(newnote)
      # subtract 2 to not count special symbols
        length = len(sentence) - 2

    # final list doesn't contain symbols
    sentence.remove("^::^")
    sentence.remove('^:::^')
    # '$:::$' is never added so it doesn't need to be removed
    return sentence

# generates song that sounds more consonant using getNextGoodNote
def generateGoodMusicalSentence(models, desiredLength, possiblePitches):
    
    sentence = ['^::^', '^:::^']

    newnote = ()
    length = 0
    while not sentenceTooLong(desiredLength, length):
    	modelchoice = selectNGramModel(models, sentence)
    	newnote = modelchoice.getNextGoodNote(sentence, possiblePitches)

    	if newnote != '$:::$':
    		sentence.append(newnote)
      # subtract 2 to not count special symbols
        length = len(sentence) - 2

    # final list doesn't contain symbols
    sentence.remove("^::^")
    sentence.remove('^:::^')
    # '$:::$' is never added so it doesn't need to be removed
    return sentence

# makes the beginning and end of songs (if the user selects option 2 or 4) slower 
# notes are either quarter or half notes at beginning
def generateSlowMusicalSentence(models, desiredLength, possiblePitches):

    sentence = ['^::^', '^:::^']

    newnote = ()
    length = 0

    while not sentenceTooLong(desiredLength, length):
     	modelchoice = selectNGramModel(models, sentence)
     	newnote = modelchoice.getSlowNote(sentence, possiblePitches)

     	if newnote != '$:::$':
    		sentence.append(newnote)
      # subtract 2 to not count special symbols
    	length = len(sentence) - 2

    # final list doesn't contain symbols
    sentence.remove("^::^")
    sentence.remove('^:::^')
    # '$:::$' is never added so it doesn't need to be removed
    return sentence

def runMusicGenerator(models, songName):
    """
    Requires: models is a list of trained models
    Modifies: nothing
    Effects:  runs the music generator as following the details in the spec.

              Note: For the core, this should print "Under construction".
    """

    i = 0
    possiblePitches = KEY_SIGNATURES[random.choice(KEY_SIGNATURES.keys())]

    song = (generateMusicalSentence(models, 2, possiblePitches))
    tonic = (generateSlowMusicalSentence(models, 2, possiblePitches[0]))

    while (len(song) < 30):
    	song = song + (generateMusicalSentence(models, 2, possiblePitches)) 
    
    song = tonic + song + tonic
    
    pysynth.make_wav(song, fn = songName)


# function if the user selects option 4 from the main menu
# if the user selects 1, will play a song only using major keys
# if the user selects 2, will play a song only using minor keys
# if the user selects something other than 1 or 2, will play a song using a combination of major and minor keys
def runMajorMinorMusicGenerator(models, songName, majorOrMinor):

    i = 0
    possiblePitches = KEY_SIGNATURES[random.choice(KEY_SIGNATURES.keys())]
    majorPitches = MAJOR_KEYS[random.choice(MAJOR_KEYS.keys())]
    minorPitches = MINOR_KEYS[random.choice(MINOR_KEYS.keys())]


    song = (generateMusicalSentence(models, 2, possiblePitches))
    tonic = (generateSlowMusicalSentence(models, 2, possiblePitches[0]))

    if majorOrMinor == 1:
        while (len(song) < 30):
        	song = song + (generateMusicalSentence(models, 2, majorPitches))
    elif majorOrMinor == 2:
        while (len(song) < 30):
        	song = song + (generateMusicalSentence(models, 2, minorPitches))    
    else:
        while (len(song) < 30):
        	song = song + (generateMusicalSentence(models, 2, possiblePitches)) 
    
    song = tonic + song + tonic
    
    pysynth.make_wav(song, fn = songName)

# function if the user selects option 3 from the main menu
# generates music that is based off the c major pentatonix scale
# song is then mixed with a ready made bassline using a popular chord progression
def runGoodMusicGenerator(models, songName):
    i = 0
    possiblePitches = OTHER_KEY[random.choice(OTHER_KEY.keys())]
    song = (generateGoodMusicalSentence(models, 2, possiblePitches))
    tonic = (generateGoodMusicalSentence(models, 2, possiblePitches[0]))
    while (len(song) < 30):
        
        song = song + (generateGoodMusicalSentence(models, 2, possiblePitches))
            
    song = tonic + song + tonic
    pysynth.make_wav(song, fn = "out2.wav")
    pysynth.mix_files("out.wav", "out2.wav", songName, chann = 2, phase = -1.)


# -----------------------------------------------------------------------------
# Main ------------------------------------------------------------------------

def getUserInput(teamName, lyricsSource, musicSource):
    """
    Requires: nothing
    Modifies: nothing
    Effects:  prints a welcome menu for the music generator and prints the
              options for the generator. Loops while the user does not input
              a valid option. When the user selects 1, 2, or 3, returns
              that choice.

              Note: this function is for the reach only. It is done for you.
    """
    print 'Welcome to the', teamName, 'music generator!\n'
    prompt = 'Here are the menu options:\n' + \
             '(1) Generate song lyrics by ' + lyricsSource + '\n' \
             '(2) Generate a song using data from ' + musicSource + '\n' \
             '(3) Generate a more consonant song using data from ' + musicSource + '\n' \
             '(4) Generate either a song that is in the major or minor scale using data from ' + musicSource + '\n' \
             '(5) Quit the music generator\n'

    userInput = -1
    while userInput < 1 or userInput > 5:
        print prompt
        userInput = raw_input('Please enter a choice between 1 and 5: ')
        try:
            userInput = int(userInput)
        except ValueError:
            userInput = -1

    return userInput

def main():
    """
    Requires: nothing
    Modifies: nothing
    Effects:  this is your main function, which is done for you. It runs the
              entire generator program for both the reach and the core.
              It begins by loading the lyrics and music data, then asks the
              user to input a choice to generate either lyrics or music.

              Note that for the core, only choice 1 (the lyrics generating
              choice) needs to be completed; if the user inputs 2, you
              can just have the runMusicGenerator function print "Under
              construction."

              Also note that you can change the values of the first five
              variables based on your team's name, artist name, etc.
    """
    teamName = 'Pythonistas'
    lyricsSource = 'The Beatles'
    musicSource = 'Nintendo Gamecube'
    lyricsDirectory = 'the_beatles'
    musicDirectory = 'gamecube'

    print 'Starting program and loading data...'
    lyricsModels = trainLyricsModels(lyricsDirectory)
    musicModels = trainMusicModels(musicDirectory)
    print 'Data successfully loaded\n'

    userInput = getUserInput(teamName, lyricsSource, musicSource)

    while userInput != 5:
        print '\n',
        if userInput == 1:
            runLyricsGenerator(lyricsModels)
        elif userInput == 2:
            songName = raw_input('What would you like to name your song? ')
            runMusicGenerator(musicModels, 'wav/' + songName + '.wav')

        elif userInput == 3:
            songName = raw_input('What would you like to name your good song? ')
            runGoodMusicGenerator(musicModels, 'wav/' + songName + '.wav')

        elif userInput == 4:
            songName = raw_input('What would you like to name your song? ')
            print '\n',
            majorOrMinor = raw_input("Enter 1 if you want your song to be in a major scale," "\n" "2 if you want your song to be in a minor scale: ")

            runMajorMinorMusicGenerator(musicModels, 'wav/' + songName + '.wav', majorOrMinor)

        print '\n',
        userInput = getUserInput(teamName, lyricsSource, musicSource)

    print '\nThank you for using the', teamName, 'music generator!'



if __name__ == '__main__':

    main()
    
    #mix_files("out.wav", "out2.wav", "chord.wav", chann = 2, phase = -1.)

    # note that if you want to individually test functions from this file,
    # you can comment out main() and call those functions here. Just make
    # sure to call main() in your final submission of the project!
