''' given stopwords file has every word in a new line which might have
    newline characters and other noise. So, this utility cleans up all
    and write all the stopwords in a single line separated by spaces
'''

from utils import properties

def regenerate_stop_words():
    output_file = open(properties.formatted_stop_words_file, 'w')

    with open(properties.given_stop_words_file, 'r') as file:
        all_lines = file.readlines()
        for line in all_lines:
            output_file.write(line.strip() + " ")

    output_file.close()

regenerate_stop_words()
