import requests
# import grequests
import random
import urllib
import threading

ip_num_max=3
ip_num_min=2
every_add_ip=2

ip_set_pool=[]
request_sessions={}
ip_error_count={}

lock=threading.Lock()

def add_ip_pool():
    global ip_set_pool
    # resp=requests.get(f"http://1591563999731191646.standard.hutoudaili.com/?num={every_add_ip}&area_type=1&scheme=1&anonymity=3&order=3")
    # resp=requests.get(f"http://ip.memories1999.com/api.php?dh=1589974848562191646&sl={every_add_ip}&xl=国内")
    # resp=requests.get(f"http://api.shenlongip.com/ip?key=57qrz908&pattern=txt&count={every_add_ip}&split=%5Cn&protocol=2")
    resp=requests.get(f"http://http2.9vps.com/getip.asp?username=132666&pwd=bc786493e0df940273aa6c4a5572a6eb&geshi=1&fenge=3&fengefu=&getnum=30")
    ip_set_pool.extend([ip for ip in resp.text.split("\n") if (ip and ":" in ip)])
    print(ip_set_pool)
        

def get_mul_ip(num):
    global ip_set_pool
    if num>ip_num_max:
        num=ip_num_max
    return random.sample(ip_set_pool,num)

def get_ip():
    global ip_set_pool
    return random.choice(ip_set_pool)

# 这里如果不用死锁的话会导致线程出错
def del_ip(ip):
    global ip_set_pool
    
    # print(f"ip请求次数{ip_error_count.get(ip,0)}")
    if ip_error_count.get(ip,0)>10:
        if ip in ip_set_pool:
            lock.acquire()
            ip_set_pool.remove(ip)
            del ip_error_count[ip]
            lock.release()
            print(f"代理请求出错了，删除IP {ip}")
    else:
        ip_error_count[ip]=(ip_error_count.get(ip,0)+1)
       
        if ip_size(ip_set_pool)<ip_num_max:
            add_ip_pool() 
    
    if ip_size(ip_set_pool)<ip_num_min:
        print("添加IP")
        add_ip_pool()

def ip_size(ip_pool):
    lock.acquire()
    size=len(ip_pool)
    lock.release()
    return size
    

def proxy_request(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'},timeout=5,**kwargs):
    #临时标记，用完删除
    if url=="https://www.52pojie.cn/thread-0-1-1.html":
        return None
    
    domain=urllib.parse.urlparse(url).netloc
    if domain in request_sessions:
        allot_session=request_sessions[domain]
    else:
        allot_session=requests.Session()
        proxies={"https":get_ip()}
        allot_session.proxies.update(proxies)
        request_sessions[domain]=allot_session

    retry_count=5
    while retry_count>0:
        try:
            resp=allot_session.get(url,headers=headers,timeout=timeout)
            if resp.status_code == 200:
                return resp
            else:
                _ip=allot_session.proxies["https"]

                del_ip(_ip)
    
                proxies={"https":get_ip()}
                allot_session.proxies.update(proxies)
                print("错误页面",url)
                
                resp.encoding="utf-8"
                print(resp.text)
        except Exception as e:
            retry_count-=1
            _ip=allot_session.proxies["https"]
            del_ip(_ip)
            proxies={"https":get_ip()}
            allot_session.proxies.update(proxies)
            print("代理请求出异常了，删除IP",str(e))
            # print(e)

# def proxy_request(url,headers={},timeout=5,**kwargs):
    
#     retry_count=5
#     while retry_count>0:
#         _ip=get_ip()
#         try:
#             resp=requests.get(url,proxies={"https":_ip},headers=headers,timeout=timeout)
#             if resp.status_code == 200:
#                 return resp
#             else:
#                 del_ip(_ip)
#                 print(url)
#                 print("代理请求出错了，删除IP")
#                 resp.encoding="utf-8"
#                 print(resp.text)
#         except Exception as e:
#             retry_count-=1
#             del_ip(_ip)
#             print("代理请求出错了，删除IP")
#             print(e)

def grequest_error_handle(_request, exception):
    print("异步代理请求出错了")
    print(_request.url)
    print(exception)
    

# def proxy_grequest(urls,size=10): #size为并发数
#     # print(urls)
#     reqs = []
#     for url in urls:
#         _ip=get_ip()
#         _grequest=grequests.get(url)
#         _grequest.session.proxies={"https":_ip}
#         _grequest.session.keep_alive=False
#         reqs.append(_grequest)
#     resps = grequests.map(reqs, size=size,exception_handler=grequest_error_handle)  
#     return resps #返回response列表


add_ip_pool()