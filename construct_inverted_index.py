import sys
import json
import nltk
import math
import urllib.request
import urllib.parse
import os.path
import string
import hashlib
import pymongo
import pprint

from bs4 import BeautifulSoup
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

# Make a connection to MongoDB
client = pymongo.MongoClient('localhost', 27017)
# Get a single instance of database
db = client.postingDb
# Get a collection(Group of documents stored in MongoDB, like table)
collection = db.posting

docId_url_dict = dict()
total_doc_number = 0
token_dict = dict()
stop_words_set = set(stopwords.words("english")).union(set(string.punctuation))

def parse_json_file(json_file_path):
	with open(json_file_path, 'r') as json_data:
		file_dict = json.load(json_data)
		global total_doc_number
		global docId_url_dict
		total_doc_number = len(file_dict) # Get number of documents of the corpus
		docId_url_dict = file_dict # Get docIc->url dict
		# counter = 0
		for docId in file_dict:
			if docId != "39/373":
				print("################ docId: ", docId, "#####################")
				parse_corpus_file(docId)
				# counter += 1
		# update_post()

def parse_corpus_file(docId):
	html_file_path = os.path.join(".", "WEBPAGES_RAW/" + docId)

	with open(html_file_path,'r') as html_file:
		data = html_file.read()
		soup = BeautifulSoup(data, "html.parser")
		for tag in soup(["head", "link", "style", "script", "meta", "[document]"]):
			tag.extract()

		# token_list = nltk.tokenize.word_tokenize(soup.get_text())
		tokenizer = RegexpTokenizer(r'\w+')
		token_list = [i.lower() for i in tokenizer.tokenize(soup.get_text())]

		# Inverted Index Structure:
		# token dictionary
		# token -> [tokenId, postId]
		# posting dictionary
		# docId -> statistics
		# statistics: TF-IDF
		for token in token_list:
			if token not in stop_words_set:
				# print(token)
				if token not in token_dict:
					print("Inserting token: " + token)
					post = defaultdict(dict)
					post[docId]["TF"] = 1 
					post[docId]["TF-IDF"] = math.log(total_doc_number)
					post_id = collection.insert_one(post).inserted_id
					token_dict[token] = post_id # token_dict is a global variable
				else:
					# print("Updating token: " + token)
					post_id = token_dict[token]
					# Update TF
					collection.update({"_id":post_id}, {"$inc":{(docId+".TF"):1}})


def update_post():
	print("Starting to update post...")
	for post in collection.find({}):
		doc_occurrence_counter = len(post)-1
		IDF = math.log( total_doc_number / (doc_occurrence_counter) )
		for key in post:
			# Update TF-IDF for all documents, key is docId
			if ("/" in key):
				TFIDF = post[key]["TF"] * IDF
				collection.update({"_id":post["_id"]}, {"$set":{(key+".TF-IDF"):TFIDF}})


if __name__ == "__main__":
	json_file_path = os.path.join(".", "WEBPAGES_RAW/bookkeeping.json")
	parse_json_file(json_file_path)

	# Write docId->url dict and token->postId dict into files
	with open("docId_url.txt",'w') as out_file1:
		for key in docId_url_dict:
			out_file1.write(key + "--->" + docId_url_dict[key] + "\n")
	with open("token_postId.txt",'w') as out_file2:
		for key in token_dict:
			out_file2.write(key + "--->" + str(token_dict[key]) + "\n")

	# Token dictionary will be stored in main memory
	# posting will be stored in database
	# For test
	# for post in collection.find({}):
	# 	pprint.pprint(post)
	print("There are: " + str(total_doc_number) + " files, in total.")
	print("There are: " + str(len(token_dict)) + " tokens, in total.")	

	# For search
	# db.posting.find({"_id" : ObjectId("5aff494e4175862746f40a78")});
