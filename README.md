# Enhancing Abstractive Summarization of Scientific Articles based on Structure Information


## Overview

**Dataset and source code for paper: "Enhancing Abstractive Summarization of Scientific Papers based on Structure Information".**

In this study, we propose a novel two-stage abstract summarization(AS) framework for scientific articles based on structure function recognition(SFR). The main contributions of this paper are as follows:

  - We proposed a two-stage framework for abstractive summarization of scientific papers, which leverages automatic structural function recognition to generate more balanced and comprehensive summaries. 
  - A controlled experiment demonstrated that the beginning and ending positions of chapters contain important information, which is beneficial for structural function recognition. Additionally, through systematic evaluation, we pointed out the biases in traditional summary quality metrics when evaluating generative models, such as GPT-4.
  - A large-scale dataset was constructed to recognize structural functions in scientific papers.
  - Experiments on two benchmarks demonstrate that our methods outperforms advanced baselines in scientific paper abstractive summarization, with the generated summaries being more comprehensive than those from the baseline models.

## Directory structure

<pre>  SFR-AS                                  Root directory
  ├── Code                                Source code folder
  |   ├── Abstract summarization          Code for AS task
  |   |   ├── Longformer.py               Code for Longformer
  |   |   ├── GPT-4.py                    Code for gpt-4
  |   |   ├── rouge_calcu.py              Code for Rouge metric
  |   |   ├── dataset                     Selected articles from Pubmed and arXiv dataset
  |   |   └── output_folder               Output summary folder
  |   ├── Structure function recognition  Code for SFR task
  |   |   ├── dataset.py                  Code for loading data from dataset
  |   |   ├── model.py                    SciBERT model
  |   |   ├── params.py                   Params of SciBERT
  |   |   ├── test.py                     Code for testing new paragraphs
  |   |   ├── train.py                    Code for training
  |   |   ├── utils.py                    Code for utils
  |   |   ├── SFR_traning_dataset         Training Dataset folder for SFR task
  |   |   ├── logs                        Save train logs
  |   |   ├── runs                        Save run history
  |   |   └── weights                     Save weights after train
  Orignal_Dataset                         Raw dataset
  |   ├── NLM_Mapping                     Mapping title of chapter to IMRaD
  |   ├── arXiv                           Raw arXiv dataset
  |   └── pubmed                          Raw Pubmed dataset
  └───README.md
</pre>


## Dataset download

### Raw Data 

This paper conducts experiments on two widely accepted datasets of scientific paper abstracts, arXiv and PubMed , Original data from the paper [A Discourse-Aware Attention Model for Abstractive Summarization of Long Document](https://arxiv.org/abs/1804.05685). 

 You can download the arXiv dataset at (https://archive.org/download/armancohan-long-summarization-paper-code/arxiv-dataset.zip) and the Pubmed dataset at (https://archive.org/download/armancohan-long-summarization-paper-code/pubmed-dataset.zip).

The datasets are substantial, requiring about 5 GB of disk space for download and approximately 15 GB additional space for extraction. Each `tar` file consists of 4 files. `train.txt`, `val.txt`, `test.txt` respectively correspond to the training, validation, and test sets. The `vocab` file is a plaintext file for the vocabulary.

The files are in jsonlines format where each line is a json object corresponding to one scientific paper from arXiv or PubMed. The abstract, sections and body are all sentence tokenized. The json objects are in the following format:

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

 You can download the structural function recognition dataset at (https://doi.org/10.5281/zenodo.13772003). The datasets are rather large as well, requiring about 2 GB of disk space for download.

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

the `classes_map.json`follows the format:

```
{
    "class_1": 0,
    "class_2": 1,
    ...
    "class_n": n-1
}
```

For the AS task, we selecte articles from both the arXiv and Pubmed datasets that simultaneously include *Background*, *Methods*, *Results*, and *Conclusions* sections. The input data format as follwing:

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

## How to start:

- [x] **For SFR task:**

1. Download the weights for SciBERT at([allenai/scibert: A BERT model for scientific text. (github.com)](https://github.com/allenai/scibert)) to the SciBERT directory
   
2. Download the SFR task dataset from the link provided earlier.
   
3. `classes_labels.json` contains the mapping between categories and their numerical labels. 

4. Some parameter settings are in `params.py`, which can be modified according to your needs.

5. Truncate the chapter according to your desired  ratio, Then, run `train.py` to start training. The trained model is saved by default in the `weights` folder. If you want to view the changes in various parameters/metrics during training, the code provides two recording methods:

   - Check the corresponding `txt` file in the `logs` directory, which records the parameters set for training and evaluation metrics for each epoch.
   - In the `runs` directory, the results recorded using TensorBoard are saved. Assuming the path is `runs/bert-base-uncased-Sep19_16-31-56`, you can start TensorBoard with the command `tensorboard --logdir=runs/bert-base-uncased-Sep19_16-31-26`.

6. Run `test.py` to evaluate the model. 


- [x] **For AS task:**

1.Download the weights from Huggingface to the local directory at the same level, or directly input the model name in the model path. Note:the latter option may encounter network issues.

2. Run the files `Longformer.py`,  to obtain summaries generated by these models. You can adjust the parameters in the `model_summarize` function according to your needs. The `load_processed_index` function keeps track of the data being processed. If you encounter network errors, you can continue running from the line number in `processed_index.txt`.

3. Run the files `GPT-4.py`,  to obtain summaries generated by these models. Based on the official website, the token pricing for GPT-4 is $30/1M for input tokken and 60/1M for output tokens. You can  apply for your apikey from [OpenAi]([OpenAI](https://openai.com/) ) and pay for API usage. Additional details about the GPT4 interface or errors encountered during operation can be found here[[API Reference - OpenAI API](https://platform.openai.com/docs/api-reference)]

4. Run `rouge_calu.py` to get the rouge score.


- [x] **For LLMs evaluation:**

1. The reference for G-eval can be found in [*G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment*](https://arxiv.org/pdf/2303.16634) 

2. The API still needs to be obtained from the official website, and pay for API usage.


## Citation

Please cite the following paper if you use this code and dataset in your work.

>Tong Bao, Heng Zhang, Chengzhi Zhang\*. Enhancing Abstractive Summarization of Scientific Articles based on Structure Information. ***Expert system with application***, 2024. [[doi]]() [[Dataset & Source Code]]( https://github.com/tongbao96/code-for-SFR-AS).

