"""
Class to load files to be processed
load.py: Class implementation of Loader
"""
__author__ = "Srihari Raman"

# Imports
from typing import Dict, Any
import pandas as pd
from nltk import sent_tokenize

from src.exceptions.load_exceptions import UnsupportedFileTypeError, ArgError
import nltk

nltk.download('punkt')

class Load:
    """
    Class implementation to load various files <br><br>
    This class is used to load files to be processed by the NLP framework <br><br>
    """

    def __init__(self, file_type, **kwargs):
        self.map = {
            'csv': self._process_csv,
            'txt': self._process_txt,
            'str': self._process_str
        }

        if file_type not in self.map.keys():
            raise UnsupportedFileTypeError(file_type)

        self.file_type = file_type
        self.kwargs = kwargs

    def run(self, result_dict: Dict[str, Any], file_name: str, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Pipeline execution function to load and process the file.

        This function determines the file type from the file name, then
        delegates the processing of the file to the corresponding handler
        based on the file type.

        Parameters:
        - result_dict (Dict[str, Any]): The result dictionary to be updated with the process results. It's a dictionary
        with string keys and values of any type.
        - file_name (str): The name of the file to be processed. It's
          expected to be a string.
        - kwargs (Dict[str, Any]): OPTIONAL Keyword arguments to aid in the processing of functions

        Returns:
        Dict[str, Any]: The updated result dictionary containing the new results after processing the file.

        Raises:
        UnsupportedFileTypeError: If the file type is not supported for processing.
        """
        try:
            result_dict = self.map[self.file_type](result_dict, file_name, **kwargs)
        except KeyError:
            raise UnsupportedFileTypeError(self.file_type)
        except Exception as e:
            raise e

        return result_dict

    def _process_csv(self, result_dict: Dict[str, Any], file_name: str, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Service function to process CSV files

        This function utilizes type inferencing through built-in Pandas dataframes and extracts the text from the
        specified column in the CSV file as a list of strings. The list of strings is then added to the resultant
        dictionary

        Parameters:
        - result_dict (Dict[str, Any]): The result dictionary to be updated with the process results. It's a dictionary
        with string keys and values of any type.
        - file_name (str): The name of the file to be processed. It's
          expected to be a string.
        - kwargs (Dict[str, Any]): OPTIONAL Keyword arguments to aid in the processing of

        Returns:
        Dict[str, Any]: The updated result dictionary containing the new results after processing the file.

        Raises:
        KeyError: If the CSV text column is not specified in the keyword arguments.
        UnsupportedFileTypeError: If the file type is not supported for processing.
        """
        # Initialize the result dictionary
        result_dict[file_name] = {}
        kwargs = {key: value for key, value in kwargs['kwargs'].items() if value is not None}


        # Check if required parameters are passed in kwargs
        try:
            trg_text_col = kwargs["csv_target_text_col"]
            filepath = kwargs["filepath"]
        except KeyError:
            raise ArgError(["csv_target_text_col", "filepath"])
        except Exception as e:
            raise e

        # Assert that the target text column is of type str
        assert isinstance(trg_text_col, str), "CSV text column must be of type str"

        # Read in text from CSV column into a list
        df = pd.read_csv(filepath)

        # Initialize the list to store individual sentences
        all_sentences = []

        # Iterate over each row and split the text into sentences
        for text in df.loc[:, trg_text_col]:
            sentences = sent_tokenize(text)
            all_sentences.extend(sentences)

        # Update the result dictionary
        result_dict[file_name]["raw_text"] = all_sentences
        result_dict[file_name]["processed_text"] = all_sentences

        return result_dict

    def _process_txt(self, result_dict: Dict[str, Any], file_name: str, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes a text file and extracts sentences.

        This function reads the content of a text file specified by `file_name` and uses the NLTK library
        for sentence tokenization. The extracted sentences are added to `result_dict` under the key 'raw_text'.

        The NLTK's `sent_tokenize` is used for accurate sentence boundary detection, ensuring that the
        semantic integrity of the text is maintained.

        Parameters:
            - result_dict (Dict[str, Any]): A dictionary to be updated with the processed results.
                The dictionary has string keys and values of any type.
            - file_name (str): The path to the text file to be processed.
            - kwargs (Dict[str, Any]): OPTIONAL Keyword arguments to aid in the processing of


        Returns:
            Dict[str, Any]: The updated result dictionary containing the list of extracted sentences
            under the 'raw_text' key.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            Exception: For handling unexpected errors during file reading or processing.

        Note:
            NLTK's 'punkt' tokenizer dataset is required for this function. Ensure it's downloaded
            using `nltk.download('punkt')` before calling this function.
        """
        # Initialize the result dictionary
        result_dict[file_name] = {}
        kwargs = {key: value for key, value in kwargs['kwargs'].items() if value is not None}


        # Check if required parameters are passed in kwargs
        try:
            file_path = kwargs["file_path"]
        except KeyError:
            raise ArgError("file_path")
        except Exception as e:
            raise e

        # Process the text file and store it in the result dictionary
        try:
            with open(file_path, 'r') as file:
                text = file.read()

            # Using nltk for sentence tokenization
            sentences = nltk.tokenize.sent_tokenize(text)

            # Clean up empty sentences
            for sentence in sentences:
                if sentence == '':
                    sentences.remove(sentence)

            result_dict[file_name]['raw_text'] = sentences
            result_dict[file_name]["processed_text"] = sentences

        except FileNotFoundError:
            raise FileNotFoundError(f"File {file_name} not found")

        except Exception as e:
            raise e

        return result_dict

    def _process_str(self, result_dict: Dict[str, Any], file_name: str, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """
            Processes sentences passed in as strings

            This function reads in a string of one or more sentences and splits into a list of sentences.

            The NLTK's `sent_tokenize` is used for accurate sentence boundary detection, ensuring that the
            semantic integrity of the text is maintained.

            Parameters:
                - result_dict (Dict[str, Any]): A dictionary to be updated with the processed results.
                        The dictionary has string keys and values of any type.
                - file_name (str): The path to the text file to be processed. Default set to empty string since
                        this function is used to process strings.
                - kwargs (Dict[str, Any]): OPTIONAL Keyword arguments to aid in the processing of


            Returns:
                Dict[str, Any]: The updated result dictionary containing the list of extracted sentences
                under the 'raw_text' key.

            Raises:
                FileNotFoundError: If the specified file does not exist.
                Exception: For handling unexpected errors during file reading or processing.

            Note:
                NLTK's 'punkt' tokenizer dataset is required for this function.
                file_text parameter MUST be passed in kwargs!!!
        """
        # Initialize the result dictionary
        result_dict[file_name] = {}
        kwargs = {key: value for key, value in kwargs['kwargs'].items() if value is not None}


        # Check if required parameters are passed in kwargs
        try:
            file_text = kwargs["file_text"]

        except KeyError:
            raise ArgError("file_text")

        except Exception as e:
            raise e

        # Process the string and store it in the result dictionary
        sentences = nltk.tokenize.sent_tokenize(file_text)
        result_dict[file_name]['raw_text'] = sentences
        result_dict[file_name]["processed_text"] = sentences

        return result_dict
