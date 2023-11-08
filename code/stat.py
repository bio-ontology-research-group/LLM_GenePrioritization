import sys
import re
genes={}
cnt=0
top1=0
top5=0
top10=0

f=open("ClinVar_100.txt.txt")
#1       VWA1    
for l in f:
	if "PubMed" not in l and cnt<100:
		p=l.rstrip().split('\t')
		genes[cnt]=p[1]
		cnt=cnt+1


for i in range(0,100):
	myranks={}
	f=open('./responses/gene'+sys.argv[1]+'/r_'+str(i+1)+'.txt')
	rank=1
	for l in f:
		p=l.rstrip().replace('"','')
		if p.strip() and p[0].isdigit():			gene_names = re.findall(r'\d+\.\s+(.+)',p) #findall(r'\d+\.\s+([^:\s]+)[:\s]', p) 
			if len(gene_names)>0:
				myranks[gene_names[0]]=rank
				rank=rank+1
	if len(myranks)>0 and genes[i] in myranks:
		if  len(myranks)>int(sys.argv[1]) :
			if  int(myranks[genes[i]])>int(sys.argv[1]):
				print ("Patient"+str(int(i+1))+"\t"+sys.argv[1]+"\tFAILED_CAUSATIVE_FOUND_IN_LARGERLIST")
			else:
				print ("Patient"+str(int(i+1))+"\t"+str(myranks[genes[i]])+"\tFAILED_LARGERLIST_RETURNED")
		elif len(myranks)<int(sys.argv[1]):
			print ("Patient"+str(i)+"\t"+str(myranks[genes[i]])+"\tFAILED_SMALLERLIST_RETURNED")
		else:
			print ("Patient"+str(i)+"\t"+str(myranks[genes[i]]))

		if int(myranks[genes[i]])==1:
			top1=top1+1
		elif int(myranks[genes[i]])>1 and int(myranks[genes[i]])<6:
			top5=top5+1
		elif int(myranks[genes[i]])>5 and int(myranks[genes[i]])<11:
			top10=top10+1
	else:
		if len(myranks)>int(sys.argv[1]):
			print ("Patient"+str(int(i+1))+"\t"+sys.argv[1]+"\tFAILED_CAUSATIVE_NOT_IN_LARGERLIST")
		else:
			rr=int(sys.argv[1])-len(myranks)
			rr=round(rr/2)
			rr=rr+len(myranks)
			print ("Patient"+str(int(i+1))+"\t"+str(rr)+"\tFAILED_CAUSATIVE_NOT_IN_SMALLERLIST")


print ("Gene:"+sys.argv[1]+"\tTOP1="+str(top1)+"\tTOP5="+str(top1+top5)+"\tTOP10="+str(top1+top5+top10))

