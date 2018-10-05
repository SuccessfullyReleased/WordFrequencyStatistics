import re


def process_file(path):
    try:
        with open(path, 'r') as file:
            text = file.read()
            text = re.sub('[^a-zA-Z0-9n]', ' ', text).lower()
    except IOError:
        print("Read File Error!")
        return None
    return text


def get_dict_value(word_freq={}, keys=[]):
    if type(keys).__name__ == 'str':
        return word_freq[keys]
    else:
        count = len(keys)
        if count == 0:
            return word_freq
        elif count == 1:
            return word_freq[keys[0]]
        elif count == 2:
            return word_freq[keys[0]][keys[1]]
        elif count == 3:
            return word_freq[keys[0]][keys[1]][keys[2]]
        else:
            string = "word_freq['"
            string += "']['".join(keys)
            string += "']"
            return eval(string)


def process_buffer(textString, num=3):
    if textString:
        word_freq = {}
        word_list = textString.split()
        if num == 1:
            for word in word_list:
                if word in word_freq:
                    word_freq[word] += 1
                else:
                    word_freq[word] = 1
        else:
            count = len(word_list)
            i = 0
            while i < count:
                finish = i
                start = i - num + 1
                if start < 0:
                    start = 0
                index = i
                while index >= start:
                    if word_list[i] in get_dict_value(word_freq, word_list[index: finish]).keys():
                        get_dict_value(word_freq, word_list[index: finish])[word_list[i]]['Value'] += 1
                    else:
                        get_dict_value(word_freq, word_list[index: finish]).update({word_list[i]: {'Value': 1}})
                    index -= 1
                i += 1

        return word_freq


def format_dict(word_freq={}, num=3):
    formated_word_freq = {}
    if num == 1:
        for word in word_freq.keys():
            formated_word_freq[word] = word_freq[word]['Value']
    else:
        phrases = []
        for word in word_freq.keys():
            phrases.append(word)
        while len(phrases) > 0:
            phrase = phrases[0]
            if len(get_dict_value(word_freq, phrase)) == 1 and type(phrase).__name__ == 'list':
                formated_word_freq[' '.join(phrase)] = get_dict_value(word_freq, phrase)['Value']
            else:
                for nextword in get_dict_value(word_freq, phrase):
                    temp = []
                    if type(phrase).__name__ == 'str':
                        temp.append(phrase)
                    else:
                        temp.extend(phrase)
                    if nextword != 'Value':
                        temp.append(nextword)
                        phrases.append(temp)
            phrases.pop(0)

    # print(formated_word_freq)
    return formated_word_freq


def output_result(word_freq):
    if word_freq:
        sorted_word_freq = sorted(word_freq.items(), key=lambda v: v[1], reverse=True)
        for item in sorted_word_freq[:10]:
            print(item)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('num')
    args = parser.parse_args()
    path = args.path
    num = int(args.num)
    buffer = process_file(path)
    if buffer:
        word_freq = process_buffer(buffer, num)
        if num != 1:
            word_freq = format_dict(word_freq, num)
        output_result(word_freq)
