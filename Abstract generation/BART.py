import torch
from transformers import BartTokenizer, BartForConditionalGeneration
import json
import os
import sys

BART_PATH = 'facebook/bart-large-cnn'
bart_model = BartForConditionalGeneration.from_pretrained(BART_PATH)
bart_tokenizer = BartTokenizer.from_pretrained(BART_PATH)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

bart_model.to(device)
bart_model.eval()

num_beams = 4
# 添加不同section对应的最大输出长度
section_max_lengths = {
    'background': 90,
    'method': 75,
    'result': 90,
    'conclusion': 45
}
processed_index = 0

def bart_summarize(input_text, num_beams, num_words):
    input_text = str(input_text)
    input_text = ' '.join(input_text.split())
    input_tokenized = bart_tokenizer.encode(input_text, return_tensors='pt').to(device)
    summary_ids = bart_model.generate(input_tokenized,
                                      num_beams=int(num_beams),
                                      no_repeat_ngram_size=2,
                                      length_penalty=1.0,
                                      min_length=20,
                                      max_length=int(num_words),
                                      early_stopping=True,
                                      remove_invalid_values=True)
    output = [bart_tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids]
    return output[0]

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

num_words = 300
def process_article(article, articles_length):
    global processed_index
    processed_index += 1
    print(f"Processing article {processed_index} out of {articles_length}")

    result = []
    article_id = article["article_id"]
    sections = article["sections"]
    filtered_sections = {key: value for key, value in sections.items() if key != 'No match'}
    for section_name, section_text in filtered_sections.items():
        final_text = truncate_text(section_text, 1024)
        summaries = bart_summarize(final_text, num_beams, num_words)
        section_result = {section_name: summaries}
        result.append(section_result)

    # Save partial result for each article
    full_summary = {"article_id": article_id, "summary": result}
    return full_summary

def main(input_file_path, output_file_path, start_index=None):
    with open(input_file_path, 'r', encoding='utf-8') as json_file:
        articles = json.load(json_file)[:2000]

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
    output_file_path = os.path.join(output_file_path, 'BART_pubmed.json')
    with open(output_file_path, 'a', encoding='utf-8') as output_file:
        json.dump(output_list, output_file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main('./dataset/pubmed_10000.json', 'output_folder/')
