# 产生指定长度的验证码，验证码由大小写字母和数字构成

import random


def main(code_len=4):
    all_chrs = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    last_pos = len(all_chrs) - 1
    code = ''
    for _ in range(code_len):
        index = random.randint(1, last_pos)
        code += all_chrs[index]
    return code


if __name__ == '__main__':
    out_code = main(6)
    print(out_code)
