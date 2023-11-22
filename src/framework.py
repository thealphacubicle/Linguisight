"""
framework.py: Class implementation; Framework built for an NLP pipeline
"""
__author__ = "Srihari Raman, Reema Sharma, Sriya Vuppala"

# Imports
from pipeline import Pipeline
from wordcloud import WordCloud
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import frontend.sankey as sk


class NLPAnalyzer:
    """
    Class implementation of the NLPAnalyzer <br><br>
    This class is used to build the overarching NLP framework <br><br>
    """

    def __init__(self, files, parser, **kwargs):
        """
        Constructor to take in multiple files as tuples -> [(file_name, file_path), ...]
        @param files: Tuples of files to be analyzed
        @param parser: Parser object to be used for parsing the files
        """
        self.files = files
        self.parser = parser
        self.results = {}
        self.kwargs = kwargs

    def analyze(self):
        """
        Runs the framework to analyze the files using the parser
        """
        for file_name, file_path in self.files:
            self.results[file_name] = self.parser.execute(file_name, file_path, kwargs=self.kwargs)

    def visualize_pipeline(self, steps):
        """
        Visualizes the pipeline of steps
        @param steps: Steps to be visualized
        @return: None
        """
        Pipeline.visualize_pipeline(steps)

    def wordcount_sankey(self, word_list=None, k=5):
        """
        Generates a Sankey diagram of the word count
        @param word_list: List of words to be visualized (default: top k words)
        @param k: Number of top words to be visualized (default: 5)
        @return: None
        """
        file_word_df = pd.DataFrame(columns=['file_name', 'word'])
        rows_to_add_list = []

        for file_name, file_info in self.results.items():
            word_freq = file_info['word_frequency']

            # Determine words to include based on word_list or top k words
            words_to_use = word_list if word_list else [word for word, _ in word_freq.most_common(k)]

            for word, count in word_freq.items():
                if word in words_to_use:
                    # Determine the number of times the word appears
                    rows_to_add = min(count, k) if word_list else count
                    # Create DataFrame for the word occurrences
                    df = pd.DataFrame([{'file_name': file_name, 'word': word}] * rows_to_add)
                    # Append DataFrame to the list
                    rows_to_add_list.append(df)

        # Concatenate all the DataFrames in the list
        file_word_df = pd.concat(rows_to_add_list, ignore_index=True)
        sk.make_sankey(file_word_df, "size", "file_name", "word")

    # Source: https://amueller.github.io/word_cloud/generated/wordcloud.WordCloud.html
    # Source: https://stackoverflow.com/questions/16310015/what-does-this-mean-key-lambda-x-x1
    def wordcloud_subplots(self):
        """
        Generates an array of word clouds, each representing a single file's contents
        """
        num = len(self.files)
        # Finding factors of the number of files to determine subplot dimensions
        factors = [(i, num // i) for i in range(1, int(num ** 0.5) + 1) if num % i == 0]
        dim = min(factors, key=lambda x: abs(x[0] - x[1]))  # Selecting the dimensions with the minimum difference

        # Creating a figure with subplots based on the determined dimensions
        fig, axes = plt.subplots(dim[0], dim[1], figsize=(6, 3), dpi=200)
        fig.suptitle(f"Word Clouds for {len(self.files)} files")  # Title for the overall figure

        for ax, file_tuple in zip(axes.flatten(), self.files):
            file_name = file_tuple[0]
            file_info = self.results[file_name]
            word_freq = file_info["word_frequency"]

            # Generating word cloud from word frequency
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)

            # Adding word cloud to the respective subplot
            ax.imshow(wordcloud)
            ax.set_title(f"{file_name}", fontsize=9)
            ax.axis('off')

        plt.tight_layout()
        plt.show()

    def polar_subject_scatterplot(self):
        """
        Generates a scatter plot of subjectivity vs polarity for the input files using Plotly
        """
        file_polarities = []
        file_subjectivities = []
        file_names = []

        for file_tuple in self.files:
            # Getting the string name of the file
            file_name = file_tuple[0]
            # Getting all the info parsed from the file
            file_info = self.results[file_name]
            # Retrieving polarity and subjectivity scores
            polarity = file_info["avg_polarity"]
            subjectivity = file_info["avg_subjectivity"]
            # Updating lists of file polarities, subjectivities, and file names
            file_polarities.append(polarity)
            file_subjectivities.append(subjectivity)
            file_names.append(file_name)

        # Creating a pandas DataFrame
        data = pd.DataFrame({
            'Polarity Scores': file_polarities,
            'Subjectivity Scores': file_subjectivities,
            'File Names': file_names
        })

        # Creating the scatter plot using Plotly Express
        fig = px.scatter(data, x='Polarity Scores', y='Subjectivity Scores', text='File Names',
                         title='Subjectivity vs Polarity for Inputted Files')
        fig.update_traces(textposition='top center')

        # Customizing axis labels
        fig.update_layout(xaxis_title='Polarity Scores', yaxis_title='Subjectivity Scores')
        fig.show()







