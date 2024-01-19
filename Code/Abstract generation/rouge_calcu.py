#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/7 17:27
# @Author  : tbao
# @File    : rougejisuan.py
# @Description : This function is used to calculate ROUGE scores for summaries generated in a specific task.

import json
from rouge import Rouge

# Read json1 file
with open('./output_folder/all_summaries_val.json', 'r', encoding='utf-8') as file:
    json1_data = json.load(file)

# Read json2 file
with open('arXiv_val_30000.json', 'r', encoding='utf-8') as file:
    json2_data = json.load(file)

# Build a dictionary of abstract_text using article_id
article_id_to_abstract = {}
for entry in json2_data:
    article_id_to_abstract[entry['article_id']] = entry['abstract_text']

# Initialize Rouge
rouge = Rouge()

# Store ROUGE scores for each article
rouge_scores = []

# Iterate through each article
for article_data in json1_data:
    # Merge summaries
    merged_summary = ''
    for section in article_data['summary']:
        for key, value in section.items():
            merged_summary += value + ' '

    # Extract abstract_text for the current article_id
    current_article_id = article_data['article_id']
    current_abstract_text = article_id_to_abstract.get(current_article_id, '')

    # Calculate ROUGE scores
    scores = rouge.get_scores(merged_summary, current_abstract_text)

    # Store scores
    rouge_scores.append(scores[0])

# Calculate average ROUGE scores
average_rouge = {
    'rouge-1': sum(score['rouge-1']['f'] for score in rouge_scores) / len(rouge_scores),
    'rouge-2': sum(score['rouge-2']['f'] for score in rouge_scores) / len(rouge_scores),
    'rouge-l': sum(score['rouge-l']['f'] for score in rouge_scores) / len(rouge_scores),
}

# Print average scores
print('Average ROUGE-1:', average_rouge['rouge-1'])
print('Average ROUGE-2:', average_rouge['rouge-2'])
print('Average ROUGE-L:', average_rouge['rouge-l'])
