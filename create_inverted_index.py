import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import pickle
import math
import time


start_time = time.time()
inverted_index = {}
document_frequency = {}
lemmatizer = WordNetLemmatizer()

for i in range(1, 101):
	f = open("Doc_" + str(i) + ".txt", "r")
	fp = open("qwerty.txt", "w+")
	text = f.read()

	# text = "Hello there! I am fine. What about you Hello Hello?"
	text_without_punctuation = " ".join("".join([" " if ch in string.punctuation else ch for ch in text]).split())
	word_tokens = nltk.word_tokenize(text_without_punctuation)
	

	stop_words = set(stopwords.words('english'))
	words_without_stopwords = []
	 
	for w in word_tokens:
	    if w not in stop_words:
	        words_without_stopwords.append(w)

	for word in words_without_stopwords:
		fp.write(lemmatizer.lemmatize(word) + "\n")
	fp.close()


	for word in words_without_stopwords:
		if word in document_frequency.keys():
			if document_frequency[word][0] == 0:
				document_frequency[word][0] = 1
				document_frequency[word][1] += 1


			if i in inverted_index[word]:
				inverted_index[word][i] += 1
			else:
				inverted_index[word][i] = 1




		else:
			document_frequency[word] = [1, 1]
			inverted_index[word] = {i: 1}



	f.close()


for word in document_frequency:
	document_frequency[word][1] = math.log(100 / document_frequency[word][1])


for word in inverted_index:
	for i in inverted_index[word]:
		inverted_index[word][i] *= document_frequency[word][1]
# print(words_without_stopwords)
# print(document_frequency)
# print(inverted_index)

with open('inverted_index.pickle', 'wb') as handle:
	pickle.dump(inverted_index, handle, protocol = pickle.HIGHEST_PROTOCOL)

handle.close()

print(time.time() - start_time)