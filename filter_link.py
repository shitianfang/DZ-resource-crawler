from enum import Flag
from ip_pool import proxy_request
from discuz import DiscuzSpider
from process_text import match_url,filter_rule
from bs4 import BeautifulSoup
import re
import requests

def get_page_value(tid,domain):
    print("开始执行获取页面值")
    _test_links=[]
    _remove_repeat_set=set()
    spider=DiscuzSpider()
    # print(0)
    info = spider.parse(tid,domain)
    # print(1)
    if not info:
        # return {"introduce":"","value":""}  
        return None

    # if not info["content"]:
    if "content" not in info:
        info["content"]=""    

    if not info["comments"]:
        #  return {"introduce":info["content"],"value":""}   
        return None

    for comment in info["comments"]:
        _link=match_url(comment["content"],filter_rule)
        if _link:
            _test_links.append(_link)
    # print(2)
    _filter_links=list(filter(lambda _data:filter_valid_rule(_data,_remove_repeat_set),_test_links))
    
    print("获取页面值执行完成")
    if _filter_links: #{urls,text}
        print("过滤列表value：",_filter_links)
        text_list=[_["text"] for _ in _filter_links]
        print("text列表：",text_list)
        if not "content" in info:
            info["content"]=""
        return {"introduce":info["content"],"value":f"{'—'*30}".join(text_list)}   

def filter_valid_rule(data,_remove_duplication_set):
    print("开始执行过滤规则")
    flag=False
    for url in data["urls"]:
        if url not in _remove_duplication_set:
            _remove_duplication_set.add(url)
        else:
            continue
        
        print("过滤规则执行到匹配字符串")
        baiduyun_link_match = re.search('(https://pan.baidu.com/s/1.{22})',url,re.S)
        if baiduyun_link_match:
            raw_url = baiduyun_link_match.group(1)
            print("匹配成功")
            print(raw_url)
        else:
            return True
        
        print("过滤规则执行到链接测试")
        # resp=requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'})
        resp=proxy_request(url)
        if resp:
            # resp.encoding='utf-8'
            soup = BeautifulSoup(resp.text,'lxml')
            if soup.select('dl.pickpw.clearfix'):
                clearfix = soup.select('dl.pickpw.clearfix')[0]
                notice = clearfix.dt.string
                if '请输入提取码' in notice:
                    print('有效')
                    flag=True
            else:
                print('已经失效')
    print("过滤规则执行完成")
    return flag
    
            
if __name__=="__main__":
    # print()
    print(get_page_value(1208696,"www.52pojie.cn"))
    
    