#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description : This script is used to summarize articles using Longformer model.
import torch
from transformers import LEDForConditionalGeneration, LEDTokenizer
import json
import os

# LED Model
LED_PATH = "allenai/led-base-16384"
led_model = LEDForConditionalGeneration.from_pretrained(LED_PATH, return_dict_in_generate=True)
led_tokenizer = LEDTokenizer.from_pretrained(LED_PATH)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
led_model.to(device)
led_model.eval()


processed_index = 0

def led_summarize(input_text):
    input_ids = led_tokenizer(input_text, return_tensors="pt").input_ids.to(device)
    global_attention_mask = torch.zeros_like(input_ids)
    global_attention_mask[:, 0] = 1
    sequences = led_model.generate(input_ids, global_attention_mask=global_attention_mask,max_length=300).sequences
    summary = led_tokenizer.batch_decode(sequences)
    return summary[0]


def truncate_text(text, max_length):
    truncated_text = text[:max_length]
    return truncated_text

def load_processed_index(filename='processed_index.txt'):
    try:
        with open(filename, 'r') as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def save_processed_index(index, filename='processed_index.txt'):
    with open(filename, 'w') as file:
        file.write(str(index))

def process_article(article, articles_length):
    global processed_index
    processed_index += 1
    result = {}
    print(f"Processing article {processed_index} out of {articles_length}")

    result = []
    article_id = article["article_id"]
    sections = article["sections"]
    filtered_sections = {key: value for key, value in sections.items() if key != 'No match'}
    combined_text = ' '.join(filtered_sections.values())
    final_text = truncate_text(combined_text, 20000)
    # Summarize using LED model
    summary = led_summarize(final_text)
    # Build result
    result = {"article_id": article_id, "summary": [{"combined_summary": summary}]}
    return result

def main(input_file_path, output_file_path, start_index=None):
    with open(input_file_path, 'r', encoding='utf-8') as json_file:
        articles = json.load(json_file)、

    if not os.path.exists(output_file_path):
        os.makedirs(output_file_path)

    global processed_index
    if start_index is None:
        start_index = load_processed_index()
    processed_index = start_index

    output_list = []

    for i, article in enumerate(articles[start_index:], start=start_index):
        processed_index = i
        result = process_article(article, len(articles))
        output_list.append(result)

        # Save the current processed index
        save_processed_index(processed_index)

    # Save the final output
    output_file_path = os.path.join(output_file_path, 'Longformer_pubmed.json')
    with open(output_file_path, 'a', encoding='utf-8') as output_file:
        json.dump(output_list, output_file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main('./dataset/pubmed_10000.json', 'output_folder/')
