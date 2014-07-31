#! /bin/sh
python crawl/crawler.py http://detail.zol.com.cn/tablepc/
python parse/parser.py tablepc
python storage/storage.py tablepc
