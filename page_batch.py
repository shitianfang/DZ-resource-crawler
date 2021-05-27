from filter_link import get_page_value
from ip_pool import proxy_request
from pyquery import PyQuery as pq
from tools import extractData
from async_pool import thread_executor
from concurrent.futures import wait,ALL_COMPLETED
from threading import Thread
from model import Mark,DBSession


def get_block_page(bid,domain,callback,start_page=2,last_page=10,is_thread=True,interval=20):
    # all_task=[thread_executor.submit(execute_task,bid,domain,callback,i) for i in range(start_page,last_page)]
    count=0
    while True:
        temp=[Thread(target=execute_task,args=(bid,domain,callback,i)) for i in range(start_page+count*interval,last_page+count*interval)]
    # print(all_task)
    # for task in all_task:
    #     task.add_done_callback(executor_callback)
    # # 等待执行完成
    # wait(all_task,return_when=ALL_COMPLETED)
        for t in temp:
            t.start()
    
        for t in temp:
            t.join()
        count+=1

def executor_callback(worker):
    exception=worker.exception()
    if exception:
        print(exception)
        
def execute_task(bid,domain,callback,page):
    session=DBSession()
    print(f"正在执行page{page}")
    url=f"https://{domain}/forum-{bid}-{page}.html"
    resp=proxy_request(url)
    # resp.encoding="utf-8"
    if resp:
        doc=pq(resp.text)
    else:
        print("未获取到列表页")
        return 
    # print(f"{page}a标签",list(doc(".s.xst").items()))
    for a in doc(".s.xst").items():
        print(f"执行  {a.text()}")
        pid=extractData(f"thread-(.*)-1-{page}.html",a.attr.href)
        
        print("pid",pid)
        if pid=="0":
            pid=extractData(f"thread-(.*)-1-1.html",a.attr.href)
            print(f"第{page}页出错，标题：{a.text()}",f"出错后获取到pid {pid}")

        

        with session.no_autoflush:
            session.merge(Mark(id=pid))  
            if session.query(Mark).filter(Mark.id==pid).first():
                continue

        page_value=get_page_value(pid,domain)
        if not page_value:
            print("没有获取到页值")
            continue
        if not page_value["value"]:
            continue
        if page_value["value"].isspace():
            continue

        title=a.text()
        introduce=page_value["introduce"]
        value=page_value["value"] 
        
        callback({"id":pid,"title":title,"introduce":introduce,"value":value},session)  
        
        

        
        


if __name__=="__main__":
    # get_block_page(8,"www.52pojie.cn")
    pass