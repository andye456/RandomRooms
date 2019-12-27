a=[[1,2,3,4,5],[2,3,4,5,6],[3,4,5,6,7],[4,5,6,7,8],[5,6,7,8,9]]

for i in a:
    for j in i:
        print('{:4}'.format(j), end='')
        # print(str(i)+" "+str(j)+"|", end='')

    print()
