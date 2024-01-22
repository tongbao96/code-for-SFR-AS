# Enhancing Abstractive Summarization of Scientific Articles based on Structure Information


## Overview

**Dataset and source code for paper "Enhancing Abstractive Summarization of Scientific Articles based on Structure Information".**

In this study, we propose a two-stage abstract summarization(AS) framework for scientific articles based on structure function recognition(SFR). Our work includes the followig aspects: 
  - A two-stage scientific article summarization framework is proposed to enhance the comprehensiveness of summaries based on chapter structure information and overcome the input length limitations of generation models. 
  - We explore the impact of the different components of a chapter on the structure function recognition and systematically analyze how and why the chapter function helps to improve the effectiveness of abstractive summarization in the scientific article.
  - Through experimental studies on two widely used scientific paper summarization datasets, the results indicate that our proposed method outperforms advanced abstractive summarization baselines.
    
## Directory structure

<pre>  SFR-AS                                  Root directory
  ├── Code                                Source code folder
  |   ├── Abstract summarization          Code for AS task
  |   |   ├── BART.py                     Code for BART
  |   |   ├── GPT-4.py                    Code for GPT-4
  |   |   ├── Longformer.py               Code for Longformer
  |   |   ├── Pegasus.py                  Code for Pegasus
  |   |   ├── rouge_calcu.py              Code for Rouge metric
  |   |   ├── T5_base.py                  Code for T5-base
  |   |   ├── articles_for_AS_task        Selected articles from Pubmed and arXiv dataset
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

For the AS task, we selecte articles from both the arXiv and Pubmed datasets that simultaneously include *Background*, *Methods*, *Results*, and *Conclusions* sections. For both two datasets, we limit section length to 1500 tokens, and the number of abstract words to a range of 50-300. the input data format as follwing:

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

- [x] **For AS task:**

