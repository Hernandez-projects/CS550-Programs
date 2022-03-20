# Might make your life easier for appending to lists
from collections import defaultdict
import datetime
# Third party libraries
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, Input
from sklearn.model_selection import train_test_split
# Only needed if you plot your confusion matrix
import matplotlib.pyplot as plt

# our libraries
from lib.partition import split_by_day
import lib.file_utilities as util
import lib.buildmodels as mod

"""
Single programmer AFFIDAVIT:
I promise that the attached assignment is my own work.
I recognize that should this not be the case,
I will be subject to penalties as outlined in the course syllabus. Jesse Hernandez
"""


# Any other modules you create


def dolphin_classifier(data_directory):
    """
    Neural net classification of dolphin echolocation clicks to species
    :param data_directory:  root directory of data
    :return:  None
    """

    plt.ion()  # enable interactive plotting
    use_onlyN = 20  # debug, only read this many files for each species
    rissoDataPath = "".join((data_directory, "/Gg"))
    whiteDataPath = "".join((data_directory, "/Lo"))  # I want to treat both sets differently at first

    rData = util.get_files(rissoDataPath )
    wData = util.get_files(whiteDataPath)
    rParsed = util.parse_files(rData)
    wParsed = util.parse_files(wData)
    # My code assumes the amount of files for both are the same

    splitR = split_by_day(rParsed)  # After data gets parsed it is partitioned into a dictionary by day
    splitW = split_by_day(wParsed)

    rissoKeys = list(splitR.keys())  # converting all the keys of the dictionary into a list
    whiteKeys = list(splitW.keys())

    # With that list of keys I can use train_test_split to get 4 lists randomly separately days into train and test
    r_TrainKeys, r_TestKeys, w_TrainKeys, w_TestKeys = train_test_split(rissoKeys, whiteKeys)
    ALLtesting = []
    ALLtraining = []
    trainLabels = []
    features = []
    # probably don't need to declare them before but these are the lists for my final parsing

    for x in r_TestKeys:
        if splitR[x]:  # some of the files would come back with and empty list I don't want empty lists
            if len(splitR[x]) > 1:  # some namedTuples are grouped in lists I want just one list holding every Tuple
                for value in splitR[x]:
                    ALLtesting.append(value)
            else:
                ALLtesting.append(splitR[x][0])

    for x in w_TestKeys:
        if splitW[x]:
            if len(splitW[x]) > 1:
                for value in splitW[x]:
                    ALLtesting.append(value)
            else:
                ALLtesting.append(splitW[x][0])

    for x in r_TrainKeys:
        if splitR[x]:  # some of the files would come back with and empty list I dont want empty lists
            if len(splitR[x]) > 1:
                for value in splitR[x]:
                    ALLtraining.append(value)
            else:
                ALLtraining.append(splitR[x][0])

    for x in w_TrainKeys:
        if splitW[x]:
            if len(splitW[x]) > 1:
                for value in splitW[x]:
                    ALLtraining.append(value)
            else:
                ALLtraining.append(splitW[x][0])

    # now ALLtraining and ALLtesting hold their respective data in a single list to later use
    count = 0  # variable too know when in first iteration
    for nameTuple in ALLtraining:
        if nameTuple.label == "Gg":
            currLabel = [1, 0]
        else:
            currLabel = [0, 1]
        tempLabels = np.full((len(nameTuple.features), 2), currLabel)
        if count == 0:
            # first iteration needs to initialize the label and feature lists before stacking
            features = nameTuple.features
            trainLabels = np.full((len(nameTuple.features), 2), currLabel)
            count += 1
        else:
            # vstack lets me pile all the clicks into an (x,20) array
            features = np.vstack((features, nameTuple.features))
            trainLabels = np.vstack((trainLabels, tempLabels))

    # same thing is done to get the test values into lists
    i = 0
    testFeatures = []
    testLabels = []
    for nameTuple in ALLtesting:
        if nameTuple.label == "Gg":
            currLabel = [1, 0]
        else:
            currLabel = [0, 1]
        tempLabels = np.full((len(nameTuple.features), 2), currLabel)
        if i == 0:
            testFeatures = nameTuple.features
            testLabels = np.full((len(nameTuple.features), 2), currLabel)
            i += 1
        else:
            testFeatures = np.vstack((testFeatures, nameTuple.features))
            testLabels = np.vstack((testLabels, tempLabels))


    specification = [(Dense, [100], {'activation': 'relu', 'input_dim': 20,
                                     'kernel_regularizer': tf.keras.regularizers.L2(0.01)}),
                     (Dense, [100],
                      {'activation': 'relu', 'input_dim': 100, 'kernel_regularizer': tf.keras.regularizers.L2(0.01)}),
                     (Dense, [100],
                      {'activation': 'relu', 'input_dim': 100, 'kernel_regularizer': tf.keras.regularizers.L2(0.01)}),
                     (Dense, [2],
                      {'activation': 'softmax', 'input_dim': 100, 'kernel_regularizer': tf.keras.regularizers.L2(0.01)})
                     ]
    model = mod.build_model(specification)
    model.compile(optimizer="Adam",
                  loss="categorical_crossentropy",
                  metrics=["accuracy"])
    model.fit(features, trainLabels, batch_size=100, epochs=10)

    predictionList = model.predict(testFeatures)

    results = model.evaluate(testFeatures, testLabels)
    output = np.argmax(predictionList, axis=1)
    print(output)
    print("Acurracy: %.2f" % (results[1]*100))


if __name__ == "__main__":
    data_directory = "C:/Users/Jesse/Documents/FA2021/CS550/features"  # root directory of data
    dolphin_classifier(data_directory)
