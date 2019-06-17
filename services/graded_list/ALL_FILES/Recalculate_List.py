import random
import string
from operator import itemgetter



def randomString(stringLength=6):
    """Generate a random string of fixed length """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

def calc_sum2(a, b, c):
	return int(a+b-c)

def calc_sum1(a, b):
	a = "AAAA"+a
	b = "BBBB"+b
	res = 0
	if len(a) < len(b):
		c = b
		b = a
		a = c
	for i, c in enumerate(a):
		if i < len(b):
			res += ord(a[i])^ord(b[i])
		else:
			res += 0
	return res


class graduatoria(object):
	def __init__(self):
		self.name = ""
		self.surname = ""
		self.score = 0
		self.list = []

	def writing(self):
		with open('graded_list', 'w') as fd:
			for x in self.list:
				fd.write(x[0] + " " + x[1] + " " + str(x[2]) + '\n')
			fd.close()

	def reading(self):
		with open('graded_list', 'r') as fd:
			for line in fd:
				values = line.split()
				if len(values) == 3:
					self.name = values[0]
					self.surname = values[1]
					self.score = int(values[2])
					self.list.append([self.name, self.surname, self.score])
				elif len(values) == 2:
					self.name = values[0]
					self.surname = values[1]
					self.list.append([self.name, self.surname, 0])
			fd.close()

	def sorting(self):
		self.list = sorted(self.list, reverse=True, key=itemgetter(2))

sum1 = 0
sum2 = 0

x = 255
y = 255
z = 0

cont = 0

grad = graduatoria()
grad.reading()
#while 1 == 1:
for k in grad.list:
	x = random.randint(220, 256)
	y = random.randint(230, 256)
	z = random.randint(0, 10)
	str1 = k[0]
	str2 = k[1]
	#str1 = randomString(16)
	#str2 = randomString(16)
	sum2 = calc_sum2(x, y, z)
	sum1 = calc_sum1(str1, str2)
	k[2] = sum1+sum2
grad.sorting()
grad.writing()
	#if sum3 > 1090:
	#	cont += 1
	#	print(str(cont) + " Score: " + str(sum3) + "\nwith: " + str(x) + " " + str(y) + " " + str(z))
	#	print("And Strings: " + str1 + " " + str2 + '\n')