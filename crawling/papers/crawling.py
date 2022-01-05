# coding=utf-8
import requests
import traceback
from lxml import etree
from tqdm import tqdm

# An example on CVPR 2021
# 创建类
class Craw:
    def __init__(self): #初始化实例属性，self继承，为形式参数
        self.url = "https://openaccess.thecvf.com/CVPR2021?day=all"
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30"}
        self.html_list = []

    def getList(self):
        response = requests.get(self.url, headers=self.header) # 发送GET请求
        html_body = etree.HTML(response.text) #调用HTML类对HTML文本进行初始化，成功构造XPath解析对象，同时可以自动修正HMTL文本（标签缺少闭合自动添加上）
        title = html_body.xpath("//dt[@class='ptitle']/a/@href")#使用路径表达式在 XML 文档中选取节点。节点是通过沿着路径或者 step 来选取
        #//:从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置（取子孙节点）;/:从根节点选取（取子节点）;@:选取属性
        #选取所有 dt 元素，且这些元素拥有值为 ptitle 的 class 属性,接着从a节点中的子元素再选取属于前者的子元素的所有拥有href属性的元素
        for item in title: #list
            self.html_list.append("http://openaccess.thecvf.com" + item)

    def getPaper(self, url):
        list=[]
        with open('test.tsv', 'a', encoding='utf8') as f: #a:只能写
            try:
                response = requests.get(url, headers=self.header)
                body = etree.HTML(response.text)
                title = body.xpath("//div[@id='papertitle']/text()")[0] #选取此节点中的所有文本
                #不加[],title类型为list，而加[],类型为lxml.etree._ElementUnicodeResult
                abstract = body.xpath("//div[@id='abstract']/text()")[0]
                down_url = body.xpath("//div[@id='content']//a/@href")[0]#.replace("../../", "http://openaccess.thecvf.com/")
                #选择属于前者元素的后代的所有a元素，而不管它们位于前者之下的什么位置
                list.append("http://openaccess.thecvf.com" + down_url)

                title = title.strip().replace('\t', ' ').replace('\n', ' ') #2021
                abstract = abstract.strip().replace('\t', ' ').replace('\n', ' ').replace('Abstract: ', '')
                #text = title + '\t' + down_url + '\t' + abstract + '\n'
                text = title + '\t' + list[0] + '\t' + abstract + '\n' # only 2021
                f.write(str(text))

            except Exception as e:
                #print(e)
                traceback.print_exc() #可以很清楚的看出哪个文件哪个函数哪一行的报错，方便调试

    def run(self):
        self.getList()
        #idex = len(self.html_list)
        for_tqdm = tqdm(enumerate(self.html_list), total=len(self.html_list))
        #for i in tqdm(range(idex)):
        for i, url in for_tqdm:
            self.getPaper(url)

if __name__ == '__main__':
    with open('test.tsv', 'w', encoding='utf8') as f:
        f.write('\t'.join(['title', 'link', 'abstract']) + '\n')
    crawlist = Craw()
    crawlist.run()
    # 36min
