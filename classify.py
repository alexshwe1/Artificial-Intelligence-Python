"""
In this project, I implement a facial analysis program using 
Principal Component Analysis (PCA), using the skills 
learned from the linear algebra + PCA lectures.
"""

import os
import math

def load_training_data(vocab, directory):
    """ Create the list of dictionaries """
    top_level = os.listdir(directory)
    dataset = []
    for d in top_level:
        if d.startswith('.'):
            # ignore hidden files
            continue
        if d[-1] == '/':
            label = d[:-1]
            subdir = d
        else:
            label = d
            subdir = d+"/"
        files = os.listdir(directory+subdir)
        for f in files:
            bow = create_bow(vocab, directory+subdir+f)
            dataset.append({'label': label, 'bow': bow})
    return dataset

def create_vocabulary(directory, cutoff):
    """ Create a vocabulary from the training directory
        return a sorted vocabulary list
    """

    top_level = os.listdir(directory)
    vocab = {}
    for d in top_level:
        if d.startswith('.'):
            # ignore hidden files
            continue
        subdir = d if d[-1] == '/' else d+'/'
        files = os.listdir(directory+subdir)
        for f in files:
            with open(directory+subdir+f,'r') as doc:
                for word in doc:
                    word = word.strip()
                    if not word in vocab and len(word) > 0:
                        vocab[word] = 1
                    elif len(word) > 0:
                        vocab[word] += 1
    return sorted([word for word in vocab if vocab[word] >= cutoff])

def create_bow(vocab, filepath):
    """ Create a single dictionary for the data
        Note: label may be None
    """
    bow = {}
    # TODO: add your code here
    with open(filepath, "r") as f:
        file = f.read()
    
    words = file.split("\n")
    
    for word in words:
        if word in vocab:
            if word not in bow:
                bow[word] = 1
            else:
                bow[word] += 1
        else:
            if None not in bow:
                bow[None] = 1
            else:
                bow[None] += 1
                

    return bow

def prior(training_data, label_list):
    """ return the prior probability of the label in the training set
        => frequency of DOCUMENTS
    """

    smooth = 1 # smoothing factor
    logprob = {}
    # TODO: add your code here   
    
    numFiles = 0 # variable to count the total number of files in the training data
    
    for label in label_list:
        numLabels = 0
        for data in training_data:
            lbl = data['label']
            if (label == lbl):
                numLabels += 1 # if the label of the file currently on matches the label of the label in label list, increment
        logprob[label] = numLabels
        numFiles += numLabels
        
    for key in logprob:
        logprob[key] = math.log((logprob[key] + smooth) / (numFiles + 2))
            
    return logprob

def p_word_given_label(vocab, training_data, label):
    """ return the class conditional probability of label over all words, with smoothing """

    smooth = 1 # smoothing factor
    word_prob = {}
    # TODO: add your code here
    
    vocabSize = len(vocab)
    
    totalWordCount = 0
    
    data_match_list = []
    for data in training_data:
        if data["label"] == label:
            data_match_list.append(data)
            
    for match in data_match_list:
        bow = match["bow"]
        for word in bow:
            if word not in word_prob:
                word_prob[word] = bow[word]
            else:
                word_prob[word] += bow[word]
            totalWordCount += bow[word]
    
    for word in vocab:
        if word not in word_prob:
            word_prob[word] = 0
            
    if None not in word_prob:
        word_prob[None] = 0
    
    for key in word_prob:
        word_prob[key] = math.log((word_prob[key] + smooth * 1) / (totalWordCount + smooth * (vocabSize + 1)))

    return word_prob

def train(training_directory, cutoff):
    """ return a dictionary formatted as follows:
            {
             'vocabulary': <the training set vocabulary>,
             'log prior': <the output of prior()>,
             'log p(w|y=2016)': <the output of p_word_given_label() for 2016>,
             'log p(w|y=2020)': <the output of p_word_given_label() for 2020>
            }
    """
    retval = {}
    label_list = [f for f in os.listdir(training_directory) if not f.startswith('.')] # ignore hidden files
    # TODO: add your code here

    vocab = create_vocabulary(training_directory, cutoff)
    td = load_training_data(vocab, training_directory)
    logPrior = prior(td, label_list)
    
    for label in label_list:
        retval["log p(w|y=" + label + ")"] = p_word_given_label(vocab, td, label)
    
    retval["log prior"] = logPrior
    retval["vocabulary"] = vocab
    
    return retval

def classify(model, filepath):
    """ return a dictionary formatted as follows:
            {
             'predicted y': <'2016' or '2020'>,
             'log p(y=2016|x)': <log probability of 2016 label for the document>,
             'log p(y=2020|x)': <log probability of 2020 label for the document>
            }
    """
    retval = {}
    # TODO: add your code here
    
    trainingVocab = model["vocabulary"]
    bow = create_bow(trainingVocab, filepath)
    
    label_list = os.listdir(filepath[:filepath.find("2")])
    for label in label_list:
        if label[0] == ".":
            label_list.remove(label)
            
    for label in label_list:
        tot_prob = 0
        curr_log_prob = model["log p(w|y=" + label + ")"]
        for word in bow:
            tot_prob += curr_log_prob[word] * bow[word]
        retval["log p(y=" + label + "|x)"] = model["log prior"][label] + tot_prob
        
    predictedYear = max(retval, key = retval.get)
    retval['predicted y'] = predictedYear[predictedYear.find("=") +1:predictedYear.find("|")]

    return retval
