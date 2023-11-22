"""
Class to analyze files using the NLP framework
analyze.py: Implements the analyzer class
"""
__author__ = "Reema Sharma"

from collections import Counter
from textblob import TextBlob
from typing import Dict, Any
from src.exceptions.analyze_exceptions import UnsupportedAnalyzeTypeError


class Analyze:
    def __init__(self, analyze_type: str, **kwargs: Dict[str, Any]):
        self.analyze_type = analyze_type
        self.map = {
            'word_count': self._word_count,
            'polarity_score': self._polarity_score,
            'subjectivity_score': self._subjectivity_score,
            'word_frequency': self._word_frequency
        }

    def run(self, result_dict: Dict[str, Any], file_name, **kwargs: Dict[str, Any]):
        """
        Pipeline execution function to analyze the file <br><br>
        @param result_dict: Result dictionary to update with process results
        @param file_name: Name of file
        @return: Updated result_dict with new results
        """
        try:
            self.map[self.analyze_type](result_dict)
        except KeyError:
            raise UnsupportedAnalyzeTypeError(self.file_type)
        except Exception as e:
            raise e

        return result_dict

    def _word_count(self, result_dict, **kwargs: Dict[str, Any]):
        """
        Calculate word count in the processed text
        @param result_dict: Result dictionary to update with process results
        """
        processed_text = result_dict["processed_text"]
        word_count = sum(len(sentence.split()) for sentence in processed_text)
        result_dict["word_count"] = word_count
        return result_dict

    def _polarity_score(self, result_dict, **kwargs: Dict[str, Any]):
        """
        Calculate average sentiment score of the processed text using TextBlob
        @param result_dict: Result dictionary to update with process results
        """
        processed_text = result_dict["processed_text"]
        sentiment_polarities = []

        for sentence in processed_text:
            blob = TextBlob(sentence)
            sentiment_polarities.append(blob.sentiment.polarity)

        # Calculate overall sentiment score
        avg_polarity_score = sum(sentiment_polarities) / len(sentiment_polarities)
        result_dict["avg_polarity"] = avg_polarity_score
        return result_dict

    def _subjectivity_score(self, result_dict, **kwargs: Dict[str, Any]):
        """
        Calculate average sentiment subjectivity score of the processed text using TextBlob
        @param result_dict: Result dictionary to update with process results
        """
        processed_text = result_dict["processed_text"]
        subjectivities = []

        for sentence in processed_text:
            blob = TextBlob(sentence)
            subjectivities.append(blob.sentiment.subjectivity)

        # Calculate overall sentiment subjectivity score
        avg_sentiment_subjectivity = sum(subjectivities) / len(subjectivities)
        result_dict["avg_subjectivity"] = avg_sentiment_subjectivity
        return result_dict

    def _word_frequency(self, result_dict, **kwargs: Dict[str, Any]):
        """
        Calculate word frequency in the processed text
        @param result_dict: Result dictionary to update with process results
        """
        processed_text = result_dict["processed_text"]
        all_words = ' '.join(processed_text).split()
        word_freq = Counter(all_words)
        result_dict["word_frequency"] = word_freq
        return result_dict
