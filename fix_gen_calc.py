with open('gen_calc_doc.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = "P('Với i = 10%/năm và f = 3%/năm:')\nFORMULA('r = (1 + 0,10) / (1 + 0,03) − 1 = %s%%' % vn(r_real * 100, 2))"
replace = "P('Với i = 8%/năm và f = 2%/năm:')\nFORMULA('r = (1 + 0,08) / (1 + 0,02) − 1 = %s%%' % vn(r_real * 100, 2))"

if target in content:
    content = content.replace(target, replace)
    with open('gen_calc_doc.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated gen_calc_doc.py successfully!')
else:
    print('Target not found')

