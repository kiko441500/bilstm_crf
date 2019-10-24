# import re
# from keras.utils import to_categorical
#
# def process_line_msr_pku(l):
#     decoded_line = l.strip().split(' ')
#     return [w.strip('\r\n') for w in decoded_line]
#
#
# def _process_text_files(decoded_line):
#     # Create possible tags for fast lookup 可能的词标签
#     possible_tags = []
#     for i in range(1, 300):
#         if i == 1:
#             possible_tags.append('s')
#         else:
#             possible_tags.append('b' + 'm' * (i - 2) + 'e')
#
#     inputs = []
#     target = []
#
#     last_isalpha_num = False
#     pos_tag = []
#     final_line = []
#
#     decoded_line = process_line_msr_pku(decoded_line)
#     for w in decoded_line:
#         is_alphanum = bool(re.match('^[a-zA-Z0-9]+$', w))  # 如果w中有字母或者数字的话，就不是中文了
#
#         if not is_alphanum:
#             # if this round is chinese and last round is alphanum,
#             # append the last alphanum's target: s and continue
#             if last_isalpha_num:
#                 pos_tag.append('s')
#
#             if w and len(w) <= 299:
#                 final_line.extend(list(w))
#                 pos_tag.extend(list(possible_tags[len(w) - 1]))
#                 last_isalpha_num = False
#         else:  # 如果当前是
#             if last_isalpha_num:  # 如果上一个是数字
#                 final_line[-1] += w
#             else:  # 如果上一个是中文
#                 final_line.append(w)
#                 last_isalpha_num = True
#
#     if last_isalpha_num:
#         pos_tag.append('s')
#
#         # decode_str = ''.join(final_line)
#
#         # pos_tag_str = ''.join(pos_tag)
#
#     if len(pos_tag) != len(final_line):
#         # print(filename)
#         # print('Skip one row. ' + pos_tag + ';' + final_line)
#         # continue
#         pass
#
#     inputs.append(final_line)
#     target.append(pos_tag)
#
#     # print(inputs)
#     # print(target)
#     return inputs, target
#
# a = "中共中央  总书记  、  国家 1984  主席  江  泽民  "
# m,n = _process_text_files(a)

import  sys
print(sys.path)