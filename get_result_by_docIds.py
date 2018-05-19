def read_docId_url(file_name:str) ->dict:
	docId_url_dict = dict()
	with open(file_name, "r") as docId_url_file:
		docId_url_list = docId_url_file.read().splitlines()
		for line in docId_url_list:
			docId, url = line.split("--->")
			docId_url_dict[docId] = url
			# For test
			# print("docId: " + docId + "--->url: " + docId_url_dict[docId])
		# print("Total amount of documents: " + str(len(docId_url_dict)))
	return docId_url_dict

def get_urls_by_docIds(docId_url_dict: dict, docId_list: list) -> list:
	url_list = []
	for docId in docId_list:
		url_list.append(docId_url_dict[docId])
		print(docId_url_dict[docId])
	return url_list



if __name__ == "__main__":
	docId_list1 = ["0/103","0/111","0/115","0/117","0/129","0/137","0/149","0/15","0/153","0/168"]
	docId_list2 = ["1/351","10/183","10/316","13/378","15/365","17/28","17/330","19/22","19/404","2/46"]
	docId_list3 = ["0/10","0/100","0/104","0/106","0/108","0/11","0/110","0/112","0/113","0/118"]
	docId_url_dict = read_docId_url("docId_url.txt")
	print("-----------------------Informatics-----------------------------")
	get_urls_by_docIds(docId_url_dict, docId_list1)
	print("-----------------------Mondego-----------------------------")
	get_urls_by_docIds(docId_url_dict, docId_list2)
	print("-----------------------Irvine-----------------------------")
	get_urls_by_docIds(docId_url_dict, docId_list3)

