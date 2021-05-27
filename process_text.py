import re

def match_url(text,func):
    print("开始执行页面匹配")
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[\u4e00-\u9fa5]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+') # 匹配模式
    urls = re.findall(pattern,text)
    print("页面匹配完成")
    if urls:
        # print(urls)
        return {"urls":list(filter(func,urls)),"text":text}


def filter_rule(url):
    if "transfer/send" in url:
        return False

    if "52pojie" in url:
        return False

    return True

if __name__=="__main__":
    text = '还有一点就是 你这个不好申述的原因就是  弄你号的人 长期登录 已经取得服务器信任了 就好像我现在改密码 连原始密码都不需要了'
    print(match_url(text,filter_rule))