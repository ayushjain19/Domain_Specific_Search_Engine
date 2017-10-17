from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen
import html
import os



i = 1

for num in range(1, 11):
	parent_link_response = urllib.request.urlopen("https://www.theverge.com/mobile/archives/" + str(num))
	html = parent_link_response.read()
	f = open("first.html", "w+")
	f.write(str(html))
	f.close()

	with open("first.html", "r", encoding = 'utf-8') as fp:
		soup = BeautifulSoup(fp, "lxml")

	fp.close()
	all_para_containing_links_in_page = soup.find_all("div", class_ = "body")

	# fp = open("exctraction.txt", "w+", encoding = 'utf-8')
	# for link_para in all_para_containing_links_in_page:
	# 	page_name = str(link_para.h3.a.next_element)
	# 	fp.write("Document " + "\n")
	# fp.close()



	# current_directory = os.getcwd()
	# print(current_directory)
	# dir_path = os.path.join(current_directory, "/Downloaded_documents")
	# directory_path = os.path.dirname(dir_path)
	# if not os.path.exists(directory_path):
	# 	print("hello")
	# 	os.makedirs(directory_path)



	for link_para in all_para_containing_links_in_page:
		link = link_para.h3.a.get('href')

		urllib.request.urlretrieve(link, "Document_" + str(i) + ".html")
		
		html = urllib.request.urlopen(link).read()    
		soup = BeautifulSoup(html, "lxml")
		for script in soup(["script", "style"]):
		    script.extract()
		text = soup.get_text()
		# break into lines and remove leading and trailing space on each
		lines = (line.strip() for line in text.splitlines())
		# break multi-headlines into a line each
		chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
		# drop blank lines
		text = '\n'.join(chunk for chunk in chunks if chunk)

		text = str(text)
		# text = text[text.find('Linkedin'):]

		final_text = ""
		head, sep, tail = text.partition('clock')
		final_text += head + '\n'

		head, sep, tail = text.partition('Linkedin')
		final_text += tail

		head, sep, tail = final_text.partition('In this Storystream')
		final_text = head

		head, sep, tail = final_text.partition('Next Up In\nTech')
		final_text = head

		head, sep, tail = final_text.partition('Next Up In\nCircuit Breaker')
		final_text = head

		final_text = final_text.lower()

		f = open("Doc_" + str(i) + ".txt", "w+")
		f.write(final_text)
		f.close()
		i = i + 1