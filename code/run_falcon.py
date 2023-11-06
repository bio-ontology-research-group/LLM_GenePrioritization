from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch
model = "falcon-180B-chat"

tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto",
)
#Files are numbers 0 through 49 (number of individuals)
for i in range(0,50,1):
    #Each file belongs to an individual 
    lines=open('questions_final/q_'+str(i)+'.txt').readlines()
    out=open('out/'+str(i),'w+')
    #Each line is a question with N number of genes
    for j,l in enumerate(lines[:-1]):
        l=l.rstrip()
        sequences = pipeline(
        l,
        max_length=1200,
        do_sample=False,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        )
        for seq in sequences:
            out.write('Q'+str(j)+':\t'+seq['generated_text']+'\n')
    out.close()
