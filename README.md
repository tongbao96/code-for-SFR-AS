# Enhancing Abstractive Summarization of Scientific Articles based on Structure Information


## Overview

**Dataset and source code for paper "Enhancing Abstractive Summarization of Scientific Articles based on Structure Information".**

In this study, we propose a two-stage abstract summarization(AR) framework for scientific articles based on structure function recognition(SFR). Our work includes the followig aspects:: 
  - A two-stage scientific article summarization framework is proposed to enhance the comprehensiveness of summaries based on chapter structure information and overcome the input length limitations of generation models. 
  - We explore the impact of the different components of a chapter on the structure function recognition and systematically analyze how and why the chapter function helps to improve the effectiveness of abstractive summarization in the scientific article.
  - Through experimental studies on two widely used scientific paper summarization datasets, the results indicate that our proposed method outperforms advanced abstractive summarization baselines.
    
## Directory structure

<pre>  code-for-SFR-AS                         Root directory
  ├── Code                                Source code folder
  |   ├── Abstract generation             Code for AR task
  |   |   ├── BART.py                     Code for BART
  |   |   ├── GPT-4.py                    Code for GPT-4
  |   |   ├── Longformer.py               Code for Longformer
  |   |   ├── Pegasus.py                  Code for Pegasus
  |   |   ├── rouge_calcu.py              Code for Rouge metric
  |   |   ├── T5_base.py                  Code for T5-base
  |   |   ├── dataset                     AR Dataset folder
  |   |   └── output_folder               Output summary folder
  |   ├── Structure function recognition  Code for SFR task
  |   |   ├── dataset.py                  Code for loading data from dataset
  |   |   ├── model.py                    SciBERT model
  |   |   ├── params.py                   Params of SciBERT
  |   |   ├── test.py                     Code for testing new paragraphs
  |   |   ├── train.py                    Code for training
  |   |   ├── utils.py                    Code for utils
  |   |   ├── dataset                     SFR Dataset folder
  |   |   ├── logs                        Save train logs
  |   |   ├── runs                        Save run history
  |   |   └── weights                     Save weights after train
  Dataset                                 Raw dataset
  |   ├── NLM_Mapping                     Mapping title of chapter to IMRaD
  |   ├── arXiv                           Raw arXiv dataset
  |   └── pubmed                          Raw Pubmed dataset
  └────README.md
</pre>

## Dataset Discription

### Raw Data 

