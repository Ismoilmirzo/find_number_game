from functions import son_top, son_top_pc
while True:
    i=son_top(10)
    i_c=son_top_pc(10)
    print(f'Siz {i} ta urunishda topdingiz. Men {i_c} ta urunishda topdim')
    if i<i_c:
        print('Siz yutdingiz')
    elif i>i_c:
        print('Men yutdim :)')
    else:
        print('Durrang')
    re = input('Yana o\'ynaymizmi? yes/no')
    if re == 'no':
        break
