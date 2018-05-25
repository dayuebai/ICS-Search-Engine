import pymongo
from bson.objectid import ObjectId

# Make a connection to MongoDB
client = pymongo.MongoClient('localhost', 27017)
# Get a single instance of database
db = client.postingDb
# Get a connection from the database
posting = db.posting

def run_main() -> None:
	docId_url_dict = read_file_into_dict("docId_url.txt")
	token_postId_dict = read_file_into_dict("token_postId.txt")
	while True:
		key_word_list = ask_user_input()
		if key_word_list == []:
			break
		docId_result = handle_user_input(key_word_list, token_postId_dict)
		if docId_result:
			sorted_docId_result = sorted([(docId, rating) for docId, rating in docId_result.items()], key = lambda x: (-x[1], x[0]))
			# print(sorted_docId_result)
			docId_list = [sorted_docId_result[i][0] for i in range(0, len(sorted_docId_result)) if i < 10]
			# print(docId_list)
			url_list = get_urls_by_docIds(docId_url_dict, docId_list)
			print("Top 10 search result: ")
			for url in url_list:
				print(url)
	print("Finish searching, bye!")


def read_file_into_dict(file_name: str) -> dict:
	result_dict = dict()
	with open(file_name, "r") as file:
		result_list = file.read().splitlines()
		for line in result_list:
			a, b = line.split("--->")
			result_dict[a] = b
	return  result_dict


def get_urls_by_docIds(docId_url_dict: dict, docId_list: list) -> list:
	url_list = []
	for docId in docId_list:
		url_list.append(docId_url_dict[docId])
	return url_list


def ask_user_input() -> list:
	query = input("Please enter keywords you want to search: ")
	return query.split()


def handle_user_input(key_word_list: list, token_postId_dict: dict):
	postId_list = []
	for word in key_word_list:
		if word.lower() in token_postId_dict:
			postId_list.append(token_postId_dict[word.lower()])
	if postId_list:
		# print("postId list: ", postId_list)
		raw_result = []
		for postId in postId_list:
			raw_result.append(retrieve_docId_by_postId(postId))
		docId_set = set(raw_result[0].keys())
		for i in range(1, len(raw_result)):
			docId_set = docId_set & set(raw_result[i].keys())
		# For test
		# print(docId_set)
		if docId_set:
			result = dict()
			for docId in docId_set:
				total_tfidf = 0
				for post in raw_result:
					total_tfidf += post[docId]["TF-IDF"]
				result[docId] = total_tfidf
			# print(result)
			return result
		else:
			print("Cannot find file containing all the keywords you want to search, please try searching other words...")

	else:
		print("No search result, please try searching other words...")


def retrieve_docId_by_postId(postId: str) -> dict:
	object_id = ObjectId(postId)
	document = posting.find_one({"_id": object_id})
	del document["_id"]
	return document


if __name__ == "__main__":
	run_main()