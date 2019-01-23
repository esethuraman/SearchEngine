import sys
import re
from utils import CommonUtils
punctuation_handle_flag = True
casefold_handle_flag = True

# GIVEN: text to parse and a flag that indicates whether stopping has to be performed
# RETURNS: a string with each term in the document separated by spaces
def parse_and_tokenize(entire_text, is_stopping_needed):
    tokenized_string = ""

    # eliminating the digits at the end of files
    entire_text = re.sub('\d+\t\d+\t\d+', '', entire_text)

    if int(casefold_handle_flag) > 0:
        entire_text = entire_text.casefold()

    entire_text = entire_text.replace('\n', ' ')
    text_parts = entire_text.split(' ')

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
                cnt = len(sub_text) - 1
                if is_non_numericals(sub_text[cnt]):
                    for j in range(len(sub_text)):
                        local_match = is_non_numericals(sub_text[cnt])
                        if local_match:
                            cnt -= 1
                        else:
                            non_numerical_part = handle_punctuation(text[(cnt + 1):len(text)], punctuation_handle_flag)

                            if (non_numerical_part.startswith('-')):
                                non_numerical_part = remove_leading_special_characters(non_numerical_part)

                            if len(non_numerical_part.strip()) > 0:
                                non_numerical_part = "\n" + non_numerical_part

                            sub_text = (sub_text[0:(cnt + 1)]) + non_numerical_part
                            break

            if len(sub_text) > 0:
                sub_text_list = sub_text.split()

                for entry in sub_text_list:
                    # if is_stopping_needed and (entry.strip() not in CommonUtils.get_stop_words():
                    if is_stopping_needed:
                        if (entry.strip() in CommonUtils.get_stop_words()):
                            continue

                    if not (is_first_line):
                        tokenized_string += " "

                    else:
                        is_first_line = False

                    entry = remove_leading_special_characters(entry)
                    if (len(entry.strip()) > 0):
                        tokenized_string += str(entry.strip())
    return tokenized_string

#Matches everything except numbers
def is_non_numericals(text):
    return re.match('(?![0-9])', text)

#Removes all the punctuation
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
