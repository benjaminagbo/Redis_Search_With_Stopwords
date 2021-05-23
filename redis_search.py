import redis
conn=redis.StrictRedis(host='localhost',port=6379, decode_responses=True, charset='utf-8')
conn.flushdb()
def GetFile(fileName):
    items=[]
    with open(fileName, 'r') as f:
        for line in f:
            for word in line.split():
                word=word.strip(".,?")
                items.append(word)

    return items



def listToSet(myList, myList2):
    for words in myList:
        conn.sadd(myList2, words)


def setToKeyword(set, setString):
    for words in set:
        conn.sadd(words, setString)

stopwords=GetFile("stopwords.txt")
listToSet(stopwords, "stopwords")
Document_A=GetFile("Document_A.txt")
Document_B=GetFile("Document_B.txt")
Document_C=GetFile("Document_C.txt")

listToSet(Document_A, "Document_A")
listToSet(Document_B, "Document_B")
listToSet(Document_C, "Document_C")


conn.sdiffstore("Document_A", "Document_A", "stopwords")
conn.sdiffstore("Document_B", "Document_B", "stopwords")
conn.sdiffstore("Document_C", "Document_C", "stopwords")

filteredData=conn.smembers("Document_A")
setToKeyword(filteredData, "Document_A")
filteredData=conn.smembers("Document_B")
setToKeyword(filteredData, "Document_B")
filteredData=conn.smembers("Document_C")
setToKeyword(filteredData, "Document_C")


while True:
    searchWord=input("Enter word you want to Search: ")
    output=conn.smembers(searchWord)
    if(len(output)==0):
        print("Word not found in any  of the file!")
    for output2 in output:
        print(output2)


    searchWord=input("Press any key to continue......")
    if input('Do You Want To Continue? [y/n] ') != 'y':
        break
    
    

    







