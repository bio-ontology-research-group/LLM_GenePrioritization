import sys
import numpy as np
from sklearn.metrics import auc

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

#path to the statistics files
path=sys.argv[2]
labels = {}
preds = {}
ranks = {}

precisions = [1]
recalls = [0]
patients = 0
with open (path+"/stat."+sys.argv[1]+".txt", "r") as f:
    for l in f:
      if "TOP" not in l:
        patients+=1
        tmp=l.rstrip().split("\t")

        if int(float(tmp[1]))>int(sys.argv[1]):
           tmp[1]=int(sys.argv[1])

        rank=int(float(tmp[1]))
        if rank in ranks:
           ranks[rank] += 1
        else:
           ranks[rank]=1

FP=0
TP=0
FN=0
cumulative=0
order=[]
for rank in range (1, int(sys.argv[1])+1):
    if rank not in ranks:
       ranks[rank]=0
    cumulative+=ranks[rank]
    TP=cumulative#ranks[rank]
    FP=(patients*rank)-TP
    FN=patients-TP

    order.append(rank)
    precisions.append(float(TP)/(float(TP)+float(FP)))
    recalls.append(float(TP)/(float(TP)+float(FN)))



print("GENE SIZE="+sys.argv[1],'\t',round(auc(recalls, precisions),3))

