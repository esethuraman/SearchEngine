import sys
import re
from bs4 import BeautifulSoup
import os

#-----------------------------------------------
source_folder_name = "Source"
destination_folder_name = "C:\\Users\\Elavazhagan S\\Documents\\GraduateCourse\\Fall17\\IR\\Project\\LocalFiles\\DocumentTerms"
#-----------------------------------------------

source_folder = os.path.join(source_folder_name)
destination_folder= os.path.join(destination_folder_name)

def main():
	punctuation_handle_flag = 0
	casefold_handle_flag = 0

	(punctuation_handle_flag, casefold_handle_flag) = get_flags()
	
	for filename in os.listdir(source_folder):
		with open(os.path.join(source_folder, filename), "r") as input_file:

			line = input_file.readlines()[3]
			soup = BeautifulSoup(line, "html.parser")

			body_soup = soup.find('body')
			all_contents = body_soup.find_all(['p', 'h'])

			filtered_text = eliminate_formulae_and_pronounciatino(all_contents)
			input_file.close()
			input_file = open(os.path.join(source_folder, filename), "r")
			title = input_file.readlines()[1].split("/")[-1]
			# print(title)
			parse_and_write(filtered_text, destination_folder, title.strip(), punctuation_handle_flag, casefold_handle_flag)


def parse_and_write(entire_text, destination_folder, document_id, punctuation_handle_flag, casefold_handle_flag):

	index_file = open(destination_folder+"/"+document_id+".txt", 'w', encoding='utf-8')

	#appending the title of the document to the begining of the content of document 
	entire_text = eliminate_citations(entire_text)

	if int(casefold_handle_flag) > 0:
			entire_text = entire_text.casefold()

	text_parts = entire_text.split()

	# flag for not writing a new line character in the very first line
	is_first_line = True

	for text in text_parts:
		if '\\x' in text:
			texts_from_non_breaking_space = re.sub('\\\\x[a-z0-9][a-z0-9]', " ", text).split()
			texts = texts_from_non_breaking_space
		else:
			texts = list([text])

		for sub_text in texts:
			
			sub_text = remove_leading_special_characters(sub_text)
			
			is_match = is_non_numericals(sub_text)
			if is_match:
				sub_text = handle_punctuation(sub_text, punctuation_handle_flag)
				

			else:
				cnt = len(sub_text)-1
				if is_non_numericals(sub_text[cnt]):
					for j in range(len(sub_text)):
						local_match = is_non_numericals(sub_text[cnt])
						if local_match:
							cnt -= 1
						else:
							non_numerical_part = handle_punctuation(text[(cnt+1):len(text)], punctuation_handle_flag)
							
							if (non_numerical_part.startswith('-')):
								non_numerical_part = remove_leading_special_characters(non_numerical_part)
								
							if len(non_numerical_part.strip())>0:
								non_numerical_part = "\n" + non_numerical_part
							
							sub_text = (sub_text[0:(cnt+1)])+ non_numerical_part
							# index_file.write(str(sub_text[cnt:len(text)])+"\n")
							break 
			
			if len(sub_text) > 0:
				sub_text_list = sub_text.split()
				
				for entry in sub_text_list:
					if not (is_first_line):
						index_file.write("\n")

					else:
						is_first_line = False
						

					entry = remove_leading_special_characters(entry)
					if (len(entry.strip()) > 0):
							index_file.write(str(entry.strip()))

def get_flags():
		return (sys.argv[1], sys.argv[2])

def is_non_numericals(text):
	return re.match('(?![0-9])', text)

def handle_punctuation(text, punctuation_handle_flag):
	if int(punctuation_handle_flag) > 0:
		text = re.sub('[_%\';.?@&+]', " ", text)
		text = re.sub('[!~`@#$%^&*/()_=+|\}{[\]/\\\\:;"\'?><,.]', "", text)
	return text

def remove_leading_special_characters(sub_text):
	while True:
		if len(sub_text) > 0:
			if re.match('[!~`@#$%^&*/()_=+|\}{[\]/\\\\:;"\'?><,\.-]', sub_text[0]):		
				sub_text = sub_text[1:]
			else:
				break
		else:
			break
	return sub_text
	
def eliminate_citations(text_part):
	return (re.sub('(\[\d\]|\[\d\d\]|\[\d\d\d\]|\[\d\d\d\d\])', '', text_part))

def eliminate_formulae_and_pronounciatino(all_contents):
	final_text = ""
	for para in all_contents:
		#eliminate formulae
		if para.find('math'):
			for spans in para.find_all('span'):
				for child_spans in para.find_all('span'):
					if child_spans.find('math'):
						spans.decompose()
						
		# eliminate pronounciation
		if para.find('a', href="/wiki/Help:IPA/English"):
			for spans in para.find_all('span'):
				for child_spans in para.find_all('span'):
					if child_spans.find('a', href="/wiki/Help:IPA/English"):
						spans.decompose()

		final_text += str(para.get_text())

	return final_text

if __name__ == "__main__":
	main()