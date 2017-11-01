from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import sys
import pickle
import math
import string
import operator
import time


Builder.load_string("""
<QueryScreen>:
	FloatLayout:
		Label:
			font_size:30
			text: 'Enter your query below'
			size_hint: (.26, .10)
			pos: (300, 500)

		TextInput:
			id: query_input
			text: 'Enter your query here'
			multiline: False
            size_hint_x: .6
            size_hint_y: .1
            pos_hint: {'x': .05, 'y': .7}

		Button:
			text: 'Search'
			font_size: 20
			size_hint: (.33, .10)
			pos: (522, 419)
			on_press:
				root.function1(query_input.text)

		Label:
			font_size:20
			size_hint: (.26, .10)
			pos: (300, 350)
			text: root.one

		Label:
			font_size:20
			size_hint: (.26, .10)
			pos: (300, 320)
			text: root.two
		Label:
			font_size:20
			size_hint: (.26, .10)
			pos: (300, 290)
			text: root.three
		Label:
			font_size:20
			size_hint: (.26, .10)
			pos: (300, 260)
			text: root.four
		Label:
			font_size:20
			size_hint: (.26, .10)
			pos: (300, 230)
			text: root.five
		Label:
			font_size:20
			size_hint: (.26, .10)
			pos: (300, 200)
			text: root.six
		Label:
			font_size:20
			size_hint: (.26, .10)
			pos: (300, 170)
			text: root.seven
		Label:
			font_size:20
			size_hint: (.26, .10)
			pos: (300, 140)
			text: root.eight
		Label:
			font_size:20
			size_hint: (.26, .10)
			pos: (300, 110)
			text: root.nine
		Label:
			font_size:20
			size_hint: (.26, .10)
			pos: (300, 80)
			text: root.ten
		Label:

			font_size:50
			size_hint: (.26, .10)
			pos: (300, 300)
			text: root.no_document_found

		Button:
			text: 'Clear'
			font_size: 20
			size_hint: (.33, .10)
			pos: (280, 30)
			on_press:
				root.function2()

""")



class QueryScreen(Screen):
	one = StringProperty()
	two = StringProperty()
	three = StringProperty()
	four = StringProperty()
	five = StringProperty()
	six = StringProperty()
	seven = StringProperty()
	eight = StringProperty()
	nine = StringProperty()
	ten = StringProperty()
	no_document_found = StringProperty()
	
	def function1(self, input_query):
		print("Your query: " + str(input_query))
		final_documents = ["","","","","","","","","",""]
		start_time = time.time()

		query = []
		query_inverted_index = {}
		query_magnitude = 0.0

		query_text = ""
		
		with open("inverted_index.pickle", "rb") as handle:
			document_inverted_index = pickle.load(handle)

		handle.close()


		query_text = input_query
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

		
		sorted_score = sorted(score.items(), key = operator.itemgetter(1), reverse = True)


		for i, document_no in zip(range(1, 11), sorted_score):
			final_documents[i-1] = str(i) + ".    " + str(sorted_score[i-1])
		self.one = final_documents[0]
		self.two = final_documents[1]
		self.three = final_documents[2]
		self.four = final_documents[3]
		self.five = final_documents[4]
		self.six = final_documents[5]
		self.seven = final_documents[6]
		self.eight = final_documents[7]
		self.nine = final_documents[8]
		self.ten = final_documents[9]

		if(len(sorted_score) == 0):
			self.no_document_found = "No document match your query!"
		print("Query time: " + str(time.time() - start_time))



	# Clear the result
	def function2(self):
		self.one = ""
		self.two = ""
		self.three = ""
		self.four = ""
		self.five = ""
		self.six = ""
		self.seven = ""
		self.eight = ""
		self.nine = ""
		self.ten = ""
		self.no_document_found = ""



sm = ScreenManager(transition = FadeTransition())
query_screen = QueryScreen(name = 'query_screen')
sm.add_widget(query_screen)

class TestApp(App):
	def build(self):
		return sm

if __name__ == '__main__':
	TestApp().run()