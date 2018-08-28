# -*- coding:utf8 -*-

file = open('/Users/hexiaotian/Downloads/urls.txt', 'w+')
for lin in range(0, 100):
    print('www.958shop.com/cluNueu/0818%s.html' % lin)
    file.write('www.958shop.com/cluNueu/0818%s.html\n' % lin)
