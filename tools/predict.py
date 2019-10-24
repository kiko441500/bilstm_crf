import argparse

from dl_segmenter import get_or_create

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description="执行命令行分词")
    # parser.add_argument("-s", "--text", help="要进行分割的语句")
    # parser.add_argument("-f", "--file", help="要进行分割的文件。", default="../data/restore.utf8")
    # parser.add_argument("-o", "--out_file", help="分割完成后输出的文件。", default="../data/pred_text.utf8")
    #
    # args = parser.parse_args()

    text="天上有无数个星星，那个最小的就是我。"
    file=None
    out_file=None
    # src_dict_path = "D:\\copus\\src_dict.json"  # 源字典路径
    # tgt_dict_path = "D:\\copus\\tgt_dict.json"  # 目标字典路径
    # config_save_path = "D:\\copus\\default-config.json"  # 模型配置路径
    # weights_save_path = "D:\\copus\\weights.01-0.05.h5"  # 模型权重保存路径

    #测试数据集
    src_dict_path = "D:\\copus\\src_dict.json"  # 源字典路径
    tgt_dict_path = "D:\\copus\\tgt_dict.json"  # 目标字典路径
    config_save_path = "D:\\copus\\test_icwb2\\default-config.json"  # 模型配置路径
    weights_save_path = "D:\\copus\\test_icwb2\\weights.01-0.04.h5"  # 模型权重保存路径


    tokenizer = get_or_create(config_save_path,
                              src_dict_path=src_dict_path,
                              tgt_dict_path=tgt_dict_path,
                              weights_path=weights_save_path)

    # text = args.text
    # file = args.file
    # out_file = args.out_file

    texts = []
    if text is not None:
        texts = text.split(' ')
        results = tokenizer.decode_texts(texts)
        print(results)

    elif file is not None:
        with open(file, encoding='utf-8') as f:
            texts = list(map(lambda x: x[0:-1], f.readlines()))

        if out_file is not None:
            with open(out_file, mode="w+", encoding="utf-8") as f:
                for text in texts:
                    seq, tag = tokenizer.decode_texts([text])[0]
                    f.write(' '.join(seq) + '\n')

