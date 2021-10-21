import csv
import numpy as np
import matplotlib.pyplot as plt
import math

def load_data(filepath):
    pokemon = []
    with open(filepath, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        integer_keys = ["HP", "Attack", "Total", "Defense", "Sp. Def", "Sp. Atk", "Speed", "#"]
        for row in reader:
            current_dictionary = {}
            for key in row:
                if key == "Legendary" or key == "Generation":
                    continue
                elif key in integer_keys:
                    current_dictionary[key] = int(row[key])
                else:
                    current_dictionary[key] = row[key]
            pokemon.append(current_dictionary)
    return pokemon[:20]


def calculate_x_y(stats):
    return (stats["Attack"] + stats["Sp. Atk"] + stats["Speed"], stats["Defense"] + stats["Sp. Def"] + stats["HP"])

def get_distance(tuple1, tuple2):
    tuple1_x = tuple1[0]
    tuple1_y = tuple1[1]
    tuple2_x = tuple2[0]
    tuple2_y = tuple2[1]
    return math.sqrt((tuple2_x - tuple1_x)**2 + (tuple2_y - tuple1_y)**2)

def hac(dataset):
    for index in range(len(dataset)):
        tupel = dataset[index]
        if not math.isfinite(tupel[0]) or not math.isfinite(tupel[1]):
            dataset.pop(index)

    cluster_count = len(dataset) - 1
    cluster_dictionary = {}
    matrix = []
    #cluster count = 19
    while len(matrix) < len(dataset) - 1:
        minimum_distance = 10000000000000000000
        minimum_1 = None
        minimum_2 = None
        
        #once minimum distance between two tuples is found, check if either of those tuples are in cluster dictionary
        for i in range(len(dataset)):
            for j in range(len(dataset)):
                if i == j:
                    continue
                tup1 = dataset[i]
                tup2 = dataset[j]
                distance = get_distance(tup1, tup2)
                if distance < minimum_distance:
                    flag = False
                    if len(cluster_dictionary) == 0:
                        minimum_distance = distance
                        minimum_1 = tup1
                        minimum_2 = tup2
                    else:
                        for c in cluster_dictionary:
                            cluster_list = cluster_dictionary[c]
                            if tup1 in cluster_list and tup2 in cluster_list:
                                flag = True
                        if not flag:
                            minimum_distance = distance
                            minimum_1 = tup1
                            minimum_2 = tup2
                                       
        pair = list(cluster_dictionary.values())
       
        flattened_pair = []
        for p in pair:
            flattened_pair += p
       
        #if tuple 1 and tuple 2 are BOTH NOT in cluster dictionary AND tuple 1 and tuple 2 not in tuples_already_paired
            #increment cluster count
            #add tuple 1 and tuple 2 to cluster dictionary with cluster count being key
            #add list to matrix with index of cluster 1, index of cluster 2, distance between cluster 1 and cluster 2, 2 for size
        if minimum_1 not in flattened_pair and minimum_2 not in flattened_pair:
            cluster_count += 1
            cluster_dictionary[cluster_count] = [minimum_1, minimum_2]
            low = min(dataset.index(minimum_1), dataset.index(minimum_2))
            high = max(dataset.index(minimum_1), dataset.index(minimum_2)) 
            matrix.append([low, high, minimum_distance, 2])
            
        #else if tuple 1 IS NOT IN cluster dictionary AND tuple 2 IS IN cluster dictionary AND tuple 1 and tuple 2 not in tuples_already_paired
            #increment cluster count
            #add cluster 1 and cluster 2 to tuples_already_paired
            #combine tuple 1 and tuple 2's clusters in cluster dictionary to new list in cluster dictionary with key being cluster count
            #add list to matrix with tuple 1, index of tuple 2's cluster dictionary key, distance between tuple 1 and tuple 2, size of tuple 2's cluster dictionary + 1
        elif minimum_1 not in flattened_pair and minimum_2 in flattened_pair:
            cluster_count += 1
            newest_cluster_n = 0
            key = 0
            for i in cluster_dictionary:
                tupels = cluster_dictionary[i]
                if minimum_2 in tupels and len(tupels) >= newest_cluster_n:
                    newest_cluster_n = len(tupels)
                    key = i
           
            new = cluster_dictionary[key]
            new.append(minimum_1)
            cluster_dictionary[cluster_count] = new
            low = min(dataset.index(minimum_1), key)
            high = max(dataset.index(minimum_1), key)          
            matrix.append([low, high, minimum_distance, len(new)])
        
        #else if tuple 1 IS IN cluster dictionary AND tuple 2 IS NOT IN cluster dictionary AND tuple 1 and tuple 2 not in tuples_already_paired
            #increment cluster count
            #add cluster 1 and cluster 2 to tuples_already_paired
            #combine tuple 1's clusters in cluster dictionary and tuple 2 to new list in cluster dictionary with key being cluster count
            #add list to matrix with tuple 1's cluster dictionary key, index of tuple 2, distance between tuple 1 and tuple 2, size of tuple 1's cluster dictionary + 1
        elif minimum_1 in flattened_pair and minimum_2 not in flattened_pair:
            cluster_count += 1
            newest_cluster_n = 0
            key = 0
            for i in cluster_dictionary:
                tupels = cluster_dictionary[i]
                if minimum_1 in tupels and len(tupels) >= newest_cluster_n:
                    newest_cluster_n = len(tupels)
                    key = i
                   
            new = cluster_dictionary[key]
            new.append(minimum_2)
            cluster_dictionary[cluster_count] = new
            low = min(key, dataset.index(minimum_2))
            high = max(key, dataset.index(minimum_2))
            matrix.append([low, high, minimum_distance, len(new)])
        
        #else (tuple 1 AND tuple 2 are in cluster dictionary)
            #increment cluster count
            #compare all values of tuple 1's AND tuple 2's cluster dictionary to find minimum value
            #combine tuple 1's clusters in cluster dictionary and tuple 2's clusters in cluster dictionary to new list in cluster dictionary with key being cluster count
            #add list to matrix with index of tuple 1's cluster dictionary key, index of tuple 2's cluster dictionary key, distance between tuple 1 and tuple 2, size of tuple 1's cluster dictionary and tuple 2's cluster dictionary
        else:
            cluster_count += 1
            newest_cluster_n1 = 0
            key1 = 0
            newest_cluster_n2 = 0
            key2 = 0
            for i in cluster_dictionary:
                tupels = cluster_dictionary[i]
                if minimum_1 in tupels and len(tupels) >= newest_cluster_n1:
                    newest_cluster_n1 = len(tupels)
                    key1 = i
            for i in cluster_dictionary:
                tupels = cluster_dictionary[i]
                if minimum_2 in tupels and len(tupels) >= newest_cluster_n2:
                    newest_cluster_n2 = len(tupels)
                    key2 = i
            new = cluster_dictionary[key1] + cluster_dictionary[key2]
            cluster_dictionary[cluster_count] = new
            low = min(key1, key2)
            high = max(key1, key2)    
            matrix.append([low, high, minimum_distance, len(new)])
       
    return matrix

def random_x_y(m):
    return_pokemon = []
    for integer in range(m):
        x = np.random.randint(1, 360)
        y = np.random.randint(1, 360)
        return_pokemon.append([x, y])
    return return_pokemon

def imshow_hac(dataset):
    for index in range(len(dataset)):
        tupel = dataset[index]
        if not math.isfinite(tupel[0]) or not math.isfinite(tupel[1]):
            dataset.pop(index)

    cluster_count = len(dataset) - 1
    cluster_dictionary = {}
    matrix = []
    #cluster count = 19
    while len(matrix) < len(dataset) - 1:
        minimum_distance = 10000000000000000000
        minimum_1 = None
        minimum_2 = None
        
        #once minimum distance between two tuples is found, check if either of those tuples are in cluster dictionary
        for i in range(len(dataset)):
            for j in range(len(dataset)):
                if i == j:
                    continue
                tup1 = dataset[i]
                tup2 = dataset[j]
                distance = get_distance(tup1, tup2)
                if distance < minimum_distance:
                    flag = False
                    if len(cluster_dictionary) == 0:
                        minimum_distance = distance
                        minimum_1 = tup1
                        minimum_2 = tup2
                    else:
                        for c in cluster_dictionary:
                            cluster_list = cluster_dictionary[c]
                            if tup1 in cluster_list and tup2 in cluster_list:
                                flag = True
                        if not flag:
                            minimum_distance = distance
                            minimum_1 = tup1
                            minimum_2 = tup2
                                       
        pair = list(cluster_dictionary.values())
       
        flattened_pair = []
        for p in pair:
            flattened_pair += p
       
        #if tuple 1 and tuple 2 are BOTH NOT in cluster dictionary AND tuple 1 and tuple 2 not in tuples_already_paired
            #increment cluster count
            #add tuple 1 and tuple 2 to cluster dictionary with cluster count being key
            #add list to matrix with index of cluster 1, index of cluster 2, distance between cluster 1 and cluster 2, 2 for size
        if minimum_1 not in flattened_pair and minimum_2 not in flattened_pair:
            cluster_count += 1
            cluster_dictionary[cluster_count] = [minimum_1, minimum_2]
            low = min(dataset.index(minimum_1), dataset.index(minimum_2))
            high = max(dataset.index(minimum_1), dataset.index(minimum_2)) 
            matrix.append([minimum_1, minimum_2])
            
        #else if tuple 1 IS NOT IN cluster dictionary AND tuple 2 IS IN cluster dictionary AND tuple 1 and tuple 2 not in tuples_already_paired
            #increment cluster count
            #add cluster 1 and cluster 2 to tuples_already_paired
            #combine tuple 1 and tuple 2's clusters in cluster dictionary to new list in cluster dictionary with key being cluster count
            #add list to matrix with tuple 1, index of tuple 2's cluster dictionary key, distance between tuple 1 and tuple 2, size of tuple 2's cluster dictionary + 1
        elif minimum_1 not in flattened_pair and minimum_2 in flattened_pair:
            cluster_count += 1
            newest_cluster_n = 0
            key = 0
            for i in cluster_dictionary:
                tupels = cluster_dictionary[i]
                if minimum_2 in tupels and len(tupels) >= newest_cluster_n:
                    newest_cluster_n = len(tupels)
                    key = i
           
            new = cluster_dictionary[key]
            new.append(minimum_1)
            cluster_dictionary[cluster_count] = new
            low = min(dataset.index(minimum_1), key)
            high = max(dataset.index(minimum_1), key)          
            matrix.append([minimum_1, minimum_2])
        
        #else if tuple 1 IS IN cluster dictionary AND tuple 2 IS NOT IN cluster dictionary AND tuple 1 and tuple 2 not in tuples_already_paired
            #increment cluster count
            #add cluster 1 and cluster 2 to tuples_already_paired
            #combine tuple 1's clusters in cluster dictionary and tuple 2 to new list in cluster dictionary with key being cluster count
            #add list to matrix with tuple 1's cluster dictionary key, index of tuple 2, distance between tuple 1 and tuple 2, size of tuple 1's cluster dictionary + 1
        elif minimum_1 in flattened_pair and minimum_2 not in flattened_pair:
            cluster_count += 1
            newest_cluster_n = 0
            key = 0
            for i in cluster_dictionary:
                tupels = cluster_dictionary[i]
                if minimum_1 in tupels and len(tupels) >= newest_cluster_n:
                    newest_cluster_n = len(tupels)
                    key = i
                   
            new = cluster_dictionary[key]
            new.append(minimum_2)
            cluster_dictionary[cluster_count] = new
            low = min(key, dataset.index(minimum_2))
            high = max(key, dataset.index(minimum_2))
            matrix.append([minimum_1, minimum_2])
        
        #else (tuple 1 AND tuple 2 are in cluster dictionary)
            #increment cluster count
            #compare all values of tuple 1's AND tuple 2's cluster dictionary to find minimum value
            #combine tuple 1's clusters in cluster dictionary and tuple 2's clusters in cluster dictionary to new list in cluster dictionary with key being cluster count
            #add list to matrix with index of tuple 1's cluster dictionary key, index of tuple 2's cluster dictionary key, distance between tuple 1 and tuple 2, size of tuple 1's cluster dictionary and tuple 2's cluster dictionary
        else:
            cluster_count += 1
            newest_cluster_n1 = 0
            key1 = 0
            newest_cluster_n2 = 0
            key2 = 0
            for i in cluster_dictionary:
                tupels = cluster_dictionary[i]
                if minimum_1 in tupels and len(tupels) >= newest_cluster_n1:
                    newest_cluster_n1 = len(tupels)
                    key1 = i
            for i in cluster_dictionary:
                tupels = cluster_dictionary[i]
                if minimum_2 in tupels and len(tupels) >= newest_cluster_n2:
                    newest_cluster_n2 = len(tupels)
                    key2 = i
            new = cluster_dictionary[key1] + cluster_dictionary[key2]
            cluster_dictionary[cluster_count] = new
            low = min(key1, key2)
            high = max(key1, key2)    
            matrix.append([minimum_1, minimum_2])
            
    pts = map(list, zip(*dataset))
    pts = list(pts)
    for x, y in zip(pts[0], pts[1]):
        plt.scatter(x, y)
    for ln in matrix:
        sg = map(list, zip(*ln))
        sg = list(sg)
        plt.plot(sg[0], sg[1])
        plt.pause(0.1)
    plt.show()