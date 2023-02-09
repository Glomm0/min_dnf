import math


def to_term(bin_str):
    term = ""
    for i in range(len(bin_str)):
        if bin_str[i] == "0":
            term += f'-x{i + 1}'
        if bin_str[i] == "1":
            term += f'x{i + 1}'

    return term

def to_bin(vect):
    pos = 0
    values = []
    for k in vect:
        if k == "1":
            bin_str = bin(pos)[2:]
            bin_str = bin_str.zfill(int(math.log2(len(vect))))
            values.append(bin_str)

        pos += 1
    return values


def group_by_ones(values):
    sorted_by_ones = []
    for i in range(0, int(math.log2(len(vect))+1)):
        for k in values:
            if k.count("1") == i:
                sorted_by_ones.append(k)

    return sorted_by_ones


def merge_neighbors(values):
    merged = []
    n = [False for x in range(len(values))]

    for i in range(len(values)-1):

        for k in range(i+1, len(values)):
            if abs(values[k].count("1") - values[i].count("1")) == 1:
                cnt = 0

                for j in range(len(values[k])):
                    if values[k][j] != values[i][j]:
                        index = j
                        cnt += 1
                if cnt == 1:

                    if not n[i] or not n[k]:
                        n[i] = True
                        n[k] = True
                    put = list(values[i])
                    put[index] = '_'
                    merged.append(''.join(put))
        if not n[i]:
            merged.append(values[i])
        if not n[len(values) - 1]:
            merged.append(values[len(values) - 1])

    check = n.count(False)
    merged = del_same(merged)
    return merged, check


def del_same(values):
    un = []
    for i in values:
        if i not in un:
            un.append(i)
    return un


def to_dnf(values):
    dnf = ""
    for i in values:
        dnf += to_term(i) + " V "
    return dnf[:-2]


def check(values):
    bin_set = to_bin(vect)
    checked = []
    c_map = []
    for i in range(len(bin_set)):
        temp = []
        for j in range(len(values)):
            temp.append('0')
        c_map.append(temp)

    lng = len(c_map[0])

    for b in range(len(bin_set)):
        for i in range(len(values)):
            stroke_pos = []
            for j in range(len(values[i])):
                if values[i][j] == '_':
                    stroke_pos.append(j)

            temp = list(bin_set[b])
            for ind in stroke_pos:
                temp[ind] = '_'
            temp = ''.join(temp)
            if values[i] == temp:
                c_map[b][i] = '1'

    for ln in range(len(c_map)):
        if c_map[ln].count('1') == 1:
            #print(c_map)
            one_pos = ''.join(c_map[ln]).find('1')
            #print(one_pos)
            checked.append(values[one_pos])
            values[one_pos] = '0'
            for ln2 in range(len(c_map)):
                if c_map[ln2] != '0' and c_map[ln2][one_pos] == '1':
                    #print(ln)
                    c_map[ln2] = '0'

    l = []

    for i in range(lng):
        st = ""
        for ln in c_map:
            if ln != '0':
                st += ln[i]
        l.append(st)

    mnn = len(values) + 1
    mnl = []

    #print(l)
    for i in range(len(l) - 1):
        st = list(l[i])
        prov = []
        if values[i] != '0':
            prov.append(values[i])

        for j in range(i + 1, len(l)):
            cnt = 0
            for k in range(len(l[i])):
                if l[i][k] == '1' and l[j][k] == '0' or l[i][k] == '0' and l[j][k] == '1':
                    cnt += 1
                    st[k] = '1'
                    temp = list(l[i])
                    temp[k] = '1'
                    l[i] = ''.join(temp)
                    if values[j] not in prov and values[j] != '0':
                        prov.append(values[j])
            if cnt == len(l[i]):
                prov.clear()
                if values[i] != '0':
                    prov.append(values[i])
                if values[j] != '0':
                    prov.append(values[j])
                break

            if st.count('1') == len(l[i]):
                break
        #print(st)
        #print(prov)
        #print(mnn)
        if len(prov) != 0 and len(prov) < mnn and st.count('1') == len(l[i]):
            mnl = prov
            mnn = len(prov)

    for x in mnl:
        checked.append(x)

    while checked.count('0') > 0:
        checked.remove('0')
    #print(checked)
    #print(l)
    #print(c_map)
    return checked


print("Введите вектор функции")
vect = input()

values = to_bin(vect)
merged = group_by_ones(values)
n = 0

while True:
    l = len(merged)
    if n == l:
        break
    merged, n = merge_neighbors(merged)

merged = check(merged)
formula = to_dnf(merged)
print("Минимизированная ДНФ: ", formula)

input()
