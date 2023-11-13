import sys
import csv
import os
import pickle as pkl

def load_data(file_path):
    with open(file_path, 'rb') as input_file:
        return pkl.load(input_file)

def process_file(file_path, score_column, data, correct, results):
    filename = os.path.basename(file_path).split('.exomiser')[0]
    all_scores = {}

    with open(file_path, "r") as file:
        info_dict = {}

        lines = file.readlines()

        column_names = lines[0].strip().split('\t')
        gene_symbol_index = column_names.index("#GENE_SYMBOL")
        gene_pheno_score_index = column_names.index(score_column)

        for line in lines[1:]:
            parts = line.strip().split('\t')
            if len(parts) >= max(gene_symbol_index, gene_pheno_score_index):
                gene_symbol = parts[gene_symbol_index]
                gene_pheno_score = float(parts[gene_pheno_score_index])
                info_dict[gene_symbol] = gene_pheno_score

        all_scores[filename] = info_dict

    return all_scores

def main():
    tool = sys.argv[1]
    dataset = sys.argv[2]
    score_column = sys.argv[3]
    result_path = sys.argv[4]
    results = sys.argv[5]

    # read pavs data and the true genes
    data = load_data(f'{dataset}_gene_data.pkl')
    correct = load_data(f'correct_{dataset}.pkl')

    for filename in os.listdir(result_path):
        file_path = os.path.join(result_path, filename)
        all_scores = process_file(file_path, score_column, data, correct, results)

        with open(f'{results}/performance_results_{tool}_{dataset}_{score_column}.tsv', 'w', newline='') as tsvfile:
            fieldnames = ['Set Number', 'Top 1', 'Top 5', 'Top 10']
            writer = csv.DictWriter(tsvfile, fieldnames=fieldnames, delimiter='\t')

            for set_num in [1, 5, 10, 15, 20]:
                ranks_at_1 = 0
                ranks_at_5 = 0
                ranks_at_10 = 0

                for file, genes_scores in all_scores.items():
                    if file in data and file in correct:
                        if set_num in data[file]:
                            gene_set = data[file][set_num]
                        else:
                            continue

                        filtered_genes = [gene for gene in gene_set if gene in genes_scores]

                        sorted_genes = sorted(filtered_genes, key=lambda gene: genes_scores[gene], reverse=True)

                        correct_gene = correct[file]
                        if correct_gene in sorted_genes:
                            rank = sorted_genes.index(correct_gene) + 1

                        elif (correct_gene not in sorted_genes) and (len(sorted_genes) < set_num * 5):
                            rank = int(set_num * 5) - len(sorted_genes)
                            rank = round(rank / 2)
                            rank = rank + len(sorted_genes)

                        auc_file_name = f'{results}/for_auc/{dataset}_{tool}_{score_column}.tsv'
                        with open(auc_file_name, 'a') as auc_file:
                            line = f"{set_num * 5}\t{file}\t{rank}\n"
                            auc_file.write(line)

                        if rank == 1:
                            ranks_at_1 += 1
                        if rank <= 5:
                            ranks_at_5 += 1
                        if rank <= 10:
                            ranks_at_10 += 1

                print(f"Set {set_num}:")
                print(f"Ranks at 1: {ranks_at_1}")
                print(f"Ranks at 5: {ranks_at_5}")
                print(f"Ranks at 10: {ranks_at_10}")
                print('----------------------------')

                writer.writerow({
                    'Set Number': set_num * 5,
                    'Top 1': ranks_at_1,
                    'Top 5': ranks_at_5,
                    'Top 10': ranks_at_10
                })

if __name__ == "__main__":
    main()
