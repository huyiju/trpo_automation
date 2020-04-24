from main import *
import codecs

f1 = codecs.open("subjects.txt", "r", "utf_8_sig")
f2 = codecs.open("bodys.txt", "r", "utf_8_sig")
subs = f1.read()
bods = f2.read()
f1.close()
f2.close()
subjects = subs.split('\n')
bodys = bods.split('~')  # Разбиение по тильде
test = ValidationMail('a', 'a')
n = 1
for i in subjects:
    test.subject = i
    test.body = bodys[n-1]
    print(n, '\t', test.validation(test.subject, test.body))
    n += 1





