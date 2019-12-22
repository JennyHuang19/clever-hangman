'''
Created on Nov 15, 2019

@author: JennyH
'''
'''
Description:
        You must create a Hangman game that allows the user to play and guess a secret word.  
        See the assignment description for details.
    
@author: Jenny Yijian Huang    YourNetID yjh3
'''
import random
#problems: misses remaining still not decreasing
#maybe the public test is failing because runGame is failing?
#my code is not updating the template after each guess. Instead, it starts a new template, so maybe create new template is wrong in rungames.
#DO NOT ADJUST THIS CODE.


def handleUserInputDebugMode():
    '''
    This function will prompt the user if they wish to play in DEBUG mode. 
    True is returned if the user enters the letter “d”, 
    indicating DEBUG mode was chosen; False is returned otherwise. 
    '''
    mode = input("Which mode do you want: (d)ebug or (p)lay: ")
    if mode == "d":
        return True
    else:
        return False

def handleUserInputDifficulty():
    '''
    This function asks the user if they would like to play the game in (h)ard or (e)asy mode, then returns the 
    corresponding number of misses allowed for the game. 
    '''
    print("How many misses do you want? Hard has 8 and Easy has 12.")
    difficulty = input("(h)ard or (e)asy> ")
    if difficulty == 'e':
        return 12
    if difficulty == 'h':
        return 8
    
def handleUserInputWordLength():
    '''
    This function asks the user what length (5-10 inclusive) secretWord should be.
    '''
    length = input("How many letters in the word you'll guess: ")
    return int(length)

def createTemplate(currTemplate, letterGuess, word):
    '''
    This function will create a new template for 
    the secret word that the user will see. This function 
    will modify currentTemplate to reflect letterGuess.
    '''
    currTemplateLst = [char for char in currTemplate]
    idxLst = []
    for i in range(len(word)):
        if word[i] == letterGuess:
            idxLst.append(i)
            for i in idxLst:
                currTemplateLst[i] = letterGuess
    newTemplate = "".join(currTemplateLst)
    return newTemplate #a string
    
def maxUnderscore(list):
    '''
    Helper function for getNewWordList. Given a list of templates, 
    this function returns the template (a string) that has 
    the most number of underscores. 
    '''
    uscount = []
    for word in list:
        uscount.append(word.count("_"))
        maxLocation = uscount.index(max(uscount))
        desiredword = list[maxLocation]
    return desiredword

def getNewWordList(currTemplate, letterGuess, wordList, DEBUG):
    '''
    This function constructs a dictionary of the template corresponding to 
    the largest group of words (strings) as the key to lists of the 
    words that fit the template as the value. 
    '''
    templateDict = {} #{template: list of possible words} #your template lists are not of correct length in terms of template length.
    for word in wordList:
        key = createTemplate(currTemplate, letterGuess, word) #string   
        if key not in templateDict: 
            templateDict[key] = []
        templateDict[key].append(word) #add the word in wordlist as the value (in str form)
    #dictionary templateDict created at this point.
 

    #sort dictionary keys. break ties by count "_", main sort by by index of "_"
    sortedA = sorted(templateDict, key = lambda x: x.count("_"), reverse = False) #want smaller counts to be at the beginning.
    sortedKeys = sorted(sortedA, key = lambda x: x.index("_"), reverse = True) #want larger indices to be at the beginning.
    
    #print statements in getNewWordList.
    if DEBUG:
        for key in sortedKeys:
            print(key + " : " + str(len(templateDict[key])))
        print("# keys = " + str(len(sortedKeys)))

    #return the template and list of the value that is longest list.
    maxnum = 0
    for (key, templateDict[key]) in templateDict.items():
        if len(templateDict[key]) > maxnum:
            maxnum = len(templateDict[key])
    maxTemplate = [(key,templateDict[key]) for key in templateDict if len(templateDict[key]) == maxnum]
    #print(maxTemplate)
    if len(maxTemplate) == 1:
        return maxTemplate[0]
#returns the (template, list) pair with the longest list
    if len(maxTemplate) > 1:
        #UnderDict = {} #{template: numUnderscore}
        listTemp = [tuple[0] for tuple in maxTemplate]
        #print(listTemp)
        desiredTemplate = maxUnderscore(listTemp)
        Answer = [tuple for tuple in maxTemplate if tuple[0] == desiredTemplate][0]
        return Answer

            

def processUserGuessClever(letterGuess, hangmanWord, missesLeft):
    '''
    Takes the user's guess, the user's current progress 
    on the word, and the number of misses left; updates 
    the number of misses left and indicates whether the user missed.
    '''
    #hangmanWord is the list version of the template that was returned by getNewWordList.
    #your code should determine if the guess was a miss based on the guessed letter’s presence in your updated template.
    if letterGuess not in hangmanWord:
        missesLeft -= 1
        lst = [missesLeft, False]
    if letterGuess in hangmanWord:
        lst = [missesLeft, True]
    return lst


