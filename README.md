# NLP-Powered Book Recomemndation System
## Introduction
Our project is a website that uses Machine Learning to automatically recommend books for the user and compute the similarity on reading habit between the user and his/her friend. We came up with this idea because we realized less and less people are reading books, either online or in paper copies. One of the leading issues is people lack access to information about books they would probably be interested in. That’s why we created a way of smart book recommendation process and add a function that tells user how his/her reading habit is closely related to his/her friends. 

## Running the Project
After downloading all the files, there are a couple more required steps to run it.
First, you have to unzip the ```book-vec-group.csv.zip``` file into its csv form. This file stores all of the data for the books, but was too large to upload to github. After unzipping, place it in the ```project/static``` directory.

Then, you also have to download Flask, as well as ```scipy.stats```. Then, you have to create a server from your computer. The way to do this is to first navigate to the ```project/``` directory, then typing ```export FLASK_APP=app.py``` in the terminal. Afterwards, typing ```flask run``` will give you a local host that you can copy and paste into your browser to view the website.

If you want to recommend book that is not in  ```book-vec-group.csv```, you can use ```EmbeddingBert.ipynb``` and ```EmbeddingWord2Vec.ipynb``` to generate the embeddings for your book base on its summary.

## Technical Architecture
First, the user will see a homepage, from which they can click the download icon to bring them to the upload page. From there, they can upload either one or two files and press compare. This will send a post request to the backend, which will then download the files into the directory, and process them into a list of the most highly rated books, which is then run through the algorithm to produce the necessary results. Depending on if one or two files were uploaded, the user will be brought to different summary pages: one with just a list of recommendations if they uploaded a single file, and one with a list of tuples of similar books between users, with a count of how many such pairs there were.

![image](https://user-images.githubusercontent.com/59509756/206057505-0f8df06d-4560-48f6-a684-b83df8b02dbc.png)



## Algorithm Explained
Our recommendation model is base on calculating a book/paragraph embedding through mean-pooling all the words embeddings. We generate two word embeddings: the first is based on ```BERT(Bidirectional Encoder Representations from Transformers)```, and second is based on ```word2vec```. Using these embeddings, for every users' favorable books, we calculate the ranking of the all other books according to their cosine distance. We then use ```rank-ensemble mechanism``` to generate a single ranking, and the top ```n``` books are used to recommend to the users.

When comparing the preference of two users, we apply ```t-SNE(t-distributed stochastic neighbor embedding)```, and ```k-means``` on top of our ```BERT``` embeddings to divide all books into 50 groups. 
We find the number of pairs of favorable books that are in the same group, and we will output all such tuples. 

## Work Distribution
The frontend was mainly designed by David, who incorporated css and Javascript to the HTML pages to improve the visual aspect of the website, including an animated background for the summary. 

The backend was managed by Bwohan, who was in charge of all the python, as well as the upload page because it communicated the most with the backend. He made sure that communication between the frontend and backend went smoothly and that information could be transferred. He also handled some preprocessing of the user's uploaded files, and put them in a convenient format for the algorithm.

Yanzhen mainly worked on the algorithm, developing ways to find similarities between books and users. He worked on returning accurate results, as well as ensuring the results were different enough from the original books to ensure relevancy. 

## References:
1.Mikolov, T. et al. (2013) Efficient estimation of word representations in vector space, arXiv.org. Available at: https://arxiv.org/abs/1301.3781 (Accessed: December 6, 2022). 

2.Devlin, J. et al. (2018) Bert: Pre-training of deep bidirectional Transformers for language understanding, ACL Anthology. Available at: https://aclanthology.org/N19-1423/ (Accessed: December 6, 2022). 

3.Shen, J. et al. (2019) Setexpan: Corpus-based set expansion via context feature selection and Rank Ensemble, SpringerLink. Springer International Publishing. Available at: https://link.springer.com/chapter/10.1007/978-3-319-71249-9_18 (Accessed: December 6, 2022). 
