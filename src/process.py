"""
Class to process files using the NLP framework
analyze.py: Implements the Process class
"""
__author__ = "Sriya Vuppala"

import urllib.request as url
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import re
from typing import Dict, Any
from src.exceptions.process_exceptions import UnsupportedProcessTypeError


class Process:
    """
    Class implementation of the Processing part of the pipeline <br><br>
    This class is used to process files using the NLP framework <br><br>
    """

    def __init__(self, process_type: str):
        nltk.download('wordnet')
        self.process_type = process_type
        self.map = {
            'stop_words': self.filter_stopwords,
            'punctuation': self.filter_punctuation,
            'lemmatize': self.lemmatize,
            'stem': self.stem,
            'capitalization': self.remove_capitalization
        }
        self.stop_words = self.load_stopwords()

    def run(self, result_dict: Dict[str, Any], file_name, **kwargs: Dict[str, Any]):
        """
        Pipeline execution function to process the file <br><br>
        @param result_dict: Result dictionary to update with process results
        @param file_name: Name of file
        @param kwargs (Dict[str, Any]): OPTIONAL Keyword arguments to aid in the processing of functions
        @return: Updated result_dict with new results
        """
        try:
            result_dict = self.map[self.process_type](result_dict, file_name, **kwargs)
        except KeyError:
            raise UnsupportedProcessTypeError(self.process_type)
        except Exception as e:
            raise e

        return result_dict

    def filter_stopwords(self, result_dict, file_name, **kwargs: Dict[str, Any]):
        """
        Filters the stop words from the loaded list of sentences
        @param result_dict: Result dictionary to update with process results
        @param kwargs (Dict[str, Any]): OPTIONAL Keyword arguments to aid in the processing of functions
        @return: Updated result_dict with new results
        """
        stop_words = self.stop_words
        processed_text = result_dict[file_name]["processed_text"]

        for i in range(len(processed_text)):
            # Splitting the sentence into words
            words = processed_text[i].split()
            # Removing stop words
            filtered_words = [word for word in words if word not in stop_words]
            # Joining the filtered words to form the updated sentence
            processed_text[i] = ' '.join(filtered_words)

        # Adding processed text to result dictionary
        result_dict["processed_text"] = processed_text
        return result_dict

    # Source: https://docs.python.org/3/howto/urllib2.html
    def load_stopwords(self, sw_url=
    "https://raw.githubusercontent.com/stopwords-iso/stopwords-en/master/stopwords-en.txt",
                       **kwargs: Dict[str, Any]):
        """
        @param sw_url: a url directed to a list of stop words
        @param kwargs (Dict[str, Any]): OPTIONAL Keyword arguments to aid in the processing of functions
        @return: a list of stop words as strings
        """
        with url.urlopen(sw_url) as response:
            content = response.read().decode('utf-8')
        # Storing stop words in a list
        stop_words = [word.strip() for word in content.split('\n')]
        return stop_words

    def filter_punctuation(self, result_dict, file_name, **kwargs: Dict[str, Any]):
        """
        Removes punctuation from the loaded list of sentences
        @param result_dict: Result dictionary to update with process results
        @param kwargs (Dict[str, Any]): OPTIONAL Keyword arguments to aid in the processing of functions
        @return: Updated result_dict with new results
        """
        processed_text = result_dict[file_name]["processed_text"]

        for i in range(len(processed_text)):
            # Removing punctuation
            processed_text[i] = re.sub('[^\w\s]', '', processed_text[i])
        # Adding processed text to result dictionary
        result_dict["processed_text"] = processed_text
        return result_dict

    # source: https://www.kdnuggets.com/2018/11/text-preprocessing-python.html
    def lemmatize(self, result_dict, file_name, **kwargs: Dict[str, Any]):
        """
        Lemmatizes words in the loaded list of sentences
        @param result_dict: Result dictionary to update with process results
        @param kwargs (Dict[str, Any]): OPTIONAL Keyword arguments to aid in the processing of functions
        @return: Updated result_dict with new results
        """
        processed_text = result_dict[file_name]["processed_text"]
        lem = WordNetLemmatizer()

        for i in range(len(processed_text)):
            # Tokenize the sentence into words
            words = word_tokenize(processed_text[i])
            # Lemmatize each word
            lem_words = [lem.lemmatize(word) for word in words]
            # Update the sentence to the lemmatized version
            processed_text[i] = ' '.join(lem_words)
        # Adding processed text to result dictionary
        result_dict["processed_text"] = processed_text
        return result_dict

    def stem(self, result_dict, file_name, **kwargs: Dict[str, Any]):
        """
        stems words in the loaded list of sentences
        @param result_dict: Result dictionary to update with process results
        @param kwargs (Dict[str, Any]): OPTIONAL Keyword arguments to aid in the processing of functions
        @return: Updated result_dict with new results
        """
        processed_text = result_dict[file_name]["processed_text"]
        stemmer = PorterStemmer()
        # Iterating through every sentence in the list
        for i in range(len(processed_text)):
            # Tokenizing the sentence into words
            tokenized_words = word_tokenize(processed_text[i])
            # Stemming each word
            stem_words = [stemmer.stem(word) for word in tokenized_words]
            # Update the sentence to the stemmed version
            processed_text[i] = ' '.join(stem_words)
        # Adding processed text to result dictionary
        result_dict["processed_text"] = processed_text
        return result_dict

    def remove_capitalization(self, result_dict, file_name, **kwargs: Dict[str, Any]):
        """
        Removes capitalization from the loaded list of sentences
        @param result_dict: Result dictionary to update with process results
        @param kwargs (Dict[str, Any]): OPTIONAL Keyword arguments to aid in the processing of functions
        @return: Updated result_dict with new results
        """
        processed_text = result_dict[file_name]["processed_text"]

        for i in range(len(processed_text)):
            # Converting the sentence to lowercase
            processed_text[i] = processed_text[i].lower()
        # Adding processed text to result dictionary
        result_dict["processed_text"] = processed_text
        return result_dict
