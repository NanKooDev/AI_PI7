import io
import os
import re
import json
import unicodedata
import time

languages = {
    'Dutch': 'dutch.txt',
    'English': 'english.txt',
    'German': 'german.txt'
}

def normalize_text(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

def preprocess_text(text):
    text = normalize_text(text)
    text = re.sub(r'[^A-Za-zÀ-ÿ ]+', '', text.lower())
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def count_text_length(text):
    return len(text)

def generate_ngrams(text, n):
    ngrams = []
    for i in range(len(text)):
        ngrams.append(text[i: i + n])
    return ngrams

def count_ngram_frequency(ngrams):
    ngram_freq = {}
    for ngram in ngrams:
        ngram_freq[ngram] = ngram_freq.get(ngram, 0) + 1
    return ngram_freq

def calculate_score(ngrams_input, ngrams_lang, corpus_len, lang_len):
    overlap = set(ngrams_input.keys()) & set(ngrams_lang.keys())
    overlap_freq_input = sum(ngrams_input[ngram] for ngram in overlap)
    overlap_freq_lang = sum(ngrams_lang[ngram] for ngram in overlap)
    total_freq_input = sum(ngrams_input.values())
    total_freq_lang = sum(ngrams_lang.values())

    factor = 1 - (lang_len / corpus_len)

    score = overlap_freq_input / total_freq_input * overlap_freq_lang / total_freq_lang * factor
    return score

def apply_laplace_smoothing(language, file=0):
    V = calculate_vocabulary_size('/raw/nld.txt')
    with open(f'/json/{language}_3.json', 'r', encoding='utf-8') as f:
        trigram_counts = json.load(f)
    with open(f'/json/{language}_2.json', 'r', encoding='utf-8') as f:
        bigram_counts = json.load(f)

    trigram_probs = {}
    for trigram, count_tri in trigram_counts.items():
        bigram = trigram[:2]
        count_bi = bigram_counts.get(bigram, 0)
        prob = (count_tri + 1) / (count_bi + V)
        trigram_probs[trigram] = prob

    if file == 1:
        with open(f'/chances/{language}.json', "w", encoding="utf-8") as f:
            json.dump(trigram_probs, f)
    return trigram_probs

def calculate_vocabulary_size(text_path):
    with open(text_path, 'r', encoding='utf-8') as f:
        text = f.read().lower()
    bigrams = set(zip(text, text[1:]))
    return len(bigrams)

def calculate(text):
    preprocessed_text = preprocess_text(text)
    bigrams_input = generate_ngrams(preprocessed_text, 2)
    trigrams_input = generate_ngrams(preprocessed_text, 3)

    corpus_len = sum(count_text_length(preprocessed_text) for _ in languages.values())

    scores = {}
    for lang, filename in languages.items():
        with open(f"/raw/{filename}", 'r', encoding='utf-8') as file:
            lang_text = file.read()
            preprocessed_lang_text = preprocess_text(lang_text)
            bigrams_lang = generate_ngrams(preprocessed_lang_text, 2)
            trigrams_lang = generate_ngrams(preprocessed_lang_text, 3)
            score_bigrams = calculate_score(bigrams_input, count_ngram_frequency(bigrams_lang), corpus_len, count_text_length(preprocessed_lang_text))
            score_trigrams = calculate_score(trigrams_input, count_ngram_frequency(trigrams_lang), corpus_len, count_text_length(preprocessed_lang_text))
            scores[lang] = (score_bigrams + score_trigrams) / 2

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    print(f"The language {sorted_scores[0][0]} is detected: {sorted_scores[0][1]}")
    for lang, score in sorted_scores[1:]:
        print(f"{lang}: {score}")

def detect_language(input_text):
    trigrams_input = generate_ngrams(preprocess_text(input_text), 3)
    language_probabilities = {}
    for filename in os.listdir('/json/'):
        if filename.endswith('_3.json'):
            language = filename.split('_')[0]
            trigram_probs = apply_laplace_smoothing(language)
            probability = 1
            for trigram in trigrams_input:
                probability *= trigram_probs.get(trigram, 1e-10)  # use a small probability for unseen trigrams
            language_probabilities[language] = probability
    return sorted(language_probabilities.items(), key=lambda x: x[1], reverse=True)

def process_input():
    text = int(input("Enter text to check: "))

    print("Version A")
    start_time = time.time()
    calculate(text)
    print("Time: %s seconds" % (time.time() - start_time))
    
    print("=====================================")
    
    print("Version B")
    start_time = time.time()
    print(detect_language(text))
    print("Time: %s seconds" % (time.time() - start_time))

    print("\n")


while True:
    process_input()
