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

def getWordDist(filename, wordDict):
    f = open(filename, 'r')
    for line in f:
        allWord = line.split(" ")
        for word in allWord:

            # remove the punctuation and treat all upper case the
            # same as lower case
            table = {ord(char): None for char in string.punctuation}
            word = word.translate(table)
            word = word.lower()

            if len(word) >= 10:
                wordDict[10] += 1
            elif len(word) > 0:
                # print(len(word), word)
                wordDict[len(word)] += 1

def storeAllFile(input_file, output_file, useDist):

    # get all files in the directory
    allFile = os.listdir(input_file)
    if not useDist:
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
    else:
        header = ["Article_Name", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # header = ["Article_Name", 1, 2, 3, 4, 5]
        ofile = open(output_file, "w")
        writer = csv.DictWriter(ofile, fieldnames=header)
        writer.writeheader()
        for file in allFile:
            filePath = input_file + file
            wordDict = {"Article_Name": file, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}
            # wordDict = {"Article_Name": file, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            getWordDist(filePath, wordDict)
            writer.writerow(wordDict)

    

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
    parser.add_argument('-o', '--output_file', type=str, default='articles.csv')
    parser.add_argument('-d', '--useDist', action='store_true', help='Use word distribution or not')
    args = parser.parse_args()
    filename = args.input_file
    outname = args.output_file
    outname = "./parsedArticles/" + outname
    storeAllFile(filename, outname, args.useDist)