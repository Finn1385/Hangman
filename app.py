import random
from flask import Flask, flash, redirect, url_for, render_template, session

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

    
app = Flask(__name__)
app.secret_key = "random"

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]


@app.route("/")
def index():
    if("guessedLetters" in session):
        word = session["guessingWord"]
        guessed = session["guessedLetters"]
        incorrect = session["incorrect"]
        pword = ""
        for c in word:
            if(c in guessed):
                pword += c
            elif(c!=" "):
                pword += "_"
            pword += " "
        if(session["incorrect"] == 7):
            session.clear()
            return render_template("index.html", imgWrong=incorrect, letters=alphabet, guessed=guessed, pword=pword, word=word, win=False)
        else:
            if("_" not in pword):
                session.clear()
                return render_template("index.html", imgWrong=incorrect, letters=alphabet, guessed=guessed, pword=pword, word=word, win=True)
            else:
                return render_template("index.html", imgWrong=incorrect, letters=alphabet, guessed=guessed, pword=pword, word=word)

    else: #Start a new game
        word = getRandomWord()
        print(word)
        pword = ""
        for c in word:
            if(c!=" "):
                pword += "_"
            pword += " "
        session["guessingWord"] = word
        session["incorrect"] = 0
        return render_template("index.html", imgWrong=0, letters=alphabet, guessed=[], pword=pword, word=word)


@app.route("/<letter>")
def guess(letter):
    if(letter != "favicon.ico"):
        if(len(letter) > 1 or type(letter) != str or not letter.isalpha()):
            return redirect(url_for("index"))
        else:
            if("guessedLetters" not in session):
                session["guessedLetters"] = [letter]
            else:
                glList = session["guessedLetters"]
                glList.append(letter)
                session["guessedLetters"] = glList
            if(letter not in session["guessingWord"]):
                session["incorrect"] += 1
            return redirect(url_for("index"))
    return redirect(url_for(index))
        
    

if __name__ == "__main__":
    app.run(debug=True)