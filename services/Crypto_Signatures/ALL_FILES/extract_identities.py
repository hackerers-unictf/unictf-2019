import csv

with open('identities', 'w') as fd1:
	with open('signatures.csv', 'r') as fd:
		incsv = csv.reader(fd)
		for row in incsv:
			fd1.write(row[0]+'\n')
	fd.close()
fd1.close()