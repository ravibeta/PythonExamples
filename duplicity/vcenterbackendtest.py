from vcenterbackend import CustomMethodRequest
from vcenterbackend import vCenterBackend
parsed_url = "https://vcd-sj-lab5-vc.corp.adobe.com/folder/vse-rajamani%40adobe.com-592-859915877-1_+%28d72f80d2-e893-4cc1-b1e4-787f95fda0a3%29-0%2Fvse-rajamani%40adobe.com-592-859915877-1_+%28d72f80d2-e893-4cc1-b1e4-787f95fda0a3%29-0.vmdk?dcPath=sj1&dsName=HDS005_CORP_0058"
vcb = vCenterBackend(parsed_url)
vcb._connect()
remote_filename = parsed_url[parsed_url.index('%2F')+3:parsed_url.index('?')]
print('remote_filename='+remote_filename)
local_path="/root/duplicity/folder2"
vcb.get(remote_filename, local_path)
