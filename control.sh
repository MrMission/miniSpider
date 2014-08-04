#! /bin/sh
python crawl/crawler.py http://detail.zol.com.cn/notebook_index/subcate16_list_1.html &
python parse/parser.py rest_nootbook &
python storage/storage.py rest_nootbook
