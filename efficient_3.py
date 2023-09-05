import sys
import os
import time
import psutil

ALPHA = [[0, 110, 48, 94], [110, 0, 118, 48],
                [48, 118, 0, 110], [94, 48, 110, 0]]

DELTA = 30



acgt_index = {'A': 0, 'C': 1, 'G': 2, 'T': 3}

def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = float(memory_info.rss/1024.0)
    return memory_consumed

def alignStrings(stringA, stringB):
    
    
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
    
    
    return alignedStringA,alignedStringB


def sequence_alignment(stringA, stringB):
    m, n = len(stringA), len(stringB)
    if m > 1 and n > 1:
        
        opt1 = space_efficient(stringA[:m//2], stringB)
        opt2 = space_efficient(stringA[m//2:][::-1], stringB[::-1])[::-1]
        min1 = float('inf')
        index_k = -1
        for i in range(n + 1):
            if min1 > opt1[i] + opt2[i]:
                min1, index_k = opt1[i] + opt2[i], i

        
        opt1_A, opt1_B = sequence_alignment(stringA[:m//2], stringB[:index_k])
        opt2_A, opt2_B = sequence_alignment(stringA[m//2:], stringB[index_k:])
        return opt1_A + opt2_A, opt1_B + opt2_B
    else:
        return alignStrings(stringA, stringB)




def space_efficient(stringA, stringB):
 
    efficient_dp = [[0] * 2 for dp_i in range(len(stringB)+1)]

    
    for j in range(len(stringB)+1):
        efficient_dp[j][0] = j * DELTA

    
    for i in range(1, len(stringA)+1):
        efficient_dp[0][1] = efficient_dp[0][0] + DELTA
        for j in range(1, len(stringB) + 1):
            efficient_dp[j][1] = min(
                efficient_dp[j-1][1] + DELTA,
                efficient_dp[j][0] + DELTA,
                ALPHA[acgt_index.get(stringA[i - 1])][acgt_index.get(stringB[j - 1])]+ efficient_dp[j-1][0]
            )

        for j in range(len(stringB)+1):
            efficient_dp[j][0] = efficient_dp[j][1]

    return [dp_i[0] for dp_i in efficient_dp]



def generate(starting, multipliers):

    output = starting
    for multiplier in multipliers:        
        splitIndex = int(multiplier) + 1
        output = output[:splitIndex] + output + output[splitIndex:]
    return output



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

if __name__ == '__main__':
    
    inputfile = sys.argv[1]
    outputFile = sys.argv[2]
    #inputfile = "in15.txt"
    #outputFile = "out15.txt"

    with open(inputfile) as f:
        inputLine = [line.strip('\n') for line in list(f)]

    first = []
    second = []
    for i in range(1, len(inputLine)):
        if not inputLine[i].isnumeric():
            first = inputLine[:i]
            second = inputLine[i:]

    stringA = generate(first[0], first[1:])
    stringB = generate(second[0], second[1:])



    start_time = time.time()
    memoryBefore = process_memory()
    str1,str2=sequence_alignment(stringA, stringB)
    memoryAfter = process_memory()
    end_time = time.time()
    time_taken = (end_time - start_time)*1000
    memory=memoryAfter-memoryBefore
    

    with open(os.path.join(os.getcwd(), outputFile), 'w') as output:
        output.write(str(calcScore(str1, str2))+"\n")    
        output.write(str1 +"\n") 
        output.write(str2+"\n")   
        output.write(str(time_taken)+"\n")   
        output.write(str(memory)+"\n")   



 