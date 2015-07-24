import os
import sqlite3
import csv

conn = sqlite3.connect('C:/Repos/HAG/data/hag_50_51_GISRUK2015_comp_CD.sqlite')
cur = conn.cursor()

res_lst = []
rd_full = cur.execute('SELECT DistCode, COUNT(*) FROM Ttb GROUP BY DistCode').fetchall()
rd_opt = cur.execute('SELECT DistCode, COUNT(*) FROM Ttb WHERE DistCode = AssignedCode GROUP BY DistCode').fetchall()
for rd in rd_full:
    res_lst.append((rd[0], rd[1], 0))

for rd in rd_opt:
    rd_tup = [item for item in res_lst if rd[0] in item]
    rd_ind = [x[0] for x in res_lst].index(rd_tup[0][0])
    res_lst[rd_ind] = (rd[0], rd_tup[0][1], rd[1])

print(res_lst)


with open('eval_measures_CD.csv','wb') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['RD_CODE','RD_FREQ', 'RD_FREQ_M'])
    for row in res_lst:
        csv_out.writerow(row)