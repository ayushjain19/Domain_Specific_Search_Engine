import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import sys
import pickle
import math
import string
import operator
import time

start_time = time.time()
length = len(sys.argv)

query = []
query_inverted_index = {}
query_magnitude = 0.0

query_text = ""


with open("inverted_index.pickle", "rb") as handle:
	document_inverted_index = pickle.load(handle)

handle.close()


for i in range(1, length):
	query_text += str(sys.argv[i]) + " "

query_text = query_text.lower()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in query_text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
query_text = '\n'.join(chunk for chunk in chunks if chunk)

query_text = str(query_text)


text_without_punctuation = " ".join("".join([" " if ch in string.punctuation else ch for ch in query_text]).split())
word_tokens = nltk.word_tokenize(text_without_punctuation)


stop_words = set(stopwords.words('english'))
query_words_without_stopwords = []
 
for w in word_tokens:
    if w not in stop_words:
        query_words_without_stopwords.append(w)


for word in query_words_without_stopwords:
	if not word in query_inverted_index:
		query_inverted_index[word] = 1.0
	else:
		query_inverted_index[word] += 1.0

for word in query_inverted_index:
	query_magnitude += query_inverted_index[word] ** 2

query_magnitude = math.sqrt(query_magnitude)

for word in query_inverted_index:
	query_inverted_index[word] = query_inverted_index[word] / query_magnitude

score = {}
for query_word in query_inverted_index:
	if query_word in document_inverted_index:
		for i in document_inverted_index[query_word]:
			if i not in score and i in document_inverted_index[query_word]:
				score[i] = document_inverted_index[query_word][i] * query_inverted_index[query_word]
			elif i in score and i in document_inverted_index[query_word]:
				score[i] += document_inverted_index[query_word][i] * query_inverted_index[query_word]

# print(len(score))
sorted_score = sorted(score.items(), key = operator.itemgetter(1), reverse = True)

# print(len(sorted_score))

for i, document_no in zip(range(1, 11), sorted_score):
	print(str(i) + " " + str(document_no))

if(len(sorted_score) == 0):
	print("No document match your query!")


print(time.time() - start_time)
# print(score)
# print(query_inverted_index)

# print(inverted_index)
# print(query)
