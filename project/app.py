from mimetypes import init
from django.shortcuts import render
from flask import Flask
from flask import render_template, request, url_for, redirect, session
import pandas as pd
#from scipy.spatial import distance
import zipfile
import os.path
import os
from scipy.stats import rankdata
import operator
from numpy import dot
from numpy.linalg import norm

app = Flask(__name__)

userid = ""
user1booklist = []
user2booklist = []
recommend_list = []
common_groups_list =[] 
common_groups = ''
score = 5.5

#df_book = pd.read_csv('https://firebasestorage.googleapis.com/v0/b/cs-222.appspot.com/o/Group-1-Project-main%2Fbook-vec-group.csv?alt=media&token=fb615c53-e2ae-4d9c-903b-093159c8da18') 
df_book = pd.read_csv('static/book-vec-group.csv')

@app.route('/', methods=['GET'])
def homepage():
    return render_template("homepage.html")

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        upload_file = request.files['file1']
        df1, df2 = pd.DataFrame(), pd.DataFrame()
        global recommend_list
        global common_groups
        common_groups = ''
        if upload_file.filename != '':
            upload_file.save(userid + "_" + upload_file.filename)
            df1 = file_to_df(userid + "_" + upload_file.filename, userid)
            global user1booklist
            user1booklist = getNameList(df1)
            print(df1)
        compare_file = request.files['file2']
        if compare_file.filename != '' and upload_file.filename != '':
            compare_file.save(userid + "_" + compare_file.filename)
            df2 = file_to_df(userid + "_" + compare_file.filename, userid)
            global user2booklist
            user2booklist = getNameList(df2)
            global common_groups_list
            common_groups_list, common_groups = compare_on_list(user1booklist, user2booklist)
            common_groups = str(common_groups)
            recommend_list = common_groups_list
        else:
            recommend_list = recommend_on_list(user1booklist)
        
        return redirect(url_for('summary'))
    return render_template("index.html")

@app.route('/summary', methods=['GET'])
def summary():
    if common_groups == '':
        return render_template("summary.html",recs=recommend_list)
    else:
        return render_template("comparison.html",recs=recommend_list, similarity = common_groups)

if __name__ == "__main__":
    app.run(debug=True)

def file_to_df(filename, id):
    df = pd.read_csv(
        filename,
        encoding="ISO-8859-1",
        header=0,
        usecols=["Title", "ISBN", "My Rating"],
        dtype={"Title": "str", "ISBN":"str", "My Rating": "float"}
    )
    df = df.dropna(subset=['ISBN'])
    for i in range(len(df.index)):
        s = len(df.at[i,'ISBN'])
        df.at[i,'ISBN'] = df.at[i,'ISBN'][2:s-1]
        if (df.at[i,"ISBN"] == ''):
            df = df.drop(i)
    for i in df.index:
        if (df.at[i,"My Rating"] == 0.0):
            df = df.drop(i)
    df = df.rename(columns={"Title": "title", "ISBN": "isbn", "My Rating": "rating"})
    df["UserID"] = id
    df = df[['UserID',"title", "isbn", "rating"]]
    return df

def getNameList(dataframe):
    df = dataframe[dataframe["rating"] >= 4.0]
    return df["title"].tolist()

#convert bert embedding in string a a list (vector)
def strtoVecBERT(str):
    str = str[1:len(str) - 1]
    list_str = list(str.split(","))
    list_float = []
    for element in list_str:
        list_float.append(float(element))
    return list_float

#convert word2vec embedding in string to a list (vector)
def strtoVecword2vec(str):
    str = str[1:len(str) - 1]
    list_str = list(str.split(" "))
    list_float = []
    for element in list_str:
        if len(element) > 0:
            list_float.append(float(element))
    return list_float

#Calculate cosine_distance of two vectors
def cosine_distance(vec1, vec2):
    cos_distance = 1 - dot(vec1, vec2) / (norm(vec1) * norm(vec2))
    return cos_distance

#compute ranking of word2vec embeddings
def compute_word2vec_rank(book_title, n):
    word2vec_list = []
    vec1 = strtoVecword2vec(df_book[df_book["Book-Title"] == book_title]["word2vec"].tolist()[0])
    for index, row in df_book.iterrows():
        vec2 = strtoVecword2vec(row["word2vec"])
        dist = cosine_distance(vec1, vec2) 
        title2 = row["Book-Title"]
        word2vec_list.append((title2, dist))
    
    word2vec_sorted = sorted(word2vec_list, key=lambda tup: tup[1])[0:len(word2vec_list)]
    word2vec_dist = [x[1] for x in word2vec_sorted]
    word2vec_rank = rankdata(word2vec_dist)
    return word2vec_rank, word2vec_sorted

#compute ranking of bert embeddings
def compute_bert_rank(book_title, n):
    bert_list = []
    vec1 = strtoVecBERT(df_book[df_book["Book-Title"] == book_title]["BERT"].tolist()[0])
    for index, row in df_book.iterrows():
        vec2 = strtoVecBERT(row["BERT"])
        dist = cosine_distance(vec1, vec2) 
        title2 = row["Book-Title"]
        bert_list.append((title2, dist))

    bert_sorted = sorted(bert_list, key=lambda tup: tup[1])[0:len(bert_list)]
    bert_dist = [x[1] for x in bert_sorted]
    bert_name = [x[0] for x in bert_sorted]
    bert_rank = rankdata(bert_dist)
    return bert_rank, bert_sorted

#combine two models of embeddings using rank ensemble
def recommend_n_on_ensemble(book_title, n):
    word2vec_rank, word2vec_sorted = compute_word2vec_rank(book_title, n)
    bert_rank, bert_sorted = compute_bert_rank(book_title, n)
    bert_name = [x[0] for x in bert_sorted]
    
    scores = []
    for i in range(len(word2vec_rank)):
       score = 1/ (i + 1)  #rank of word2vec; add 1 to avoid division by 0
       index_bert_name = bert_name.index(word2vec_sorted[i][0])
       rank = bert_rank[index_bert_name]
       score = score + 1 / (rank + 1) 
       scores.append((word2vec_sorted[i][0], score))
    
    scores_sorted = sorted(scores, key=lambda tup: tup[1])[:n]
    book_list = [x[0] for x in scores_sorted]
    return book_list

#recommend n books base on a list of book titles
def recommend_on_list(book_list, n=10):
    recommend_list = []
    #print(book_list)
    for book in book_list:
        recommend_books = recommend_n_on_ensemble(book, 10)
        for recommend_book in recommend_books:
            if recommend_book not in recommend_list:
                recommend_list.append(recommend_book)
    return recommend_list[:n]

#compare book title list given by two users, return books in common groups
def compare_on_list(book_list1, book_list2):
    group_list1 = []
    group_list2 = []
    for book in book_list1:
        row = df_book[df_book["Book-Title"] == book]
        group = row["group"].to_list()[0]
        group_list1.append(group)
    
    for book in book_list2:
        row = df_book[df_book["Book-Title"] == book]
        group = row["group"].to_list()[0]
        group_list2.append(group)
    
    common_groups_list = []
    common_groups = 0
    i = 0
    for group1 in group_list1:
        j = 0
        for group2 in group_list2:
            if group1 == group2:
                common_groups += 1
                common_groups_list.append((book_list1[i], book_list2[j]))    
            j += 1
        i += 1

    return  common_groups_list, common_groups

