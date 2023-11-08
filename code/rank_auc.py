import sys
import numpy as np

#run stat.py before this script

def compute_rank_roc(ranks, n_prots):
    auc_x = list(ranks.keys())  
    auc_x.sort()
    auc_y = []
    tpr = 0
    sum_rank = sum(ranks.values())

    if sum_rank == 0:
        auc = 0  
    else:
      for x in auc_x:
          tpr += ranks[x]
          auc_y.append(tpr / sum_rank)
    auc_x.append(n_prots+1)
    auc_y.append(1)

    auc = np.trapz(auc_y, auc_x) / n_prots

    return auc

#path to the responses folder
path="./GPCards/GPCards_questions/responses/GPT4_zeroshot/"

labels = {}
preds = {}
ranks = {}


with open (path+"/stat."+sys.argv[1]+".txt", "r") as f:
    for l in f:
      if "TOP" not in l:
        tmp=l.rstrip().split("\t")
        if int(float(tmp[1]))>int(sys.argv[1]):
           tmp[1]=int(sys.argv[1])

        rank=int(float(tmp[1]))
        if rank in ranks:
           ranks[rank] += 1
        else:
           ranks[rank]=1
#print (ranks)
for rank in range (1, int(sys.argv[1])+1):
    if rank not in ranks:
       ranks[rank]=0



rank_auc = compute_rank_roc(ranks, int(sys.argv[1]))
rank_auc = round(rank_auc, 3)

print ("GENE SIZE="+sys.argv[1]+"\t"+str(rank_auc))


