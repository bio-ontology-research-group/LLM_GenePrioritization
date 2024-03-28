## Scripts

- **questions_clinvar.py:** Script to generates questions to be used by the zero.shot.py and one_shot.py
- **zero.shot.py:** Scipt that utilizes GPTs through the OpenAI API with zero-shot prompting.
- **one_shot.py:** Scipt that utilizes GPTs through the OpenAI API with one-shot chain of thought prompting.
- **run_falcon.py:** Scipt that utilizes Falcon180B.
- **run_other_tools.sh:** Script to run other tools (Exomiser, PHIVE, Phenix, and exomeWalker) following the default command in the [manual](https://exomiser.github.io/Exomiser/manual/7/exomiser/).
- **stat.py:** Script to calculate statistics on LLM responses.
- **AUPR.py:** Script to calculate the Area Under the Precision-Recall curve (AUPR).
- **rank_other_tools.py:** Script to calculate the ranks for other tools (exomiser, phenic, phive, and Exomewalker).
- **rank_auc.py:**  Script to calculate ROC AUC.

## Dependencies

- Access to the [ChatGPT](https://platform.openai.com/docs/introduction) through the API.
- Installation of other LLM and tools ([Falcon180B](https://falconllm.tii.ae/falcon-180b.html), [Exomiser](https://www.sanger.ac.uk/tool/exomiser/), [PHIVE](https://exomiser.github.io/Exomiser/manual/7/quickstart/#phive), [Phenix](https://exomiser.github.io/Exomiser/manual/7/quickstart/#phenix), and [exomeWalker](https://exomiser.github.io/Exomiser/manual/7/quickstart/#exomewalker))


## How to run
- Generate prompts:
  run: python questions_clinvar.py

-  Run openAI's GPT:
   Step1. Create an output folder called: responses_one_shot
   
   Step2. Please edi the one_shot.py script to palce your OpenAI key.
   
   Step2. python one_shot.py

- Evaluate:
  Step1. python stat.py
  
  Step2. python AUPR.py
  
  Step3. python rank_auc.py
  
