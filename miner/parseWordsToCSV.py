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
import argparse

def getFileDict(filename, wordDict):
    f = open(filename, 'r')
    result = {}
    for line in f:
        allWord = line.split(" ")
        for word in allWord:

            # remove the punctuation and treat all upper case the
            # same as lower case
            table = {ord(char): None for char in string.punctuation}
            word = word.translate(table)
            word = word.lower()

            # if it is a valid english word
            if word.isalpha():
                wordDict.add(word)
                if word in result.keys():
                    result[word] += 1
                else:
                    result[word] = 1
    return result


def storeAllFile(input_file, output_file):

    # get all files in the directory
    allFile = os.listdir(input_file)
    wordDict = set()
    articlesInfo = []

    # process the files to store the name and count
    for file in allFile:
        filePath = input_file + file
        info = getFileDict(filePath, wordDict)
        info["Article_Name"] = file
        articlesInfo.append(info)

    # add in the row for name
    wordDict = list(wordDict)
    wordDict = ["Article_Name"] + wordDict

    rowInfo = fillOutNotExistWord(wordDict, articlesInfo)

    produceCSV(rowInfo, output_file)

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

def produceCSV(rowInfo, output_file):
    ofile = open(output_file, "w")
    writer = csv.writer(ofile, quoting=csv.QUOTE_NONNUMERIC)
    # print(rowInfo)
    writer.writerows(rowInfo)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help='Input file')
    parser.add_argument('-o', '--output_file', type=str, default='out.csv')
    args = parser.parse_args()
    filename = args.input_file
    outname = args.output_file
    storeAllFile(filename, outname)



