from page_batch import get_block_page
from storage import save_data

get_block_page(8,"www.52pojie.cn",save_data,start_page=300,last_page=320,interval=20)
print("总执行完成")

