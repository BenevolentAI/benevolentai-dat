import os
import logging 

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class GraphUtility:
    # =============
    # Graph Methods
    # =============
    def __init__(self, df, output_directory_path):
        self.df = df
        self.output_directory_path = output_directory_path

    def build_graph(self):
        """this function collects columns with predifined column names and maps
        through a dictionary of graphing functions"""

        colname_dict = {
            'age_band': 'Age Band',
            'ethnicity': 'Ethnicity',
            'race': 'Race',
            'sex': 'Sex',
        }
        # Add missing colnames
        missing_cols = list(set(self.df.columns.values)-set(colname_dict.keys()))
        colname_dict.update({colname: colname for colname in  missing_cols})
        # Plot individual feature graphs
        for column_name in self.df.columns.values:
            self.generate_bar_graph(column_name, 'Number of patients', colname_dict[column_name])

        # Two variable graphs
        if set(['age_band', 'ethnicity']).issubset(self.df.columns.values):
            self.generate_stacked_bar_graph('age_band', 'ethnicity', 'Number of participants', colname_dict['age_band'], colname_dict['ethnicity'])
        if set(['age_band', 'race']).issubset(self.df.columns.values):
            self.generate_stacked_bar_graph('age_band', 'race',  'Number of participants', colname_dict['age_band'], colname_dict['race'])
        if set(['race', 'sex']).issubset(self.df.columns.values):
            self.generate_stacked_bar_graph('race', 'sex', 'Number of participants', colname_dict['race'], colname_dict['sex'])
        if set(['ethnicity', 'sex']).issubset(self.df.columns.values):
            self.generate_stacked_bar_graph('ethnicity', 'sex', 'Number of participants', colname_dict['ethnicity'], colname_dict['sex'])
        if set(['age_band', 'sex']).issubset(self.df.columns.values):
            self.generate_stacked_bar_graph('age_band', 'sex', 'Number of participants', colname_dict['age_band'], colname_dict['sex'])


    def generate_bar_graph(self, column_name, x_label = None, y_label= None):
        """
        The graph functions can be called on a df and returns a visualization bar chart for one variable
         Args:
            column_name: specifies the column that is shown as bar chart
            x_label (optional): label for x axis. If none no x-axis label is shown.
            y_label (optional): label for y axis. If none the major_category_column_name is used as label
        """
        sns.set(style='whitegrid', palette='colorblind', font='DejaVu Sans', font_scale=1,
                color_codes=True)

        g = sns.catplot(y=column_name, kind="count", data=self.df.sort_values(column_name, na_position='last', ascending=False), color="b")
        [plt.setp(ax.get_xticklabels(), rotation=-45) for ax in g.axes.flat]
        if x_label:
            plt.xlabel(x_label)
        if y_label:
            plt.ylabel(y_label)

        file_path = os.path.join(self.output_directory_path, f"{column_name}_bar_chart")
        g.savefig(file_path,bbox_inches='tight')
        logger.info(f"successfully saved {column_name} bar graph")


    def generate_stacked_bar_graph(self, major_category_column_name, minor_category_column_name, x_label = None, y_label= None, legend_title=None):
        """
        generates a stacked bar graph. Each graph will be labelled by a value in the
        major_category_column_name. Withiin each bar, the height will be divided based on counts of
        values in the minor_category_column_name
        Args:
            major_category_column_name: provides labels for each separate bar in the graph
            minor_category_column_name: used to divide each bar into sections for each minor category label
            x_label (optional): label for x axis. If none no x-axis label is shown.
            y_label (optional): label for y axis. If none the major_category_column_name is used as label
            legend_title (optional): title for legend. If none the minor_category_column_name is used as  title
        """
        sns.set(style='whitegrid', palette='colorblind', font='DejaVu Sans', font_scale=1,
                color_codes=True)

        stacked_bar_graph_df = self.df[[major_category_column_name, minor_category_column_name]]
        results_df = pd.crosstab(stacked_bar_graph_df[major_category_column_name],
                                 stacked_bar_graph_df[minor_category_column_name],
                                 margins=True)
        all_df = pd.DataFrame(results_df['All']).T.drop(columns='All')
        filtered = results_df.drop(labels='All').drop(columns=['All'])

        # plot stacked major/minor
        filename = f"{major_category_column_name}_{minor_category_column_name}_stacked_bar_chart"
        self._create_stacked_figure(filtered)
        if x_label:
            plt.xlabel(x_label)
        if y_label:
            plt.ylabel(y_label)
        if legend_title:
            plt.legend(title=legend_title, bbox_to_anchor=(1.05, 1), loc='upper left')
        file_path = os.path.join(self.output_directory_path, filename)
        plt.savefig(file_path, bbox_inches='tight')


        # plot only major
        filename = f"{major_category_column_name}_stacked_bar_chart"
        # removing index name so it doesn't appear as label 'all'
        all_df.index = ['']
        self._create_stacked_figure(all_df)
        if x_label:
            plt.xlabel(x_label)
        if y_label:
            plt.legend(title=y_label, bbox_to_anchor=(1.05, 1), loc='upper left')
        file_path = os.path.join(self.output_directory_path, filename)
        plt.savefig(file_path, bbox_inches='tight')

        logger.info(("successfully saved stacked bar graph for "
               f"{major_category_column_name} and {minor_category_column_name}"))


    def _create_stacked_figure(self, frames):
        fig = frames.plot(kind='barh', stacked=True,edgecolor = "none")
        plt.legend(title=frames.columns.name)
        plt.gcf().subplots_adjust(bottom=0.30)
        return fig