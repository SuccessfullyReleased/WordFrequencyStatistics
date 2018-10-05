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
    """如果keys为字符串,返回word_freq字典中以keys为键的值。
    如果keys为列表,则使用eval()函数进行字符串拼接，深度查找word_freq字典中以keys为键的值。"""
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
    """当只统计单词时（num == 1），生成<str,int>形式的键值对,
    当统计短语时，生成字典套字典的形式，具体参考sample.json文件"""
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


def format_dict(word_freq={}):
    """对统计短语的情况生成的复杂字典进行格式化，格式化后的形式为<str,int>"""
    formated_word_freq = {}
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
            word_freq = format_dict(word_freq)
        output_result(word_freq)
