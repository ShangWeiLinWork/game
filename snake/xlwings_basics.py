# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import xlwings as xw


# book -> sheet -> cell
book = xw.Book()

sheet = book.sheets[0]

sheet.name = 'test sheet'

sheet['A1'].value = 'my cell'# cell name in excel convention, i.e. count form 1
# sheet.range('D1').value = 'CCC' # alternative method

sheet['A2:D3'].value = 'AAA'
sheet[3:5, 4:6].value = 'ccc'
# sheet[(7, 7), (7, 8)].value = 'ddd' # This doesn't work

sheet[(0, 5)].value = 'BBB' # (3, 7) in Python convention, i.e. count from 0

sheet['E1'].color = (255, 0, 0)# (r, g, b), 0~255

while True:
    print(book.selection.address)#$A$1