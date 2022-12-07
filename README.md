# Group-1-Project

## Running the Project
After downloading all the files, there are a couple more required steps to run it.
First, you have to unzip the ```book-vec-group.csv.zip``` file into its csv form. This file stores all of the data for the books, but was too large to upload to github. After unzipping, place it in the ```project/static``` directory.

Then, you also have to download Flask, as well as scipy.stats. Then, you have to create a server from your computer. The way to do this is to first navigate to the ```project/``` directory, then typing ```export FLASK_APP=app.py``` in the terminal. Afterwards, typing ```flask run``` will give you a local host that you can copy and paste into your browser to view the website.

If you want to recommend book that is not in  ```book-vec-group.csv```, you can use ```EmbeddingBert.ipynb``` and ```EmbeddingWord2Vec.ipynb``` to generate the embeddings for your book base on its summary.

## Algorithm Explained
Our recommendation model is base on calculate a book/paragraph embedding through mean-pooling all the words embeddings. We generate two word embeddings: the first is based on ```BERT(Bidirectional Encoder Representations from Transformers)```, and second is based on ```word2vec```. Using these embeddings, for every users' favorable books, we calculate the ranking of the all other books according to their cosine distance. We then use rank-ensemble mechanism to generate a single ranking, and the top ```n``` books are used to recommend to the users.

When comparing the preference of two users, we apply ```t-SNE(t-distributed stochastic neighbor embeddin)```, and ```k-means``` on top of our BERT embeddings to divide all books into 50 groups. 
We find the number of pairs of favorable books are in the same group, and we will output all such tuples. 


## References:
1.Devlin, J. et al. (no date) Bert: Pre-training of deep bidirectional Transformers for language understanding, ACL Anthology. Available at: https://aclanthology.org/N19-1423/ (Accessed: December 6, 2022). 

2.Mikolov, T. et al. (2013) Efficient estimation of word representations in vector space, arXiv.org. Available at: https://arxiv.org/abs/1301.3781 (Accessed: December 6, 2022). 

3.Shen, J. et al. (1970) Setexpan: Corpus-based set expansion via context feature selection and Rank Ensemble, SpringerLink. Springer International Publishing. Available at: https://link.springer.com/chapter/10.1007/978-3-319-71249-9_18 (Accessed: December 6, 2022). 
