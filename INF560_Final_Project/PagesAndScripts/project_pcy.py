# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 16:52:57 2016

@author: Mounik Muralidhara

This programe determines the frequent paths, stores, dead-zones using PCY
algorithm.

"""
import sys
import re
import itertools
import time
import csv
from PIL import Image, ImageDraw, ImageFont

        
def GenerateAllHashTables(omniList, tableOrderNumber, bucketSize):
    # Generates all the hash tables at each pass
    hashTableList = []
    for elementList in omniList:
        dictHashTable = {}
        for singleList in elementList:
            sumItems = 0
            for item in singleList:
                sumItems += ord(item)
            modValue = sumItems%bucketSize
            dictHashTable[modValue]= dictHashTable.get(modValue,0)+1
        hashTableList.append(dictHashTable)
    print(hashTableList[tableOrderNumber])
        
def GenerateOmniList(inputData,tableOrderNumber):
    # Generates the combination of all stores from the frquent item-sets
    omniList = [[] for i in range(tableOrderNumber+1)]
    combinationList = []

    for line in inputData:
        line = re.findall('\w',line)
        lines = sorted(line)
        
        for ind in xrange(1,len(lines)+1):
            combo = [list(x) for x in itertools.combinations(lines, ind)]
            combinationList.extend(combo)    
    for ind1 in range (len(omniList)):
        for item in combinationList:
            if(ind1 == len(item)):
                omniList[ind1].append(item)
    return omniList   
    

def GenerateFutureFrequentItems(lstFrequentItemSets, maxPossibleElements, lstInputData, inputData, support, bucketSize):
    # Generation of frequent paths of order more than 2
    lstFreqItems = []
    lstFreqItems = lstFrequentItemSets
    lstDupFreqItems = []
    omniList = []
    omniList = GenerateOmniList(inputData,maxPossibleElements)
    dictCountItemSets = {}
    while(len(lstFreqItems)>0):
        for i in range(maxPossibleElements):
            for pairInd1 in range(len(lstFreqItems)):
                for pairInd2 in range(pairInd1+1, len(lstFreqItems)):
                    setA = set(lstFreqItems[pairInd1]+lstFreqItems[pairInd2])
                    sortedList = sorted(list(setA))
                    if(len(sortedList) == len(lstFreqItems[pairInd1])+1):
                        count =0
                        for sinTrans in lstInputData:
                            if(set(sortedList).issubset(set(sinTrans))):
                                count += 1                        
                        dictCountItemSets[tuple(sortedList)] = count
        
        lstFreqItems = []
        for item in dictCountItemSets:
            if(dictCountItemSets[item]>=support):
                lstFreqItems.append(list(item))
        dictCountItemSets.clear()
        lstElementCount = []
        if(len(lstFreqItems) > 0):
            for index in range(len(lstFreqItems)):
                lstElementCount.append(len(lstFreqItems[index]))
            GenerateAllHashTables(omniList,max(lstElementCount),bucketSize)
            print(sorted(lstFreqItems))
            lstDupFreqItems = sorted(lstFreqItems)
    return(lstDupFreqItems)
            
        

def ExecuteSecondPass(inputData,lstSingleFrequentItems, dictPairs, support, bucketSize):
    
    # Form pairs from the frequent itemsets generated from the first pass
    
    dictPossibleCandidatePairs = {}
    lstFrequentPairs = []
    lstLengthOfEachTrasaction= []
    lstInputData= []
    
    for line in inputData:
        line = re.findall('\w',line)
        lines = sorted(line)
        lstLengthOfEachTrasaction.append(len(lines))
        lstInputData.append(lines)
        
        for ind1 in range(len(lines)):
            for ind2 in range(ind1+1, len(lines)):
                lstDoublePair = []
                lstDoublePair.append(lines[ind1])
                lstDoublePair.append(lines[ind2])
                count= 0
                for item in lstDoublePair:
                    if item in lstSingleFrequentItems:
                        count += 1
                if(count== 2):
                    mod1Value = (ord(lines[ind1])+ord(lines[ind2]))%bucketSize
                    if(dictPairs[mod1Value] !=0):
                        dictPossibleCandidatePairs[tuple(lstDoublePair)] =dictPossibleCandidatePairs.get(tuple(lstDoublePair),0)+1
    
    
    for item in dictPossibleCandidatePairs:
        if(dictPossibleCandidatePairs[item] >= support):
            lstFrequentPairs.append(list(item))
    print(sorted(lstFrequentPairs))
    inputData.close()
    inputData=open(sys.argv[1])
    lstFinalList = []
    lstFinalList = GenerateFutureFrequentItems(lstFrequentPairs, max(lstLengthOfEachTrasaction), lstInputData, inputData, support, bucketSize)
    return lstFinalList    
 

def ExecuteFirstPass(inputData, support, bucketSize):
    #Determination of Frequent Pairs
    lstSingleCandidates= []
    dictItemCount = {}
    hashTableDict = {}
    for line in inputData:
        line = re.findall('\w+', line)
        lines= sorted(line)
        for item in lines:
            dictItemCount[item] = dictItemCount.get(item,0)+1
        # Hashing Technique
        for index in range(len(lines)):
            for ind in range(index+1, len(lines)):
                modValue = (ord(lines[index])+ord(lines[ind]))%bucketSize
                hashTableDict[modValue] = hashTableDict.get(modValue,0)+1

    for element in dictItemCount:
        if(dictItemCount[element] >= support):
            lstSingleCandidates.append(element)
    print(dictItemCount)
    print(sorted(lstSingleCandidates))
    print(hashTableDict)
    #Replacing the values of the dictionary by bit maps
    for element in hashTableDict:
        if(hashTableDict[element]>= support):
            hashTableDict[element]=1
        else:
            hashTableDict[element]=0
    return sorted(lstSingleCandidates), hashTableDict, dictItemCount


if __name__ == '__main__':
    startTime = time.time()
    timestr = time.strftime("%Y%m%d-%H%M%S")
    #Records all the printed output to a text file
    sys.stdout = open("pcy_log_"+timestr+".txt", "w")
    inputData=open(sys.argv[1])
    support = int(sys.argv[2])
    bucketSize = int(sys.argv[3])
    print("Support Count: "+str(support))
    print("Bucket Size: "+str(bucketSize))
    frequentItemList = []
    hashTableDict = {}
    singleItemDict = {}
    #Determination Of Frequent Pairs
    frequentItemList, hashTableDict, singleItemDict=ExecuteFirstPass(inputData, support, bucketSize)
    inputData.close()
    inputData= open(sys.argv[1])
    # Determination of Frequent Paths
    lstFinalList = []
    lstFinalList = ExecuteSecondPass(inputData,frequentItemList, hashTableDict, support, bucketSize)
    lstConvertList = []
    for  item in lstFinalList:
        for element in item:
            lstConvertList.append(element)
    
    all_items_frequentset = set(lstConvertList) # Determines frequent stores from Frequent Paths
    
    allItemsList = []
    for key in singleItemDict:
        allItemsList.append(key)

    all_items_set = set(allItemsList)
    print("Frequent Paths:")
    print(lstFinalList)
    print("Frequent Stores:")
    frequentStoresList = []
    frequentStoresList = list(list(all_items_frequentset))
    print(frequentStoresList)
    frequentStoreDict = {}
    for store in frequentStoresList:
        for entry in singleItemDict:
            if(entry == store):
                frequentStoreDict[store] = singleItemDict[entry]
    print(frequentStoreDict)
    print("Non-Frequent Stores:")
    deadZonesList = []
    deadZonesList = list(all_items_set-all_items_frequentset)
    print(deadZonesList)
    deadZoneStoreDict = {}
    for store in deadZonesList:
        for entry in singleItemDict:
            if(entry == store):
                deadZoneStoreDict[store]= singleItemDict[entry]
    print(deadZoneStoreDict)
    sortedSingleItemList = []
    sortedSingleItemList = sorted(singleItemDict.items(), key= lambda t:t[1], reverse = True)
    
    # Ranking Algorithm
    frequentDictOrder = {}
    deadDictOrder = {}
    freqRank = 0
    deadRank = 0
    # Determination of frequent stores rank
    for tuples in sortedSingleItemList:
        for item in frequentStoresList:
            if(tuples[0] == item):
                freqRank += 1
                frequentDictOrder[tuples[0]] = freqRank
    sortedSingleItemListAsc = sorted(singleItemDict.items(), key= lambda t:t[1])
    # Determination of Least visited stores rank
    for tuples in sortedSingleItemListAsc:
        for element in deadZonesList:
            if(tuples[0] == element):
                deadRank += 1
                deadDictOrder[tuples[0]] = deadRank
    print("Ranking of Least Visited Store:")
    print("*******************************************************")
    print("Store\tRank")
    print("*******************************************************")
    sortedDeadList = sorted(deadDictOrder.items(), key= lambda t:t[1])
    for tuples in sortedDeadList:
        print(tuples[0]+"\t"+str(tuples[1]))
    print("Ranking of Most Visited Store:")
    print("*******************************************************") 
    print("Store\tRank")
    print("*******************************************************")
    sortedFrequentList = sorted(frequentDictOrder.items(), key=lambda t:t[1])
    for tuples in sortedFrequentList:
        print(tuples[0]+"\t"+str(tuples[1]))
        
    # Optimal Location Strategy Algorithm
    lstOptimizedPlacing = []
    lstDeadStores= []
    if(len(sortedFrequentList)>len(sortedDeadList)):
        for indA in range(len(sortedDeadList)/2):
            lstTempPos= []
            lstTempPos.append(sortedDeadList[indA][0])
            lstDeadStores.append(sortedDeadList[indA][0])
            lstTempPos.append(sortedFrequentList[indA][0])            
            lstOptimizedPlacing.append(lstTempPos)
    elif(len(sortedFrequentList)<=len(sortedDeadList)):
        for indB in range(len(sortedFrequentList)/2):
            lstTempPos = []
            lstTempPos.append(sortedDeadList[indB][0])
            lstDeadStores.append(sortedDeadList[indB][0])
            lstTempPos.append(sortedFrequentList[indB][0])
            lstOptimizedPlacing.append(lstTempPos)
    print("*********************************************************")
    print("Optimal Location Strategy")
    print("*********************************************************\n")
    print("DeadZone\tBenificialLocation")
    for item in lstOptimizedPlacing:
        print(item[0]+"\t\t"+item[1])
    
    # Write the stats of the store, frequent store, non-frequent store, frequent paths to a csv file
    writer = csv.writer(open('store_stats.csv', 'wb'))
    writer.writerow(['Store', 'Count'])
    for key, value in singleItemDict.items():
        writer.writerow([key, value])
        
    writer1 = csv.writer(open('freq_stats.csv', 'wb'))
    writer1.writerow(['Store', 'Count'])
    for key, value in frequentStoreDict.items():
        writer1.writerow([key, value])
    
    writer2 = csv.writer(open('nonfreq_stats.csv', 'wb'))
    writer2.writerow(['Store', 'Count'])
    for key, value in deadZoneStoreDict.items():
        writer2.writerow([key, value])
    
    with open('frequent_paths.csv', 'wb') as f:
        writer3 = csv.writer(f)
        writer3.writerows(lstFinalList)
    
    with open('map_pos.csv', 'rb') as f:
        reader = csv.reader(f)
        next(reader, None)
        positionList = []
        for row in reader:
            positionList.append(row)
    
    # Plotting the positions of Dead Stores, Frequent Stores, Non-Frequent Stores, Optimal Location Strategy On Map
    lstFreqCoordinates = []  
    r = 15.0      
    for store in frequentStoresList:
        for item in positionList:
            if(item[0].lower() == store):
                lstTempCoordinates = []
                lstTempCoordinates.append(float(item[1])-r)
                lstTempCoordinates.append(float(item[2])-r)
                lstTempCoordinates.append(float(item[1])+r)
                lstTempCoordinates.append(float(item[2])+r)
                lstFreqCoordinates.append(tuple(lstTempCoordinates))
    
    # Plotting the frequent store on the map
    image_fileName = "store_map.png"
    propImage = Image.open(image_fileName)
    draw = ImageDraw.Draw(propImage)
    for entry in lstFreqCoordinates:
        draw.ellipse(entry, fill ='blue', outline='black')
    propImage.save("freq_store_map.png", "PNG")
    
    lstNonFreqCoordinates = []
    for store in deadZonesList:
        for item in positionList:
            if(item[0].lower() == store):
                lstTempCoordinates = []
                lstTempCoordinates.append(float(item[1])-r)
                lstTempCoordinates.append(float(item[2])-r)
                lstTempCoordinates.append(float(item[1])+r)
                lstTempCoordinates.append(float(item[2])+r)
                lstNonFreqCoordinates.append(tuple(lstTempCoordinates))
    
    # Plotting the non frequent store on the map
    image_fileName = "store_map.png"
    propImage = Image.open(image_fileName)
    draw = ImageDraw.Draw(propImage)
    for entry in lstNonFreqCoordinates:
        draw.ellipse(entry, fill ='green', outline='black')
    propImage.save("non_freq_store_map.png", "PNG")
    
    lstDeadStoresCoordinates = []
    for store in lstDeadStores:
        for item in positionList:
            if(item[0].lower() == store):
                lstTempCoordinates = []
                lstTempCoordinates.append(float(item[1])-r)
                lstTempCoordinates.append(float(item[2])-r)
                lstTempCoordinates.append(float(item[1])+r)
                lstTempCoordinates.append(float(item[2])+r)
                lstDeadStoresCoordinates.append(tuple(lstTempCoordinates))
                
    # Plotting the dead-zones store on the map
    image_fileName = "store_map.png"
    propImage = Image.open(image_fileName)
    draw = ImageDraw.Draw(propImage)
    for entry in lstDeadStoresCoordinates:
        draw.ellipse(entry, fill ='red', outline='black')
    propImage.save("dead_zone_store_map.png", "PNG")
    
    r1 = 30.0
    lstOptimalLocationStoreText = []
    lstOptimalCoordinates = []
    for stores in lstOptimizedPlacing:
        for item in positionList:
            if(item[0].lower() == stores[1]):
                tmpOptimalList = []
                tmpOptimalListString = []
                tmpOptimalList.append(float(item[1])-5.0)
                tmpOptimalList.append(float(item[2])+3.0)
                tmpOptimalListString.append(str(stores[0]))
                tmpOptimalListString.append(tuple(tmpOptimalList))
                lstOptimalLocationStoreText.append(tmpOptimalListString)
                lstTempCoordinates = []
                lstTempCoordinates.append(float(item[1])-r1)
                lstTempCoordinates.append(float(item[2])-r1)
                lstTempCoordinates.append(float(item[1])+r1)
                lstTempCoordinates.append(float(item[2])+r1)
                lstOptimalCoordinates.append(tuple(lstTempCoordinates))
    
    # Plotting the optimal locations on the map
    image_fileName = "store_map.png"
    propImage = Image.open(image_fileName)
    draw = ImageDraw.Draw(propImage)
    for entry in lstOptimalCoordinates:
        draw.ellipse(entry, fill ='green', outline='black')
    for entry in lstOptimalLocationStoreText:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 30)
        draw.text(entry[1], entry[0].upper(),fill='black',font = font)
    propImage.save("optimal_location_store_map.png", "PNG")
    endTime = time.time()
    print("Total Time taken to execute: "+str(endTime-startTime)+"s")
    