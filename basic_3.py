import os
import sys
import psutil
import time



acgt_index = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
ALPHA = [[0, 110, 48, 94],
         [110, 0, 118, 48],
         [48, 118, 0, 110],
         [94, 48, 110, 0]]


DELTA = 30


def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = float(memory_info.rss/1024.0)
    return memory_consumed


def string_insert(basic_string, insert_pos):
    string_start = basic_string[:insert_pos + 1]
    string_end = basic_string[insert_pos + 1:]
    return string_start + basic_string + string_end


def createInputStrings(inputFilePath):
    memoryBefore = process_memory()
    temp_string = ""
    with open(inputFilePath, "r") as f:
        first_string = f.readline().rstrip()
        while True:
            temp_string = f.readline().rstrip()
            if temp_string.isdigit():
                first_string = string_insert(first_string, int(temp_string))
            else:
                break

        second_string = temp_string
        while True:
            temp_string = f.readline().rstrip()
            if temp_string.isdigit():
                second_string = string_insert(second_string, int(temp_string))
            else:
                break

    memoryAfter = process_memory()
    return first_string, second_string, memoryAfter-memoryBefore


def alignStrings(stringA, stringB):
    memoryBefore = process_memory()
    alignedStringA = ""
    alignedStringB = ""

    lenA = len(stringA) + 1
    lenB = len(stringB) + 1

    dp = []
    for i in range(lenB):
        inner = [0] * lenA
        dp.append(inner)

    for i in range(lenB):
        dp[i][0] = i * DELTA

    for j in range(lenA):
        dp[0][j] = j * DELTA

    for i in range(1, lenB):
        for j in range(1, lenA):
            cost_x_y = dp[i - 1][j - 1] + ALPHA[acgt_index.get(stringA[j - 1])][acgt_index.get(stringB[i - 1])]
            cost_x_not = dp[i - 1][j] + DELTA
            cost_y_not = dp[i][j - 1] + DELTA
            dp[i][j] = min(cost_x_not, min(cost_y_not, cost_x_y))


    i = lenB - 1
    j = lenA - 1
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + ALPHA[acgt_index.get(stringA[j - 1])][acgt_index.get(stringB[i - 1])]:
            alignedStringA = stringA[j - 1] + alignedStringA
            alignedStringB = stringB[i - 1] + alignedStringB
            i = i - 1
            j = j - 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + DELTA:
            alignedStringA = "_" + alignedStringA
            alignedStringB = stringB[i - 1] + alignedStringB
            i = i - 1
        else:
            alignedStringA = stringA[j - 1] + alignedStringA
            alignedStringB = "_" + alignedStringB
            j = j - 1
    memoryAfter = process_memory()
    return alignedStringA, alignedStringB, memoryAfter-memoryBefore


def calcScore(stringA, stringB):
    lent = len(stringA)
    score = 0
    for i in range(lent):
        if stringA[i] == '_' or stringB[i] == '_':
            score += DELTA
        elif stringA[i] == stringB[i]:
            score += 0
        else:
            score += ALPHA[acgt_index.get(stringA[i])][acgt_index.get(stringB[i])]
    return score


def call_algorithm(inputFile):
    inputStringA, inputStringB, A = createInputStrings(os.path.join(os.getcwd(),inputFile))
    basicAlignedA, basicAlignedB, B = alignStrings(inputStringA, inputStringB)

    return basicAlignedA, basicAlignedB, A + B


def time_wrapper(inputFile):
    start_time = time.time()
    basicAlignedA, basicAlignedB, memeroy = call_algorithm(inputFile)
    end_time = time.time()
    time_taken = (end_time - start_time)*1000
    return time_taken, basicAlignedA, basicAlignedB, memeroy


def basicProcess():
    
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]



    timeTakenBasic, basicAlignedA, basicAlignedB, memeroy = time_wrapper(inputFile)
  
    with open(os.path.join(os.getcwd(), outputFile), 'w') as output:
        output.write(str(calcScore(basicAlignedA, basicAlignedB))+"\n")   
        output.write(basicAlignedA +"\n")  
        output.write(basicAlignedB+"\n")   
        output.write(str(timeTakenBasic)+"\n")   
        output.write(str(memeroy)+"\n")   

    
if __name__ == "__main__":
    basicProcess()
