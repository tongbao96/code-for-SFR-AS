#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : tbao
# @File    : rouge_calculation.py
# @Description : This function is used to calculate ROUGE scores for summaries generated in a specific task.

import json
from pyrouge import Rouge155
import os

if not os.path.exists('rouge_summaries'):
    os.makedirs('rouge_summaries/system_summaries')
    os.makedirs('rouge_summaries/reference_summaries')

with open('./output_folder/t5-pubmed_summaries.json', 'r', encoding='utf-8') as file:
    json1_data = json.load(file)

with open('pubmed_10000.json', 'r', encoding='utf-8') as file:
    json2_data = json.load(file)

article_id_to_abstract = {}
for entry in json2_data:
    article_id_to_abstract[entry['article_id']] = entry['abstract_text']

# Store system-generated summaries and reference summaries in files for ROUGE calculation
for i, article_data in enumerate(json1_data):
    # Merge the summary sections into one
    merged_summary = ''
    for section in article_data['summary']:
        for key, value in section.items():
            merged_summary += value + ' '
    
    current_article_id = article_data['article_id']
    current_abstract_text = article_id_to_abstract.get(current_article_id, '')

    with open(f'rouge_summaries/system_summaries/sys_{i}.txt', 'w', encoding='utf-8') as sys_file:
        sys_file.write(merged_summary.strip())
    
    with open(f'rouge_summaries/reference_summaries/ref_{i}.txt', 'w', encoding='utf-8') as ref_file:
        ref_file.write(current_abstract_text.strip())


rouge = Rouge155()
rouge.system_dir = 'rouge_summaries/system_summaries'
rouge.model_dir = 'rouge_summaries/reference_summaries'
rouge.system_filename_pattern = 'sys_(\d+).txt'
rouge.model_filename_pattern = 'ref_#ID#.txt'

# Calculate ROUGE scores
output = rouge.convert_and_evaluate()
print(output)

# Optionally, convert the output to a dictionary for further analysis
rouge_scores = rouge.output_to_dict(output)

# Print average ROUGE scores
print('Average ROUGE-1:', rouge_scores['rouge_1_f_score'])
print('Average ROUGE-2:', rouge_scores['rouge_2_f_score'])
print('Average ROUGE-L:', rouge_scores['rouge_l_f_score'])
