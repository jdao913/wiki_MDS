"""
Produce a CSV file from the text file in a particular directory,
in a format (Article_Name, word, word, ... , word),
with each row representing an article and the word count.

If a word exists in any file in the directory it would be listed as a column.
If a word not exists in a particular file it would have a 0 for that column.

"""

import csv
import string
import os

def getFileDict(filename, wordDict):
    f = open(filename, 'r')
    result = {}
    for line in f:
        allWord = line.split(" ")
        for word in allWord:

            # remove the punctuation and treat all upper case the
            # same as lower case
            word = word.translate(None, string.punctuation)
            word = word.lower()

            # if it is a valid english word
            if word.isalpha():
                wordDict.add(word)
                if word in result.keys():
                    result[word] += 1
                else:
                    result[word] = 1
    return result


def storeAllFile():

    # get all files in the directory
    allFile = os.listdir('text_files')
    wordDict = set()
    articlesInfo = []

    # process the files to store the name and count
    for file in allFile:
        filePath = "text_files/" + file
        info = getFileDict(filePath, wordDict)
        info["Article_Name"] = file
        articlesInfo.append(info)

    # add in the row for name
    wordDict = list(wordDict)
    wordDict = ["Article_Name"] + wordDict

    rowInfo = fillOutNotExistWord(wordDict, articlesInfo)

    produceCSV(rowInfo)

def fillOutNotExistWord(wordDict, articlesInfo):
    result = [list(wordDict)]

    for info in articlesInfo:
        singleFileList = []
        for word in wordDict:
            if word in info.keys():
                singleFileList.append(info[word])
            else:
                singleFileList.append(0)
        result.append(singleFileList)

    return result

def produceCSV(rowInfo):
    ofile = open('test.csv', "wb")
    writer = csv.writer(ofile, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerows(rowInfo)

if __name__ == "__main__":
    storeAllFile()



