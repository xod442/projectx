import json


f = open("da5id_data.txt", "r")
while True:
    # read a single line
    line = f.readline()
    line = line.rstrip()
    if not line:
        break
    if line[0] == "@":
        junk, dbname = line.split('-')
        line = f.readline()
        line = line.rstrip()
    print('/////////////////////////////////////////////////////////////')
    print(line)
    print('/////////////////////////////////////////////////////////////')
    x = json.loads(line)
    print(type(x))
    print('--------------------------------------------------------------------------')

    print('this is x {}'.format(x))
# close the pointer to that file
f.close()
