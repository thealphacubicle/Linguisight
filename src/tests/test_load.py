"""
Unit tests for the Load class
test_load.py: Tests the load.py module
"""
__author__ = "Srihari Raman"

import pytest

from src.exceptions.load_exceptions import ArgError
from src.load import Load
import os

########################################   FIXTURES   ########################################
@pytest.fixture(scope="module")
def sample_text_file():
    filename = "sample.txt"
    content = "This is the first sentence. Here is the second sentence."

    # Create and write to the text file
    with open(filename, 'w') as file:
        file.write(content)

    # Yield the filename for use in tests
    yield filename

    # Cleanup - remove the file after tests are done
    os.remove(filename)

########################################   STR TESTS   ########################################
def test_process_str_success():
    """
    Test the _process_str function for success
    """
    processor = Load(file_type="str")
    result_dict = {}
    file_name = "test_file"
    test_string = "Hello world. This is a test string."

    expected_sentences = ["Hello world.", "This is a test string."]
    result = processor._process_str(result_dict, file_name, file_text=test_string)
    print(result)

    assert file_name in result
    assert 'raw_text' in result[file_name]
    assert result[file_name]['raw_text'] == expected_sentences
    assert result[file_name]['processed_text'] == expected_sentences

def test_process_str_missing_file_text():
    """
    Test the _process_str function for failure when file_text is missing
    """
    processor = Load(file_type="str")
    result_dict = {}
    file_name = "test_file"

    with pytest.raises(ArgError):
        processor._process_str(result_dict, file_name)

def test_process_str_general_exception():
    processor = Load(file_type="str")
    result_dict = {}
    file_name = "test_file"

    with pytest.raises(Exception):
        processor._process_str(result_dict, file_name, file_text=None)


#################################   CSV TESTS   #################################
def test_process_csv_success():
    processor = Load(file_type="csv")
    result_dict = {}
    file_name = "sample_csv"
    csv_target_text_col = "sentences"
    filepath = ("https://raw.github.khoury.northeastern.edu/ramansr04/Linguisight/main/src/tests/sample_file.csv?token"
                "=GHSAT0AAAAAAAAARFTQR7JQQIGDM7FNJQR4ZLE4GZA")

    result = processor._process_csv(result_dict, file_name, filepath=filepath, csv_target_text_col=csv_target_text_col)

    expected_sentences = [
        'This is a sentence.',
        'This is another sentence.',
        'This is a sentence.',
        'This is another sentence.',
        'This is a third sentence.'
    ]

    assert file_name in result
    assert 'raw_text' in result[file_name]
    assert result[file_name]['raw_text'] == expected_sentences
    assert result[file_name]['processed_text'] == expected_sentences

def test_process_csv_missing_column():
    processor = Load(file_type="csv")
    result_dict = {}
    file_name = "sample_csv"
    filepath = ("https://raw.github.khoury.northeastern.edu/ramansr04/Linguisight/main/src/tests/sample_file.csv?token"
                "=GHSAT0AAAAAAAAARFTQR7JQQIGDM7FNJQR4ZLE4GZA")

    with pytest.raises(ArgError):
        processor._process_csv(result_dict, file_name, filepath=filepath)

def test_process_csv_file_not_accessible():
    processor = Load(file_type="csv")
    result_dict = {}
    file_name = "sample_csv"
    csv_target_text_col = "sentences"

    with pytest.raises(Exception):
        processor._process_csv(result_dict, file_name, csv_target_text_col=csv_target_text_col)

#################################   TXT TESTS   #################################
#TODO: Add tests for _process_txt