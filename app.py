import random

def getRandomWord():
    wordsPath = "./words.txt"
    wordsFile = open(wordsPath, "r")
    words = wordsFile.readlines()
    randint = random.randint(0, len(words)-1)
    return words[randint].replace("\n", "")
    #Words not by me
    #https://github.com/Xethron/Hangman/blob/master/words.txt

def start():
    word = getRandomWord()
    pword = ""
    for c in word:
        if(c!=" "):
            pword += "_"
        pword += " "

    print("Welcome to the Hangman game!")
    print("Word: " + pword)
    guessesLeft = 6
    guessed = []
    while guessesLeft != 0:
        if(len(guessed) > 1):
            for x in word:
                if(x not in guessed):
                    break
            else:
                print("\nYou won with %d guesses left!" %guessesLeft)
                break

                
        print("")
        print("Enter your guess:")
        guess = input(">>> ")
        if(len(guess) > 1):
            print("")
            print("Please, enter just one letter:")
        elif(type(guess) != str or guess == " " or len(guess) == 0):
            print("")
            print("Please, enter only letters:")
        else:
            if(guess in word):
                if(guess in guessed):
                    print("")
                    print("You have already guessed letter %s" %guess)
                else:
                    guessed.append(guess)
                pword = ""
                for c in word:
                    if(c in guessed):
                        pword += c
                    elif(c != " "):
                        pword += "_"
                    pword += " "
            else:
                guessesLeft -= 1
        print(pword)
        print("Guesses left %d" % guessesLeft)
    else:
        print("")
        print("You lost! The word was: %s" % word)


try:
    start()
except KeyboardInterrupt:
    print("\nThanks for playing!")
    