This paper conducts experiments on two widely accepted datasets of scientific paper abstracts, ArXiv and PubMed , Original data from the paper [A Discourse-Aware Attention Model for Abstractive Summarization of Long Document](https://arxiv.org/abs/1804.0568 ).

The files are in jsonlines format where each line is a json object corresponding to one scientific paper from ArXiv or PubMed. The abstract, sections and body are all sentence tokenized. The json objects are in the following format:

```
{ 
  'article_id': str,
  'abstract_text': List[str],
  'article_text': List[str],
  'section_names': List[str],
  'sections': List[List[str]]
}
```

### Data process

We use [National Library of Medicine (NLM) ]([lhncbc.nlm.nih.gov/ii/areas/structured-abstracts/downloads/Structured-Abstracts-Labels-102615.txt](https://www.lhncbc.nlm.nih.gov/ii/areas/structured-abstracts/downloads/Structured-Abstracts-Labels-102615.txt))files to map and align chapter title according to the IMRaD (*Introduction*, *Methods*, *Results* and *Conclusion*)  format.

For the SFR task, the traning data format as follwing:

```
[
    {
        "text": ..., 
        "label": ...
    }, 
    ..., 
    {
        "text": ..., 
        "label": ...
    }
]
```

the `classes_labels.json`follows the format:

```
{
    "class_1": 0,
    "class_2": 1,
    ...
    "class_n": n-1
}
```

For the AR task, we selecte articles from both the arXiv and Pubmed datasets that simultaneously include *Background*, *Methods*, *Results*, and *Conclusions* sections. For both two datasets, we limit section length to 1500 tokens, and the number of abstract words to a range of 50-300. the input data format as follwing:

```
[
  {
    "article_id": "1512.03812",
    "sections": {
      "BACKGROUND": "...",
      "METHODS": "...",
      "RESULTS": "...",
      "CONCLUSIONs": "...",
  	},
     "abstract_text": "..."
  }
   ..., 
]   
```

We limit the summary length of the model output to no more than 300 and no less than 50. （1）For models where the length of the full text exceeds the input length of the model (i.e., BARD, PEGASUS, T5-base), we use a divide-and-conquer approach to generate summary sentences for four sections, which are then concatenated to form the final abstract. （2）For models that are capable of handling long documents, we use the chapter labels along with the content as full-text inputs. 



## How to start:

- [x] **For SFR task:**

1. Run `load_dataset.py` to download and process the dataset, saving it locally. 

2. Download the [weights]([allenai/scibert: A BERT model for scientific text. (github.com)](https://github.com/allenai/scibert)) file to the SCIBERT directory

3. `classes_labels.json` contains the mapping between categories and their numerical labels. 

4. Some parameter settings are in `params.py`, which can be modified according to your needs. Alternatively, you can modify these parameters by entering commands in the terminal. Additionally, the template for prompts is also present in this file.

5. Run `train.py` to start training. The trained model is saved by default in the `weights` folder. If you want to view the changes in various parameters/metrics during training, the code provides two recording methods:

   - Check the corresponding `txt` file in the `logs` directory, which records the parameters set for training and evaluation metrics for each epoch.
   - In the `runs` directory, the results recorded using TensorBoard are saved. Assuming the path is `runs/bert-base-uncased-Sep19_16-31-56`, you can start TensorBoard with the command `tensorboard --logdir=runs/bert-base-uncased-Sep19_16-31-26`.

6. Run `test.py` to evaluate the model on the test set. Assuming the model weights are saved as `bert-base-uncased-Sep19_16-31-56-epoch0.pth`, you can run `test.py` in the terminal using the following command:

   ```commandline
   python test.py --weights_name=bert-base-uncased-Sep19_16-31-56-epoch0.pth
   ```

- [x] **For AR task:**

1. Run the files `BART.py`, `T5-base.py`, `Pegasus.py`, etc., separately to obtain summaries generated by these models. You can adjust the parameters in the `model_summarize` function according to your needs. The `load_processed_index` function keeps track of the data being processed. If you encounter network errors, you can continue running from the line number in `processed_index.txt`.
2. Run the files `GPT-4.py`,  to obtain summaries generated by these models. You can  apply for your apikey from [OpenAi]([OpenAI](https://openai.com/) ). Additional details about the GPT4 interface or errors encountered during operation can be found here[[API Reference - OpenAI API](https://platform.openai.com/docs/api-reference)]
3. Run `rouge_calu.py` to calculate the performance of different models.

## Results 

- **Results of SFR task**

| **Model**   |             | **Pubmed**  |             |             | **arXiv**   |             |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| **Macro_P** | **Macro_R** | **Macro_P** | **Macro_F** | **Macro_P** | **Macro_R** | **Macro_F** |
| BiLSTM      | 89.97%      | 88.85%      | 89.41%      | 86.21%      | 84.62%      | 85.40%      |
| BiLSTM-ATT  | 90.12%      | 89.39%      | 89.75%      | 86.74%      | 85.29%      | 86.01%      |
| BERT        | 91.35%      | 90.11%      | 90.73%      | 88.19%      | 87.02%      | 87.60%      |
| RoBERTa     | 91.72%      | 90.67%      | 9120%       | 88.33%      | 87.17%      | 87.74%      |
| **SciBERT** | **92.38%**  | 91.21%      | **91.79%**  | 89.01%      | 87.84%      | **88.42%**  |
| T5          | 92.21%      | **91.24%**  | 91.72%      | 87.90%      | 86.61%      | 87.25%      |

- **Results of AR task**

| **Models**                             | ****        | **arXiv**   |             |             | **Pubmed**  |             |
| -------------------------------------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| **Rouge-1**                            | **Rouge-1** | **Rouge-2** | **Rouge-L** | **Rouge-1** | **Rouge-2** | **Rouge-L** |
| BERTSUM  (Liu,  2019)                  | 31.98       | 10.02       | 27.75       | 34.39       | 13.24       | 30.90       |
| BART  (Lewis et al., 2019)             | 34.87       | 12.82       | 29.83       | 37.44       | 15.39       | 32.71       |
| PEGASUS  (Zhang et al., 2020)          | 33.36       | 11.18       | 28.94       | 36.94       | 15.05       | 31.81       |
| T5-base  (Raﬀel et al., 2020)          | 33.75       | 11.76       | 29.01       | 37.75       | 14.92       | 32.65       |
| BigBird-Pegasus-4K                     | 42.47       | 17.95       | 37.29       | 42.81       | 18.71       | 39.23       |
| Longformer-16k  (Beltagy et al., 2020) | **42.81**   | **18.26**   | **38.72**   | **44.39**   | **19.07**   | **40.08**   |
| GPT-4-32K  *                           | 29.96       | 09.13       | 27.01       | 30.02       | 09.17       | 27.62       |

- **Results of the human evaluation of the summaries generated by different models **

| **Models**         | **Informativeness** | **Coherence** | **Fluency** |
| ------------------ | ------------------- | ------------- | ----------- |
| BERTSUM            | 2.41                | 2.27          | 2.99        |
| BART               | 3.37                | 3.44          | 3.09        |
| PEGASUS            | 3.09                | 3.26          | 3.46        |
| T5-base            | 3.28                | 3.40          | 3.43        |
| BigBird-Pegasus-4K | 3.72                | 3.82          | 3.64        |
| Longformer-16k     | 3.89                | 3.88          | 3.80        |
| GPT-4-32K          | **4.09**            | **4.03**      | **4.41**    |

## Citing

Relevant reference is "A Discourse-Aware Attention Model for Abstractive Summarization of Long Documents"

```
"A Discourse-Aware Attention Model for Abstractive Summarization of Long Documents"  
Arman Cohan, Franck Dernoncourt, Doo Soon Kim, Trung Bui, Seokhwan Kim, Walter Chang, and Nazli Goharian  
NAACL-HLT 2018
```


