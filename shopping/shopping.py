import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier as knn

TEST_SIZE = 0.4
k = 1 #K number of neighbors


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    months = {"Jan":0, "Feb":1, 'Mar':2, 'Apr':3, 'May':4, 'June':5, 'Jul':6, 'Aug':7, 'Sep':8, 'Oct':9, 'Nov':10, 'Dec':11}
    evidences = []
    labels = [] 
    with open(filename, 'r', newline="\r\n") as data: 
        for row in data: 
            try:
                row_list = row.split(",")
                evidence = [
                    int(row_list[0]),
                    float(row_list[1]),
                    int(row_list[2]),
                    float(row_list[3]),
                    int(row_list[4]),
                    float(row_list[5]),
                    float(row_list[6]),
                    float(row_list[7]),
                    float(row_list[8]),
                    float(row_list[9]),
                    months[row_list[10]],
                    int(row_list[11]),
                    int(row_list[12]),
                    int(row_list[13]),
                    1 if row_list[14]=="Returning_Visitor" else 0,
                    1 if row_list[15]=="True" else 0,
                ]
                label = 1 if row_list[-1][0] == 'T' else 0

                evidences.append(evidence)
                labels.append(label)
            except:
                continue
    #print(evidences)
    #print(labels)
    #print(len(evidences))
    return (evidences, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = knn(n_neighbors=k)
    return model.fit(evidence, labels)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    counter = 0 
    total = 0
    for i, j in zip(labels, predictions):
        if i == 1: 
            total += 1
            if j == 1:
                counter += 1
    sensitivity = counter / total

    counter = 0 
    total = 0
    for i, j in zip(labels, predictions):
        if i == 0: 
            total += 1
            if j == 0:
                counter += 1
    specificity = counter / total

    return (sensitivity, specificity)

if __name__ == "__main__":
    main()
