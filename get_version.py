import re
import requests
from bs4 import BeautifulSoup
import json
def str_quoted(s:str) -> str:
    str_list = []
    for x in s.splitlines():
        str_list.append('> '+x+'  ')
    return '\n'.join(str_list)
header = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'Keep-Alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

raw_version_html = requests.get('https://mzh.moegirl.org.cn/Phigros/%E8%B0%B1%E9%9D%A2%E4%BF%A1%E6%81%AF',headers=header).text
raw_log_html = requests.get('https://mzh.moegirl.org.cn/Phigros/%E6%9B%B4%E6%96%B0%E8%AE%B0%E5%BD%95',headers=header).text

ver_text = re.search(r'本页面现已更新至(?P<year>\d+)年(?P<month>\d+)月(?P<day>\d+)日更新的(?P<version>.*)版本。',raw_version_html)

ver_log_beautifulsoup = BeautifulSoup(
        raw_log_html, 'html.parser'
).find(
        attrs={'class':"mf-section-1 collapsible-block"}
)
ver_log = ver_log_beautifulsoup.get_text()
ver_log = re.sub(r'\[\d+\]?','',ver_log).strip()
#print('Phi 当前版本:',ver_text.group('version'))
#print('Phi 更新日期:',ver_text.group('year'))
year = int(ver_text.group('year'))
month = int(ver_text.group('month'))
day = int(ver_text.group('day'))
date = {
    'year':year,
    'month':month,
    'day':day
}
info = {
    'version':ver_text.group('version'),
    'date':date,
    'log':ver_log
}
with open('version_info.json','w') as f:
    f.write(json.dumps(info,indent=4,ensure_ascii=False))

readme = open('README.md').read()
readme = re.sub(r'<!-- begin Phigros version -->(.*)<!-- end Phigros version -->',r'<!-- begin Phigros version --> `{}` <!-- end Phigros version -->'.format(ver_text.group('version')),readme)
readme = re.sub(r'<!-- begin Phigros log -->(.*)<!-- end Phigros log -->',r'<!-- begin Phigros log -->\n{}\n<!-- end Phigros log -->'.format(str_quoted(ver_log)),readme,flags=16)
readme = re.sub(r'<!-- begin Phigros time -->(.*)<!-- end Phigros time -->',r'<!-- begin Phigros time --> {}.{}.{} <!-- end Phigros time -->'.format(year,month,day),readme)
with open('README.md','w') as f:
    f.write(readme)
