import re,sys
FONTS=sys.argv[1]
s=open('plakat-kapitel-02.src.html',encoding='utf-8').read().replace('/*FONTS*/',open(FONTS).read())
open('plakat-kapitel-02.html','w',encoding='utf-8').write(s)
