
from random import sample
import time
from timeit import timeit
from itertools import combinations
import networkx as nx


G = nx.Graph()


def readFile(path):
    fileObj = open(path,
                   'r')  # opens the file in read mode
    words = fileObj.read().splitlines()  # puts the file into an array
    fileObj.close()
    return words


#wordList = readFile('wordle-allowed-guesses.txt')
#wordList = readFile('wordle-answers-alphabetical.txt')
wordList = ["bemix", "bling", "blunk", "brick", "brung", "chunk", "cimex", "clipt", "clunk", "cylix", "fjord", "glent", "grypt", "gucks", "gymps", "jumby", "jumpy", "kempt", "kreng", "nymph", "pling", "prick", "treck", "vibex", "vozhd", "waltz", "waqfs", "xylic"]

wordList = [word for word in wordList if len(word) == 5 and len(word)==len(set(word)) ]
print("number of words after filtering: " + str(len(wordList)))
def graphMaker(wordList):
    #create new dictionary to map each word to a bitmask
    newDict = {}
    # loop through each character in a word, ord() is to get the unicode value of a character, as the letters a-z are represented from 97-122 in unicode, 
    # subtracting 97 from the unicode value of a character would give us the position of a letter, e.g ord('c')-97 will give us 2, which is the 3rd position(counting from 0), 
    # then we apply a left shift 2 times to get 0b100, 
    # then we sum it with all the other letters in the word to get our final binary value of a word, "abcde" will be 0b11111
    # A limitation of this is that we could not use words with repeating letters, however we already excluded that in our initial wordlist as we can only use 5 words to get 25 distinct letters.
    # why left shift and not right shift? because a right shift replaces the least significant bit which will result in a 0b1 in all letters and we will not be able to identify different letters.
    for word in wordList:
        newDict[word] = sum(1<<(ord(char)-97) for char in word )
    items = list(newDict.items())
    edges = []
    for i,(word,word_mask) in enumerate(newDict.items()):
        for word2,word2_mask in items[i+1:]:
            if not (word_mask&word2_mask):
                edges.append([word,word2])
                G.add_edge(word,word2)
                
    return (edges)

print(str(timeit(lambda: graphMaker(wordList), number=1))+'s to complete 1 loops, beginning clique find')
st = time.time()
for clq in nx.clique.find_cliques(G):
    if(len(clq) ==5 ):
        print(clq)
et = time.time()
print(str(et-st) + "s to find all cliques")