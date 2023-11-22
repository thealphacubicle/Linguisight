"""
pipeline.py: Defines parsers built for the NLP framework as a pipeline <br><br>
"""
__author__ = "Srihari Raman, Reema Sharma, Sriya Vuppala"

# Imports
# from graphviz import Digraph

class Pipeline:
    """
    Class implementation of the PipelineParser <br><br>
    This class is used to construct a parser pipeline for the NLP framework <br><br>
    """
    def __init__(self, steps):
        """
        Constructor to take in a list of steps <br><br>
        @param steps: List of steps to be used in the pipeline (can take Input, Process, or Output functions)
        """
        self.steps = steps
        self.results = {}

    # TODO: To be implemented
    def execute(self, file_name, file_path, **kwargs):
        """
        Executes each step in the pipeline
        @param file: File to be processed
        @return: Results from processing the file
        """
        kwargs = {key: value for key, value in kwargs['kwargs'].items() if value is not None}
        kwargs['filepath'] = file_path

        # Create a new result_dict for each file
        result_dict = {}

        for process_name, func in self.steps:
            result_dict = func.run(result_dict=result_dict, file_name=file_name, kwargs=kwargs)

        return result_dict

    def add_to_pipeline(self, step):
        """
        Adds a step to the pipeline
        @param step: Step to be added to the pipeline
        @return: None
        """
        self.steps.append(step)


    def visualize_pipeline(self, steps):
        """
        Visualizes the pipeline of steps <br><br>
        @param steps: Steps to be visualized
        @return: None
        """
        dot = Digraph()

        for i, step in enumerate(steps):
            dot.node(str(i), label=step)

            if i > 0:
                dot.edge(str(i - 1), str(i))

        # Render the graph
        dot.render('pipeline', view=True)