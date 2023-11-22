"""
main.py: Main file
"""

from pipeline import Pipeline
from framework import NLPAnalyzer
from load import Load
from process import Process
from analyze import Analyze

# Create basic pipeline
parser = Pipeline([
    ("input", Load(file_type="csv")),
    ("capitalization", Process(process_type="capitalization")),
    ("punctuation", Process(process_type="punctuation")),
    ("stop_words", Process(process_type="stop_words")),
    ("lemmatize", Process(process_type="lemmatize")),
    ("word_count", Analyze(analyze_type="word_count")),
    ("word_frequency", Analyze(analyze_type="word_frequency")),
    ("polarity_score", Analyze(analyze_type="polarity_score")),
    ("subjectivity_score", Analyze(analyze_type="subjectivity_score")),
])

# Instantiate the NLPAnalyzer
nlp_analyzer = NLPAnalyzer(
    files=[("Taylor Swift", "https://raw.github.khoury.northeastern.edu/ramansr04/Linguisight/main/data/01-taylor_swift.csv?token=GHSAT0AAAAAAAAARHA24N2SJYBZCAHRD26IZLGUWSQ"),
           ("Fearless (Taylor's Version)", "https://raw.github.khoury.northeastern.edu/ramansr04/Linguisight/main/data/02-fearless_taylors_version.csv?token=GHSAT0AAAAAAAAARHA3NQSMTZW2B6UTAMKUZLGUXHQ"),
           ("Speak Now", "https://raw.github.khoury.northeastern.edu/ramansr04/Linguisight/main/data/03-speak_now_deluxe_package.csv?token=GHSAT0AAAAAAAAARHA3QR57CLCCDHYYQEDEZLGUXUA"),
           ("Red", "https://raw.github.khoury.northeastern.edu/ramansr04/Linguisight/main/data/04-red_deluxe_edition.csv?token=GHSAT0AAAAAAAAARHA2CEVEGZ6G2MU62JMGZLGUYBQ"),
           ("1989", "https://raw.github.khoury.northeastern.edu/ramansr04/Linguisight/main/data/05-1989_deluxe.csv?token=GHSAT0AAAAAAAAARHA3IPUCPR2JY4LHA236ZLGUYOA"),
           ("Reputation", "https://raw.github.khoury.northeastern.edu/ramansr04/Linguisight/main/data/06-reputation.csv?token=GHSAT0AAAAAAAAARHA2FFWWTRLAKK4NQPAOZLGUYWQ"),
           ("Lover", "https://raw.github.khoury.northeastern.edu/ramansr04/Linguisight/main/data/07-lover.csv?token=GHSAT0AAAAAAAAARHA2HGG4SCQ6KZ5EVHSMZLGUZBQ"),
           ("Folklore", "https://raw.github.khoury.northeastern.edu/ramansr04/Linguisight/main/data/08-folklore_deluxe_version.csv?token=GHSAT0AAAAAAAAARHA34B267UECT4PZPITOZLGUZLQ"),
           ("Evermore", "https://raw.github.khoury.northeastern.edu/ramansr04/Linguisight/main/data/09-evermore_deluxe_version.csv?token=GHSAT0AAAAAAAAARHA3T3BXLPCQDMHMEDDMZLGUZVQ")],
    csv_target_text_col="lyric", parser=parser)

# Run the analyzer
nlp_analyzer.analyze()

# Creating visualization 1: Word Count Sankey Diagram
nlp_analyzer.wordcount_sankey(word_list=["love", "hate", "crime", "friend"])

# Creating visualization 2: Subplots of Word clouds
nlp_analyzer.wordcloud_subplots()

# Creating visualization 3: Subjectivity vs. Polarity Scatter plot
nlp_analyzer.polar_subject_scatterplot()

