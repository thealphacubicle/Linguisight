"""
File: sankey.py
Description:  A simple library for building sankey diagrams from a dataframe
Author: Sriya Vuppala
Date: 10-3-2023
"""

import plotly.graph_objects as go
import pandas as pd


def stack_columns(df, cols):
    """
    Stacks multiple columns in a dataframe into just two columns
    :param df: a dataframe
    :param cols: a list of strings representing the columns to stack
    :return stacked: a dataframe with the columns stacked
    """
    # initializing an empty dataframe
    stacked = pd.DataFrame()

    # stacks two consecutive columns at a time
    for i in list(range(len(cols)-1)):
        mini_df = df[[cols[i], cols[i+1]]]
        # setting new column names
        mini_df.columns = ['src', 'targ']
        stacked = pd.concat([stacked, mini_df], axis=0)
    return stacked


def code_mapping(df, src, targ):
    """
    Maps each value in the dataframe to an integer value
    :param df: dataframe input
    :param src: a string representing the src column of a dataframe
    :param targ: a string representing the targ column of a dataframe
    :return: mapped_df: a dataframe whose values have been replaced with the mapping codings
            labels: a list of all the distinct values in the df
    """

    # get the distinct labels from src/targ columns
    labels = list(set(list(df[src]) + list(df[targ])))

    # generate n integers for n labels
    codes = list(range(len(labels)))

    # create a map from label to code
    lc_map = dict(zip(labels, codes))

    # substitute names for codes in the dataframe
    mapped_df = df.replace({src: lc_map, targ: lc_map})

    # Return modified dataframe and list of labels
    return mapped_df, labels


# https://www.statology.org/pandas-count-duplicates/
def aggregate_data(artists_df, *cols):
    """
           Aggregates data, counting the number of artists grouped by source and targ
           :param artists_df - the dataframe of the artists info
           :return: aggregate_df - an aggregated dataframe of artists grouped by source and targ
    """
    # counting duplicates for each unique row
    aggregate_df = artists_df.groupby(list(cols)).size().reset_index(name="size")
    return aggregate_df


def filter_data(aggregate_df, threshhold):
    """
        Filters the aggregated data
        :param threshhold: an int used as a threshold to filter some links
        :param aggregate_df - the dataframe of the aggregated artists info
        :return: clean_df - a dataframe of the newly filtered data
    """

    # dropping rows with missing values
    clean_df = aggregate_df.dropna()

    # dropping rows where the decade is 0
    clean_df = clean_df.loc[aggregate_df['src'] != 0]
    clean_df = clean_df.loc[aggregate_df['targ'] != 0]

    # dropping rows where the value of a link is below the given threshhold
    clean_df = clean_df.loc[clean_df['size'] > threshhold]

    return clean_df


def make_sankey(df, vals=None, *cols, **kwargs):
    """
    Create a sankey diagram from a dataframe and specified columns
    :param cols: a list of column names representing sources and targets
    :param df: a dataframe to be made into a sankey diagram
    :param vals: a string representing the column name of the link values
    :param kwargs: a key-worded argument list
    :return: nothing, but shows a sankey diagram visualization
    """
    if len(cols) < 2:
        print("Sorry! You need at least 2 column inputs.")
    else:

        # stack the columns into 1 dataframe with 2 columns
        stacked_df = stack_columns(df, cols)

        # aggregate the dataframe
        aggregated_df = aggregate_data(stacked_df, "src", "targ")

        # convert df labels to integer values
        mapped_df, labels = code_mapping(aggregated_df, "src", "targ")

        # filter the dataframe
        final_df = filter_data(mapped_df, 1)
        # setting the values for the sankey diagram
        if vals:
            values = final_df[vals]
        else:
            values = [1] * len(final_df)

        # establishing the links
        link = {'source': final_df['src'], 'target': final_df['targ'], 'value': values,
                'line': {'color': 'black', 'width': 1}}

        # setting node thickness
        node_thickness = kwargs.get("node_thickness", 50)

        # establishing node
        node = {'label': labels, 'pad': 50, 'thickness': node_thickness,
                'line': {'color': 'black', 'width': 1}}

        # making Sankey Diagram (finally!)
        sk = go.Sankey(link=link, node=node)
        fig = go.Figure(sk)
        fig.show()
