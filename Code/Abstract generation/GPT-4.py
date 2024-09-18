#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time：2023/3/3 19:27
# @Author：BaoTong
import requests
import json
import os

# Set your API key
api_key = "your_api_key"
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}',
}

def gpt_summarize(input_text, temperature=0.5, max_tokens=300):
    data = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": f"Summarize the following paragraph (no more than {max_tokens} tokens): {input_text}"}],
        "presence_penalty": 0.5,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    response = requests.post('replace with your chat/completions xxxxxxxxx', headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    else:
        print("Error:", response.status_code, response.text)
        return None

# Read file content
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Save results to file
def save_to_file(output_list, output_file_path):
    with open(output_file_path, 'a', encoding='utf-8') as output_file:
        json.dump(output_list, output_file, ensure_ascii=False, indent=2)

# Main processing function
def process_articles(articles, start_index=0):
    global processed_index
    output_list = []
    for i, article in enumerate(articles[start_index:], start=start_index):
        result = process_article(article, len(articles))
        output_list.append(result)
        print(f"Processing article {i+1} out of {len(articles)}")
    return output_list

# Process a single article
def process_article(article, articles_length):
    article_id = article["article_id"]
    sections = article["sections"]
    filtered_sections = {key: value for key, value in sections.items() if key != 'No match'}
    combined_text = ' '.join(filtered_sections.values())
    final_text = truncate_text(combined_text, 20000)
    summary = gpt_summarize(final_text)
    # Build result
    result = {"article_id": article_id, "summary": [{"summary": summary}]}
    return result

# Truncate text function
def truncate_text(text, max_length):
    truncated_text = text[:max_length]
    return truncated_text

if __name__ == "__main__":
    input_file_path = ./dataset/pubmed_10000.json'
    output_folder_path = 'output_folder/'
    output_file_path = os.path.join(output_folder_path, 'GPT-4_Pubmed.json')

    # Read file content
    articles = read_file(input_file_path)
    # Process articles
    output_list = process_articles(articles)
    # Save results to file
    save_to_file(output_list, output_file_path)
