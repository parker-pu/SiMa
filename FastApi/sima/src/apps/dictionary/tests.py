# -*- coding: utf-8 -*-
import re

if __name__ == '__main__':
    a = ("CREATE TABLE `a1` (', '  `name` varchar(100) DEFAULT NULL', ') "
         "ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci")
    r = re.compile(r'(^.+\)) ENGINE.+$').findall(a)
    print(a)
    print(r)
