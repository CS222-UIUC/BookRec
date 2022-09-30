import pandas as pd

books_filename   = 'BX-CSV-Dump/BX-Books.csv'
ratings_filename = 'BX-CSV-Dump/BX-Book-Ratings.csv'

def get_books():
    '''Reads the book data from the BX-Books file, and puts the title and author into the dataframe.
    Sets the index of the dataframe to the isbn of each book and deletes books with missing data'''
    df_books = pd.read_csv(
        books_filename,
        encoding = "ISO-8859-1",
        sep=";",
        header=0,
        names=['isbn', 'title', 'author'],
        usecols=['isbn', 'title', 'author'],
        dtype={'isbn': 'str', 'title': 'str', 'author': 'str'})
    df_books = df_books.set_index('isbn')
    df_books.dropna(inplace=True)
    return df_books

def get_ratings():
    '''Reads information from the BX-Book-Ratings file and puts them into a dataframe.
    Each row contains the users unique ID, the isbn of the book, and the rating the user assigned to it.'''
    df_ratings = pd.read_csv(
        ratings_filename,
        encoding = "ISO-8859-1",
        sep=";",
        header=0,
        names=['user', 'isbn', 'rating'],
        usecols=['user', 'isbn', 'rating'],
        dtype={'user': 'int32', 'isbn': 'str', 'rating': 'float32'})
    df_ratings = df_ratings[df_ratings.index <= 100000]
    return df_ratings


def main():
    #df_books = get_books()
    #print(df_books.loc["0195153448"]["title"])
    df_ratings = get_ratings()
    print(df_ratings)

main()