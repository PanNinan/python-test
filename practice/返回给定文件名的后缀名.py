# 返回给定文件名的后缀名


def get_suffix(file_name, has_dot=False):
    dot_pos = file_name.rfind('.')
    if 0 < dot_pos < len(file_name):
        index = dot_pos if has_dot else dot_pos + 1
        return file_name[index:]
    else:
        return ''


if __name__ == '__main__':
    print(get_suffix('xxx.avi'))
    print(get_suffix('xxx.avi', True))
    print(get_suffix('..aviu'))
