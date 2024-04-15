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
    
    #open raw file and read string
    raw_file = open(raw_directory + language, "r", encoding="utf-8")
    string = raw_file.read()
    raw_file.close()
    
    #normalize string and create bigrams and trigrams
    string = normalize_string(string)
    bigrams = make_ngrams(string, 2)
    trigrams = make_ngrams(string, 3)
    
    #create json file with bigrams and trigrams
    processed_file = open(processed_directory + language.split(".")[0] + ".json", "w", encoding="utf-8")
    processed_file.write(json.dumps({"bigrams": bigrams, "trigrams": trigrams}))
    processed_file.close()
        
    return
        
def normalize_string(string: str) -> str:
    """Normalize a string by removing all non-alphabetic characters and converting all characters to lowercase.

    Args:
        string (str): The string to normalize.

    Returns:
        str: The normalized string.
    """
    
    # Remove all non-alphabetic characters
    string = ''.join([char for char in string if char.isalpha() or char.isspace()])
    
    # Convert all characters to lowercase
    string = string.lower()
    
    return string

def make_ngrams(string: str, n: int) -> dict:
    """Create n-grams from a given string.

    Args:
        string (str): The string to create n-grams from.
        n (int): The size of the n-grams.

    Returns:
        dict: A dict of n-grams and their frequencies.
    """
    
    ngrams = {}
    for i in range(len(string) - n + 1): # Loop over the string from 0 to len(string) - n + 1. We need to subtract n because we need to have n characters left to create a ngram
        ngram = string[i:i+n] # Get the ngram by slicing the string from i to i+n where n is the size of the ngram
        if ngram in ngrams:
            ngrams[ngram] += 1
        else:
            ngrams[ngram] = 1
            
    return ngrams

def get_normalized_corpora() -> str:
    """Get the normalized corpora.
    
    Returns:
        str: The normalized corpora.
    """
    
    corpora_string = ""
    
    for language in languages:
        raw_file = open(raw_directory + language + ".txt", "r", encoding="utf-8")
        corpora_string += raw_file.read()
        raw_file.close()
        
    return normalize_string(corpora_string)

def probability_of_ngram(ngram: str, corpus_ngrams: dict) -> float:
    """Calculate the probability of an ngram in the corpus.

    Args:
        ngram (str): The ngram to calculate the probability of.
        corpus_ngrams (dict): The ngrams of the corpus.

    Returns:
        float: The probability of the ngram in the corpus.
    """
    
    ngram_count = corpus_ngrams.get(ngram, 0) + 1 # Add 1 to the count of the ngram to prevent division by zero, use .get() to return 0 if the ngram is not in the corpus
    
    total_ngrams = (sum(corpus_ngrams.values()) + 1) * len(corpus_ngrams) # Add 1 to the total ngrams to prevent division by zero and multiply by the number of ngrams to prevent the probability from being 1
    
    # P(ngram) = count(ngram) / total ngrams
    return ngram_count / total_ngrams
    
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
    
    # P(string|language) = P(trigram1) * P(trigram2) * ... * P(trigramN) / P(bigram1) * P(bigram2) * ... * P(bigramN) * P(language)
    return product_of_trigram_chance / product_of_bigram_chance * language_chance

def get_results_using_frequency(trigrams: dict) -> dict:
    """Get the results of the analysis of the string.
    
    Args:
        trigrams (dict): The trigrams of the string.
        
    Returns:
        dict: A dictionary with the results of the analysis.
    """
    
    results = {}
    
    for language in languages:
        language_ngrams = read_ngrams_from_file(language)
        
        score = 0
                
        for trigram in trigrams:
            if trigram in language_ngrams["trigrams"]:
                bigram = trigram[:2]
                score += language_ngrams["trigrams"][trigram] / language_ngrams["bigrams"][bigram]
        
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
    """Get the results of the analysis of the string.
    
    Args:
        user_trigrams (dict): The trigrams of the string.
        
    Returns:
        dict: A dictionary with the results of the analysis.
    """
    
    probabilities = {}
    
    corpora_trigrams = make_ngrams(get_normalized_corpora(), 3)
    
    for language in languages:
        language_ngrams = read_ngrams_from_file(language)
        
        product_of_trigrams = 1
        product_of_bigrams = 1

        for trigram in user_trigrams:
            for _ in range(user_trigrams[trigram]):
                product_of_trigrams *= probability_of_ngram(trigram, language_ngrams["trigrams"])
                product_of_bigrams *= probability_of_ngram(trigram[:2], language_ngrams["bigrams"])
        
        probabilities[language] = probability_of_string_given_language(\
            product_of_trigrams,\
            product_of_bigrams,\
            probability_of_language(language_ngrams["trigrams"], corpora_trigrams))
        
    return probabilities

def get_probabilities_per_key_from_frequency(trigrams: dict) -> dict:
    """Get the probabilities of the trigrams based on their frequency.
    
    Args:
        trigrams (dict): The trigrams of the string.
        
    Returns:
        dict: A dictionary with the probabilities of the trigrams.
    """
    
    probabilities = {}
    
    for trigram in trigrams:
        probabilities[trigram] = trigrams[trigram] / sum(trigrams.values())
    
    return probabilities

def main() -> None:
    """Main function of the program.
    
    Args:
        None
        
    Returns:
        None        
    """
    
    string = input("Enter string to analyze: ")
    string = normalize_string(string)
    
    trigrams = make_ngrams(string, 3)
    
    start_time = time.time()
    freq_results = get_results_using_frequency(trigrams)
    print("freq Time: %s seconds" % (time.time() - start_time))
    
    start_time = time.time()
    prob_results = get_results_using_probability(trigrams)
    print("prob Time: %s seconds" % (time.time() - start_time))
    
    freq_probability = get_probabilities_per_key_from_frequency(freq_results)
    prob_probability = get_probabilities_per_key_from_frequency(prob_results)
    
    freq_probability = sorted(freq_probability.items(), key=lambda x: x[1], reverse=True)
    prob_probability = sorted(prob_probability.items(), key=lambda x: x[1], reverse=True)
    
    
    
    print("The language detected using freq is:", max(freq_results, key=freq_results.get))
    print("The language detected using prob is:", max(prob_results, key=prob_results.get))
    
    print("The freq results are: ", sorted(freq_results.items(), key=lambda x: x[1], reverse=True))
    print("The prob results are: ", sorted(prob_results.items(), key=lambda x: x[1], reverse=True))
    
    print("The freq probabilities are:", freq_probability)
    print("The prob probabilities are:", prob_probability)

    print("For the string: %s" % string)
    print("My prediction is that the language is: %s. I am %.2f%% confident of this." % (prob_probability[0][0], prob_probability[0][1] * 100))

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

while True:
    main()