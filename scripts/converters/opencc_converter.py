from opencc import OpenCC

cc = OpenCC("s2t")


def to_traditional(text):
    """
    简体转换为繁体
    """
    if not text:
        return text

    return cc.convert(text)
