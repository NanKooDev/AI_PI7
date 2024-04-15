import json
import os
import time

corpus_directory = "PI7 deel 3/corpus/"
raw_directory = corpus_directory + "raw/"
processed_directory = corpus_directory + "processed/"

def process_file(language : str) -> None:
    """Process a raw language file and save the processed data to a new file.

    Args:
        language (str): The name of the language file to process.
        
    Returns:
        None
    """
    
    #open file and read text
    file = open(raw_directory + language, "r", encoding="utf-8")
    text = file.read()
    file.close()
    
    #normalize text and create bigrams and trigrams
    processed_text = normalize_string(text)
    bigrams = make_ngrams(processed_text, 2)
    trigrams = make_ngrams(processed_text, 3)
    
    #create json file with bigrams and trigrams
    processed_file = open(processed_directory + language.split(".")[0] + ".json", "w", encoding="utf-8")
    processed_file.write(json.dumps({"bigrams": bigrams, "trigrams": trigrams}))
    processed_file.close()
        
    return
        
def normalize_string(text: str) -> str:
    """Normalize a string by removing all non-alphabetic characters and converting all characters to lowercase.

    Args:
        text (str): The string to normalize.

    Returns:
        str: The normalized string.
    """
    
    # Remove all non-alphabetic characters
    text = ''.join([char for char in text if char.isalpha() or char.isspace()])
    # Convert all characters to lowercase
    text = text.lower()
    return text

def make_ngrams(text: str, n: int) -> dict:
    """Create n-grams from a given text.

    Args:
        text (str): The text to create n-grams from.
        n (int): The size of the n-grams.

    Returns:
        dict: A dict of n-grams and their frequencies.
    """
    ngrams = {}
    for i in range(len(text) - n + 1):
        ngram = text[i:i+n]
        if ngram in ngrams:
            ngrams[ngram] += 1
        else:
            ngrams[ngram] = 1
    return ngrams

def get_normalized_corpus() -> str:
    """Get the normalized corpus.
    
    Returns:
        str: The normalized corpus.
    """
    corpus_text = ""
    
    for language in languages.keys():
        raw_file = open(processed_directory + languages[language], "r", encoding="utf-8")
        corpus_text += raw_file.read()
        raw_file.close()
        
    return normalize_string(corpus_text)

def probability_of_ngram(ngram: str, corpus_ngrams: dict) -> float:
    """Calculate the probability of a ngram in the corpus.

    Args:
        ngram (str): The ngram to calculate the probability of.
        corpus_ngrams (dict): The ngrams of the corpus.

    Returns:
        float: The probability of the ngram in the corpus.
    """
    ngram_count = 0.0000000001
    if ngram in corpus_ngrams:
        ngram_count = corpus_ngrams[ngram]
    
    # P(ngram) = count(ngram) / sum(all ngrams)
    return ngram_count / sum(corpus_ngrams.values())

def probability_of_language(language_trigrams: dict, corpus_trigrams: dict) -> float:
    """Calculate the probability of a language.

    Args:
        language_trigrams (dict): The trigrams of the language.
        corpus_trigrams (dict): The trigrams of the corpus.

    Returns:
        float: The probability of the language.
    """
    # P(language) = sum(all trigrams in language) / sum(all trigrams)
    return sum(language_trigrams.values()) / sum(corpus_trigrams.values())

def probability_of_string_given_language(product_of_trigram_chance: float, product_of_bigram_chance: float, language_chance: float) -> float:
    """Calculate the probability of a string given a language.
    
    Args:
        product_of_trigram_chance (float): The product of the trigram chances.
        product_of_bigram_chance (float): The product of the bigram chances.
        language_chance (float): The chance of the language.
        
    Returns:
        float: The probability of the string given the language.
    """
    return product_of_trigram_chance / product_of_bigram_chance * language_chance

def get_results_using_frequency(user_trigrams: dict) -> dict:
    """Get the results of the analysis of the text.
    
    Args:
        trigrams (dict): The trigrams of the text.
        
    Returns:
        dict: A dictionary with the results of the analysis.
    """
    
    results = {}
    
    for language in languages.keys():
        processed_data = read_ngrams_from_file(language)
        
        score = 0
                
        for trigram in user_trigrams.keys():
            if trigram in processed_data["trigrams"]:
                score += processed_data["trigrams"][trigram] / processed_data["bigrams"][trigram[:2]]
        
        results[language] = score

    return results

