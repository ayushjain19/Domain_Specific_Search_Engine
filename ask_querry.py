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

querry = []
querry_inverted_index = {}
querry_magnitude = 0.0

querry_text = ""


with open("inverted_index.pickle", "rb") as handle:
	document_inverted_index = pickle.load(handle)

handle.close()


for i in range(1, length):
	querry_text += str(sys.argv[i]) + " "

querry_text = querry_text.lower()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in querry_text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
querry_text = '\n'.join(chunk for chunk in chunks if chunk)

querry_text = str(querry_text)


text_without_punctuation = " ".join("".join([" " if ch in string.punctuation else ch for ch in querry_text]).split())
word_tokens = nltk.word_tokenize(text_without_punctuation)


stop_words = set(stopwords.words('english'))
querry_words_without_stopwords = []
 
for w in word_tokens:
    if w not in stop_words:
        querry_words_without_stopwords.append(w)


for word in querry_words_without_stopwords:
	if not word in querry_inverted_index:
		querry_inverted_index[word] = 1.0
	else:
		querry_inverted_index[word] += 1.0

for word in querry_inverted_index:
	querry_magnitude += querry_inverted_index[word] ** 2

querry_magnitude = math.sqrt(querry_magnitude)

for word in querry_inverted_index:
	querry_inverted_index[word] = querry_inverted_index[word] / querry_magnitude

score = {}
for querry_word in querry_inverted_index:
	if querry_word in document_inverted_index:
		for i in document_inverted_index[querry_word]:
			if i not in score and i in document_inverted_index[querry_word]:
				score[i] = document_inverted_index[querry_word][i] * querry_inverted_index[querry_word]
			elif i in score and i in document_inverted_index[querry_word]:
				score[i] += document_inverted_index[querry_word][i] * querry_inverted_index[querry_word]

# print(len(score))
sorted_score = sorted(score.items(), key = operator.itemgetter(1), reverse = True)

# print(len(sorted_score))

for i, document_no in zip(range(1, 11), sorted_score):
	print(str(i) + " " + str(document_no))

if(len(sorted_score) == 0):
	print("No document match your querry!")


print(time.time() - start_time)
# print(score)
# print(querry_inverted_index)

# print(inverted_index)
# print(querry)