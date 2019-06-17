from operator import itemgetter

class graduatoria(object):
	def __init__(self):
		self.name = ""
		self.surname = ""
		self.score = 0
		self.list = []

	def writing(self):
		with open('graded_list', 'a') as fd:
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
					self.list.append([self.name, self,surname, self.score])

	def read_noscore(self):
		with open('graded_list', 'r') as fd:
			for line in fd:
				values = line.split()
				if len(values) == 2:
					self.name = values[0]
					self.surname = values[1]
					self.list.append([self.name, self,surname, self.score])

	def sorting(self):
		self.list = sorted(self.list, reverse=True, key=itemgetter(2))
