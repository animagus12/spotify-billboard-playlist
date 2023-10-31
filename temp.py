names1 = ['Amit', 'Ben', 'Charlie', 'Damon']
names2 = names1
names3 = names1[:]
names2[0] = 'Stefan'
names3[1] = "John"
sum = 0
for ls in (names1, names2, names3):
    if ls[0] == "Stefan":
        sum += 1
    if ls[1] == "John":
        sum += 10
print(sum)