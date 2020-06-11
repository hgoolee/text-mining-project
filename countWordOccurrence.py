import os


def wordOccurrence(fileName, substring, sortOccurrence):
    filePath = "./data/" + fileName

    if not os.path.exists(filePath):
        print(filePath, "does not exist!")
        exit(1)
    else:
        print("Word Occurrence of ", substring, " in <", filePath, "> is being counted!", sep="")

    newFileName = "[Word Occurrence of " + substring + "]" + fileName
    newFilePath = "./result/" + newFileName

    tempArray = []

    with open(filePath, "r", encoding='utf-8') as file:
        for line in file:
            count = line.count(substring)
            temp = [str(count), line]
            tempArray.append(temp)

    if sortOccurrence:
        tempArray.sort(key=lambda x: int(x[0]), reverse=True)

    newFile = open(newFilePath, "w", encoding='utf8')
    for element in tempArray:
        s = element[0] + "\t" + element[1]
        newFile.write(s)
    newFile.close()


# TODO: Select file name (MUST be in data folder)
FileName = "Chicago Tribune_date_content.txt"
# TODO: Select a substring to count occurrence
Substring = "South Korea"
# TODO: Select whether to sort occurrence or not
SortOccurrence = True

wordOccurrence(FileName, Substring, SortOccurrence)
