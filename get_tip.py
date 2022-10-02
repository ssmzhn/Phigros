import re
import requests
from bs4 import BeautifulSoup
import json

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'Keep-Alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

raw_tip_html = requests.get('https://mzh.moegirl.org.cn/Phigros',headers=header).text


tip_table = BeautifulSoup(
    raw_tip_html, 'html.parser'
).find(
    attrs={'class':"mw-collapsible mw-collapsed wikitable"}
)
ol_list = tip_table.find_all('ol')

tip_info = {}
for x in ol_list:
    if not ('class' in x.attrs.keys() and x.attrs['class'] == ['references']):  # 可能会出错
        group_name = x.find_previous().get_text().strip()
        tips = []
        for y in x:
            if y.name == 'li':
                single_tip = y.get_text().strip()
                single_tip = re.sub(r'引用错误：没有找到(.*)标签','',single_tip)
                single_tip = re.sub(r'\[(.*?)\]','',single_tip)
                tips.append(single_tip)
        tip_info[group_name]=tips

with open('tips.json','w') as f:
    f.write(json.dumps(tip_info,indent=4,ensure_ascii=False))
