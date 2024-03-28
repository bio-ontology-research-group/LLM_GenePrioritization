from unidecode import unidecode

#cnt	ID      geneSymbol      phenoLabels     phenoClasses    sex     zygosityLabel
f=open(".data/datasets/Clinvar_100.txt","r")
phens=[]
genes=[]
import sys
import random
idx=int(sys.argv[1])

l=f.readlines()[(idx-1)]

l=unidecode(l)
p=l.rstrip().split('\t')
phens.append([p[1],p[2]])
gene=p[1]

x="A  patient who is suspected of having a genetic disease, presented with these clinical symptoms: "
for phen in phens[0][1].split('|'):
	phen=phen[0]+phen[1:]
	x+='"'+phen+'", '
x=x[:-2]+'. Rank these genes according to their association with the symptoms of the patient:'

f=open('.data/hgnc.genes.txt')
for l in f:
	p=l.rstrip()
	if p.isnumeric():
		continue
	genes.append(p)
genes=set(genes)
genes=list(genes)

for i in range(4, 101, 5):
	tt=x
	for gene in set(genes[:i]+[phens[0][0]]):
		tt+='"'+gene+'", '
	print(tt[:-2])
print('correct answer:',phens[0])

