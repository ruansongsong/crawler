#coding: utf-8
import sys
import jieba
from boilerpipe.extract import Extractor
reload(sys)
sys.setdefaultencoding('utf-8')
extractor = Extractor(extractor='ArticleExtractor', url="http://news.scut.edu.cn/s/22/t/3/82/0a/info33290.htm")
processed_plaintext = extractor.getText()
highlighted_html = extractor.getHTML()
segList = jieba.cut(processed_plaintext, cut_all = False)
print "/".join(segList)
print processed_plaintext
