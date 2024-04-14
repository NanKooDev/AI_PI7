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

def get_results(user_bigrams: dict, user_trigrams: dict) -> dict:
    """Get the results of the analysis of the text.
    
    Args:
        bigrams (dict): The bigrams of the text.
        trigrams (dict): The trigrams of the text.
        
    Returns:
        dict: A dictionary with the results of the analysis.
    """
    
    results = {}
    
    for language in languages.keys():
        processed_file = open(processed_directory + languages[language], "r", encoding="utf-8")
        processed_data = json.loads(processed_file.read())
        processed_file.close()
        
        bigram_score = 0
        trigram_score = 0
        
        #region get bigram results
        get_bigram_results_start_time = time.time()
        
        for bigram in user_bigrams.keys():
            if bigram in processed_data["bigrams"]:
                bigram_score += 1
        
        get_bigram_results_stop_time = time.time()
        get_bigram_results_time = get_bigram_results_stop_time - get_bigram_results_start_time
        
        print("Time to get bigram results: ", get_bigram_results_time)
        
        #endregion
        
        #region get trigram results
        get_trigram_results_start_time = time.time()
                
        for trigram in user_trigrams.keys():
            if trigram in processed_data["trigrams"]:
                trigram_score += 1
                
        get_trigram_results_stop_time = time.time()
        get_trigram_results_time = get_trigram_results_stop_time - get_trigram_results_start_time
        
        print("Time to get trigram results: ", get_trigram_results_time)
        
        #endregion
        
        
        results[language] = {"bigrams": bigram_score, "trigrams": trigram_score}

    return results

def main() -> None:
    """Main function of the program.
    """
    
    user_input = input("Enter text to analyze: ")
    user_input = normalize_string(user_input)
    
    #region make & time ngrams
    
        #region make bigrams
    make_bigrams_start_time = time.time()
    bigrams = make_ngrams(user_input, 2)
    make_bigrams_stop_time = time.time()
    
    make_bigrams_time = make_bigrams_stop_time - make_bigrams_start_time
    print("Time to make bigrams: ", make_bigrams_time)
        #endregion
    
        #region make trigrams
    make_trigrams_start_time = time.time()
    trigrams = make_ngrams(user_input, 3)
    make_trigrams_stop_time = time.time()

    make_trigrams_time = make_trigrams_stop_time - make_trigrams_start_time
    print("Time to make trigrams: ", make_trigrams_time)
        #endregion
    
    #endregion
    
    results = get_results(bigrams, trigrams)
    
    #get every language and the amount of bigrams and trigrams that are in the text, and set in a dictionary
    #the language with the most bigrams and trigrams is the detected language
    results = {language: results[language]["bigrams"] + results[language]["trigrams"] for language in results.keys()}
        
    
    print("The language detected is: ", max(results, key=results.get))
    print("The results are: ", results)
    
    
    
    
    # #print("Version A")
    # #start_time = time.time()
    # calculate(user_input)
    # #print("Time: %s seconds" % (time.time() - start_time))
    
    # print("=====================================")
    
    # #print("Version B")
    # #start_time = time.time()
    # print(detect_language(user_input))
    # #print("Time: %s seconds" % (time.time() - start_time))

    # print("\n")

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