def createDisplayString(lettersGuessed, missesLeft, hangmanWord):
    '''
    Creates the string that will be displayed to the user, using the information in the parameters.
    '''
    alphabetLst = [l for l in "abcdefghijklmnopqrstuvwxyz"]
    for letter in lettersGuessed:
        index = alphabetLst.index(letter)
        alphabetLst[index] = " "
    
    displayString  = "letters not yet guessed: " + ''.join(alphabetLst) + "\n" 
    displayString += "misses remaining = " + str(missesLeft) + "\n" 
    displayString += ' '.join(hangmanWord) + "\n"
    return displayString


def handleUserInputLetterGuess(lettersGuessed, displayString):
    '''
    Prints displayString, then asks the user to input a letter to guess.
    This function handles the user input of the new letter guessed and checks if it is a repeated letter.
    '''
    print(displayString)
    newLetter = input("letter> ")
    while newLetter in lettersGuessed:
        print("you already guessed that")
        newLetter = input("letter> ")
    return newLetter


#Although some functions are unchanged from regular Hangman, how/when they should be called in runGame may change in the context of Clever Hangman.

def runGame(filename):
    '''
    This function sets up the game, runs each round, and prints a final message on whether or not the user won.
    True is returned if the user won the game. If the user lost the game, False is returned.
    '''
    #Loads the words from the file at the location specified in the parameter filename.
    f = open(filename)
    words = []
    for line in f:
        words.append(line.strip()) #take off the extra white space to either side of one line.
    f.close()
    wordList = words
    #User determines whether play on debug mode. 
    DEBUG = handleUserInputDebugMode()
    #User chooses the length of the secret word between 5-10 inclusive.
    length = handleUserInputWordLength()
    #Calls handleUserInputDifficulty and getWord
    missesLeft = handleUserInputDifficulty()
    originalMisses = missesLeft
    #Create the list of strings that holds the currently displayed hangman (a.k.a. hangmanWord).
    currTemplate = "".join(["_" for _ in range(length)]) #a string
    hangmanWord = currTemplate
    #while the current hangmanWord contains "_"
    misses = 0
    #no letters guessed set as initial condition.
    lettersGuessed = []
    #choose initial secret word.
    newWordList = [] #wordList is redefined as all possible words
    for word in wordList: #words in the textfile. Eclipse should have a way to highlight lines of code.
        if len(word) == len(currTemplate):
            newWordList.append(word)
#    print(wordList)
#     randomIndex = random.randint(0, len(wordList)-1)
#     word = wordList[randomIndex] #secretword - this is working correctly
    word = random.choice(newWordList)
    
    while missesLeft >= 1: #is guessedLetter different from letterGuess?
        #create the display string
        displayString = createDisplayString(lettersGuessed, missesLeft, hangmanWord)
        #prints display string then tell user to input new letter
        letterGuess = handleUserInputLetterGuess(lettersGuessed, displayString)
        #length of current word list:
        L = len(newWordList)
        wordList = newWordList
        #gets new word list based on guessedLetter. Prints keys if debug mode.
        tuple = getNewWordList(currTemplate, letterGuess, wordList, DEBUG) #a (template, list) tuple
        #create the updated template after a guessed letter, which is also the hangmanWord
        hangmanWord = tuple[0]
        newWordList = tuple[1]
        #subtracts from misses left and returns true if user guessed the letter correctly. Why is processUserGuessClever not being called on.
        Lst = processUserGuessClever(letterGuess, list(hangmanWord), missesLeft) 
        #adds guessedLetter to the list of lettersGuessed
        lettersGuessed.append(letterGuess)
        #choose a secret word from new wordList
        newWord = random.choice(newWordList) #wordList[1] is a list of the words corresponding to the new template. It is the first index of the return value of getNewWordList
        if DEBUG:
            print("(word is " + newWord + ")")
            print("# possible words: " + str(L))
            
        if Lst[1] == False:
            print("you missed: " + letterGuess + " not in word")
       
    if "_" not in hangmanWord:
        print("you guessed the word: " + newWord)
        GUESSES = str(len(lettersGuessed))
        MISSES = str(originalMisses - missesLeft)
        print("you made " + GUESSES + " guesses with " + MISSES + " misses")
        return True
    
    if "_" in hangmanWord:
        print("you're hung!!" + "\n" + "word is " + newWord)
        GUESSES = str(len(lettersGuessed))
        MISSES = str(originalMisses - missesLeft)
        print("you made " + GUESSES + " guesses with " + MISSES + " misses")
        return False
   #returns true if user won, false otherwise.
   #function is not returning all the possible keys. It is only returning the key that has the letter in it.



if __name__ == "__main__":
    '''
    Running CleverHangman.py should start the game, which is done by calling runGame, therefore, we have provided you this code below.
    '''
    #print(getNewWordList("tri_", "o", ["trio", "trip"], True))
    #a session can be multiple games
    won = 0
    lost = 0
    previousGame = runGame('shortLowerWords.txt')
    if previousGame == True:
        won += 1
    if previousGame == False:
        lost +=1
 
    decision = input("Do you want to play again? y or n> ")
     
    while decision == 'y':
        previousGame = runGame('lowerwords.txt')
        if previousGame == True:
            won += 1
        if previousGame == False:
            lost +=1
        decision = input("Do you want to play again? y or n> ")
    print("You won " + str(won) + " game(s)" + " and lost " + str(lost))