1. Run the files `BART.py`, `T5-base.py`, `Pegasus.py`, etc., separately to obtain summaries generated by these models. You can adjust the parameters in the `model_summarize` function according to your needs. The `load_processed_index` function keeps track of the data being processed. If you encounter network errors, you can continue running from the line number in `processed_index.txt`.
2. Run the files `GPT-4.py`,  to obtain summaries generated by these models. You can  apply for your apikey from [OpenAi]([OpenAI](https://openai.com/) ). Additional details about the GPT4 interface or errors encountered during operation can be found here[[API Reference - OpenAI API](https://platform.openai.com/docs/api-reference)]
3. Run `rouge_calu.py` to calculate the performance of different models.

## Results 

- **Results of SFR task**

<table>
  <tr>
    <th rowspan="2">Model</th>
    <th colspan="3">Pubmed</th>
    <th colspan="3">arXiv</th>
  </tr>
  <tr>
    <th>Macro_R</th>
    <th>Macro_P</th>
    <th>Macro_F</th>
    <th>Macro_R</th>
    <th>Macro_P</th>
    <th>Macro_F</th>
  </tr>
   <tr>
    <td>BiLSTM</td>
    <td>89.97%</td>
    <td>88.85%</td>
    <td>89.41%</td>
    <td>86.21%</td>
    <td>84.62%</td>
    <td>85.40%</td>
  </tr>
  <tr>
    <td>BiLSTM-ATT</td>
    <td>90.12%</td>
    <td>89.39%</td>
    <td>89.75%</td>
    <td>86.74%</td>
    <td>85.29%</td>
    <td>86.01%</td>
  </tr>
  <tr>
    <td>BERT</td>
    <td>91.35%</td>
    <td>90.11%</td>
    <td>90.73%</td>
    <td>88.19%</td>
    <td>87.02%</td>
    <td>87.60%</td>
  </tr>
  <tr>
    <td>RoBERTa</td>
    <td>91.72%</td>
    <td>90.67%</td>
    <td>91.20%</td>
    <td>88.33%</td>
    <td>87.17%</td>
    <td>87.74%</td>
  </tr>
  <tr>
    <td>SciBERT</td>
    <td>92.38%</td>
    <td>91.21%</td>
    <td>91.79%</td>
    <td>89.01%</td>
    <td>87.84%</td>
    <td>88.42%</td>
  </tr>
  <tr>
    <td>T5</td>
    <td>92.21%</td>
    <td>91.24%</td>
    <td>91.72%</td>
    <td>87.90%</td>
    <td>86.61%</td>
    <td>87.25%</td>
  </tr>
</table>

- **Results of AS task**

<table>
  <tr>
    <th rowspan="2">Models</th>
    <th colspan="3">arXiv</th>
    <th colspan="3">Pubmed</th>
  </tr>
  <tr>
    <th>Rouge-1</th>
    <th>Rouge-2</th>
    <th>Rouge-L</th>
    <th>Rouge-1</th>
    <th>Rouge-2</th>
    <th>Rouge-L</th>
  </tr>
  <tr>
    <td>BERTSUM (Liu, 2019)</td>
    <td>31.98</td>
    <td>10.02</td>
    <td>27.75</td>
    <td>34.39</td>
    <td>13.24</td>
    <td>30.90</td>
  </tr>
  <tr>
    <td>BART (Lewis et al., 2019)</td>
    <td>34.87</td>
    <td>12.82</td>
    <td>29.83</td>
    <td>37.44</td>
    <td>15.39</td>
    <td>32.71</td>
  </tr>
  <tr>
    <td>PEGASUS (Zhang et al., 2020)</td>
    <td>33.36</td>
    <td>11.18</td>
    <td>28.94</td>
    <td>36.94</td>
    <td>15.05</td>
    <td>31.81</td>
  </tr>
  <tr>
    <td>T5-base (Raﬀel et al., 2020)</td>
    <td>33.75</td>
    <td>11.76</td>
    <td>29.01</td>
    <td>37.75</td>
    <td>14.92</td>
    <td>32.65</td>
  </tr>
  <tr>
    <td>BigBird-Pegasus-4K</td>
    <td>42.47</td>
    <td>17.95</td>
    <td>37.29</td>
    <td>42.81</td>
    <td>18.71</td>
    <td>39.23</td>
  </tr>
  <tr>
    <td>Longformer-16k (Beltagy et al., 2020)</td>
    <td><strong>42.81</strong></td>
    <td><strong>18.26</strong></td>
    <td><strong>38.72</strong></td>
    <td><strong>44.39</strong></td>
    <td><strong>19.07</strong></td>
    <td><strong>40.08</strong></td>
  </tr>
  <tr>
    <td>GPT-4-32K</td>
    <td>29.96</td>
    <td>9.13</td>
    <td>27.01</td>
    <td>30.02</td>
    <td>9.17</td>
    <td>27.62</td>
  </tr>
</table>

- **Results of the human evaluation of the summaries generated by different modelsk**

| **Models**         | **Informativeness** | **Coherence** | **Fluency** |
| ------------------ | ------------------- | ------------- | ----------- |
| BERTSUM            | 2.41                | 2.27          | 2.99        |
| BART               | 3.37                | 3.44          | 3.09        |
| PEGASUS            | 3.09                | 3.26          | 3.46        |
| T5-base            | 3.28                | 3.40          | 3.43        |
| BigBird-Pegasus-4K | 3.72                | 3.82          | 3.64        |
| Longformer-16k     | 3.89                | 3.88          | 3.80        |
| GPT-4-32K          | **4.09**            | **4.03**      | **4.41**    |

## Citation
Please cite the following paper if you use this code and dataset in your work.

>Tong Bao, Heng Zhang, Chengzhi Zhang\*. Enhancing Abstractive Summarization of Scientific Articles based on Structure Information. ***Journal of the Association for Information Science and Technology***, 2024 (Submitted).


