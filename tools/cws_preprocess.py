import re


def process_line_msr_pku(l):
    decoded_line = l.strip().split(' ')
    return [w.strip('\r\n') for w in decoded_line]


def _process_text_files(decoded_line):
    # Create possible tags for fast lookup 可能的词标签
    possible_tags = []
    for i in range(1, 300):
        if i == 1:
            possible_tags.append('s')
        else:
            possible_tags.append('b' + 'm' * (i - 2) + 'e')

    inputs = []
    target = []

    last_isalpha_num = False
    pos_tag = []
    final_line = []


    for w in decoded_line:
        is_alphanum = bool(re.match('^[a-zA-Z0-9]+$', w))  # 如果w中有字母或者数字的话，就不是中文了

        if not is_alphanum:
            # if this round is chinese and last round is alphanum,
            # append the last alphanum's target: s and continue
            if last_isalpha_num:
                pos_tag.append('s')

            if w and len(w) <= 299:
                final_line.extend(list(w))
                pos_tag.extend(list(possible_tags[len(w) - 1]))
                last_isalpha_num = False
        else:  # 如果当前是
            if last_isalpha_num:  # 如果上一个是数字
                final_line[-1] += w
            else:  # 如果上一个是中文
                final_line.append(w)
                last_isalpha_num = True

    if last_isalpha_num:
        pos_tag.append('s')

        # decode_str = ''.join(final_line)

        # pos_tag_str = ''.join(pos_tag)

    if len(pos_tag) != len(final_line):
        # print(filename)
        # print('Skip one row. ' + pos_tag + ';' + final_line)
        # continue
        pass

    inputs.append(final_line)
    target.append(pos_tag)

    # print(inputs)
    # print(target)
    # return inputs, target
    m = list(zip(inputs[0],target[0]))
    return m
import os
import re
import argparse

def print_process(process):
    num_processed = int(30 * process)
    num_unprocessed = 30 - num_processed
    print(
        f"{''.join(['['] + ['='] * num_processed + ['>'] + [' '] * num_unprocessed + [']'])}, {(process * 100):.2f} %")


def convert_to_bis(source_dir, target_path, log=False, combine=False, single_line=True):
    print("Converting...")
    for root, dirs, files in os.walk(source_dir):
#root 所指的是当前正在遍历的这个文件夹的本身的地址
#dirs 是一个 list ，内容是该文件夹中所有的目录的名字(不包括子目录)
#files 同样是 list , 内容是该文件夹中所有的文件(不包括子目录)
        total = len(files)
        tgt_dir = target_path + root[len(source_dir):]

        print(tgt_dir)
        for index, name in enumerate(files):
            file = os.path.join(root, name)
            bises = process_file(file)
            if combine:
                _save_bises(bises, target_path, write_mode='a', single_line=single_line)
            else:
                os.makedirs(tgt_dir, exist_ok=True)
                _save_bises(bises, os.path.join(tgt_dir, name), single_line=single_line)
            if log:
                print_process((index + 1) / total)

    print("All converted")


def _save_bises(bises, path, write_mode='w+', single_line=True):
    with open(path, mode=write_mode, encoding='UTF-8') as f:
        if single_line:
            for bis in bises:
                sent, tags = [], []
                for char, tag in bis:
                    sent.append(char)
                    tags.append(tag)
                sent = ' '.join(sent)
                tags = ' '.join(tags)
                f.write(sent + "\t" + tags)
                f.write('\n')
        else:
            for bis in bises:
                for char, tag in bis:
                    f.write(char + "\t" + tag + "\n")
                f.write("\n")


def process_file(file):
    with open(file, 'r', encoding='UTF-8') as f:
        text = f.readlines()
        bises = _parse_text(text)
    return bises


def _parse_text(text: list):
    bises = []
    for line in text:
        # remove POS tag
        line, _ = re.subn('\\n', '', line)#(pattern,replacement,text)
        if line == '' or line == '\n':
            continue
        words = re.split('\s+', line)#'\s'表示空格，+表示一个或者多个

        if len(words) > 150:#如果一句话中的词多于150个
            texts = re.split('[。？！，.?!,]/w', line)
            if len(min(texts, key=len)) > 150:#如果最短的文本长度多于150
                continue
            bises.extend(_parse_text(texts))
        else:#如果一句话中的词不多余150个则直接append
            bises.append(_tag(words))
    return bises


def _tag(words):
    """
    给指定的一行文本打上BIS标签
    :param line: 文本行
    :return:
    """
    bis = []
    bis = _process_text_files(words)
    return bis


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description="将使用词性标注的文件转换为用BIS分块标记的文件。")
    # parser.add_argument("corups_dir", type=str, help="指定存放语料库的文件夹，程序将会递归查找目录下的文件。")
    # parser.add_argument("output_path", type=str, default='.', help="指定标记好的文件的输出路径。")
    # parser.add_argument("-c", "--combine", help="是否组装为一个文件", default=False, type=bool)
    # parser.add_argument("-s", "--single_line", help="是否为单行模式", default=False, type=bool)
    # parser.add_argument("--log", help="是否打印进度条", default=False, type=bool)
    # parser.add_argument("--max_len", help="处理后的最大语句长度（将原句子按标点符号断句，若断句后的长度仍比最大长度长，将忽略",
    #                     default=150, type=int)
    # args = parser.parse_args()
    # MAX_LEN_SIZE = args.max_len

    # convert_to_bis(args.corups_dir, args.output_path, args.log, args.combine, args.single_line)
    convert_to_bis("D:\\copus\\test_icwb2\\corpus" , "D:\\copus\\test_icwb2\\processed_data", True,True,True)

