import pandas as pd
import csv
import json
def read_file(filename):
    '''Appends each row in the file to a list'''
    data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f, dialect='excel-tab')
        for row in reader:
            data.append(row)
    return data

def make_dataframe():
    '''Takes a list of data corresponding to each row and creates a dataframe.
    Indices of the data are lowercase book titles, and columns store ID, capitalized titles,
    authors, and a JSON format of genres'''
    data = read_file("booksummaries.txt")
    indices = []
    freebase_ids = []
    authors = []
    names = []
    genres = []

    rowcounter = 1
    for i in data:
        indices.append(rowcounter)
        rowcounter += 1
        freebase_ids.append(i[1])
        names.append(i[2])
        authors.append(i[3])
        genres.append(i[5])

    dataframe = pd.DataFrame({"Index": indices, "ID": freebase_ids, "BookTitle": names, "Author": authors, "Genre": genres})
    for i in range(len(names)):
        names[i] = names[i].lower()
    dataframe.index = names
    return dataframe


def clean_data(dataframe):
    '''Formats the Genres JSON to a standard list of the genres'''
    dataframe = dataframe.drop(dataframe[dataframe["Genre"] == ""].index)
    clean_genres = []
    for i in dataframe["Genre"]:
        clean_genres.append(list(json.loads(i).values()))
    dataframe["Genre"] = clean_genres
    return dataframe


def main():
    dataframe = make_dataframe()
    dataframe = clean_data(dataframe)
    print(dataframe.head())
    

if __name__ == '__main__':
    main()