def read_ngrams_from_file(language: str) -> dict:
    """Read n-grams of a language.
    
    Args:
        language (str): The language to read the n-grams from.
        
    Returns:
        dict: A dictionary with the n-grams and their frequencies.
    """
    
    file = open(processed_directory + languages[language], "r", encoding="utf-8")
    ngrams = json.loads(file.read())
    file.close()
    
    return ngrams

def get_results_using_probability(user_trigrams: dict) -> dict:
    """Get the results of the analysis of the text.
    
    Args:
        user_trigrams (dict): The trigrams of the text.
        
    Returns:
        dict: A dictionary with the results of the analysis.
    """
    probabilities = {}
    
    product_of_trigrams = 1
    product_of_bigrams = 1
    for trigram in user_trigrams:
        for _ in range(user_trigrams[trigram]):
            product_of_trigrams *= probability_of_ngram(trigram, make_ngrams(corpus, 3))
            product_of_bigrams *= probability_of_ngram(trigram[:2], make_ngrams(corpus, 2))
        
    for language in languages.keys():
        processed_data = read_ngrams_from_file(language)
        
        probabilities[language] = probability_of_string_given_language(\
            product_of_trigrams,\
            product_of_bigrams,\
            probability_of_language(processed_data["trigrams"], make_ngrams(corpus, 3)))
        
    return probabilities

def get_probabilities_from_frequency(trigrams: dict) -> dict:
    """Get the probabilities of the trigrams based on their frequency.
    
    Args:
        trigrams (dict): The trigrams of the text.
        
    Returns:
        dict: A dictionary with the probabilities of the trigrams.
    """
    
    probabilities = {}
    
    for trigram in trigrams.keys():
        probabilities[trigram] = trigrams[trigram] / sum(trigrams.values())
    
    return probabilities

def main() -> None:
    """Main function of the program.
    """
    
    user_input = input("Enter text to analyze: ")
    user_input = normalize_string(user_input)
    
    trigrams = make_ngrams(user_input, 3)
    
    start_time = time.time()
    freq_results = get_results_using_frequency(trigrams)
    print("freq Time: %s seconds" % (time.time() - start_time))
    
    start_time = time.time()
    prob_results = get_results_using_probability(trigrams)
    print("prob Time: %s seconds" % (time.time() - start_time))
        
    
    print("The language detected using freq is: ", max(freq_results, key=freq_results.get))
    print("The language detected using prob is: ", max(prob_results, key=prob_results.get))
    
    print("The freq results are: ", sorted(freq_results.items(), key=lambda x: x[1], reverse=True))
    print("The prob results are: ", sorted(prob_results.items(), key=lambda x: x[1], reverse=True))

def check_language_files() -> None:
    """Check if all raw language files have been processed and process them if necessary.
    
    Returns:
        None
    """
    
    # Create a dictionary with the filenames as keys and the full file names as values
    raw_languages = {file.split(".")[0]: file for file in os.listdir(raw_directory) if file.endswith(".txt")} 
    print("The known raw languages are: ", raw_languages)

    # Create a dictionary with the filenames as keys and the full file names as values
    processed_languages = {file.split(".")[0]: file for file in os.listdir(processed_directory) if file.endswith(".json")} 
    print("The known processed languages are: ", processed_languages)

    # Check if all raw language files have been processed
    for language in raw_languages.keys():
        if processed_languages.get(language) is None:
            print(f"Processed file for {language} is missing")
            print("Processing the file now")
            process_file(raw_languages[language])
            print("File processed")

def get_languages() -> dict:
    """Get all processed language files.
    
    Returns:
        dict: A dictionary with the languages as keys and the full file names as values.
    """
    check_language_files()
    
    return {file.split(".")[0]: file for file in os.listdir(processed_directory) if file.endswith(".json")} 

languages = get_languages()
corpus = get_normalized_corpus()

while True:
    main()