from random import randint
def son_top(x):
    print(f'Men 1 dan {x} oralig\'ida 1 ta son o\'yladim. Shu sonni toping')
    a = randint(1,x)
    b = int(input('Javobingizni kiriting:'))
    i = 1
    while True:
        if a>b:
            print('Men bundan kattaroq son o\'ylaganman')
            b = int(input('Javobigiz:'))
        elif a<b:
            print('Men bundan kichikroq son o\'ylaganman')
            b = int(input('Javobingiz:'))
        else:
            print(f'To\'g\'ri topdingiz    men {a} ni o\'ylagan edim. Siz {i} ta urunishda topdingiz')
            return i
            break
        i+=1
def son_top_pc(x):
    input(f'Endi siz 1 dan {x} oralig\'ida son o\'ylang. o\'ylagan bo\'lsangiz Enterni bosing')
    a=randint(1,x)
    print(a)
    b=input('Agar men o\'ylagan son to\'g\'ri bo\'lsa [t] kiriting. Agar men o\'ylagan son siz o\'ylagan sondan kichik bo\'lsa [+] kiriting. Agar men o\'ylagan son siz o\'ylagan sondan katta bo\'lsa [-] kiriting.')
    i_c = 1
    while True:
        if b=='+':
            a+=1
            print(a)
        elif b == '-':
            a-=1
            print(a)
        else:
            print(f'Men siz o\'ylagan sonni {i_c} ta urunishda topdim') 
            return i_c
            break
        i_c += 1
        b=input('Agar men o\'ylagan son to\'g\'ri bo\'lsa [t] kiriting. Agar men o\'ylagan son siz o\'ylagan sondan kichik bo\'lsa [+] kiriting. Agar men o\'ylagan son siz o\'ylagan sondan katta bo\'lsa [-] kiriting.')
