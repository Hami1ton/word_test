aa = [[3, [2, 3, 2]], [1, [3, 5, 67]]]
ans = [[3, 2], [1, 67]]
bb = [0, 1]
# print([a[0] for a in aa])
#user_ans = [[a[0], a[1][b]]for [a, b] in [aa, bb]]
# user_ans = [a for a in aa for b in bb]
n = len(aa)
# enumerateとかでもっとスマードにかける
user_ans = [[aa[i][0], aa[i][1][bb[i]]] for i in range(n)]

print(user_ans)
