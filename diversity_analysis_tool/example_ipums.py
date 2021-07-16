import logging

from diversity_analysis_tool.diversity import AssessDiversity
from diversity_analysis_tool.diversity import GraphUtility

import pandas as pd

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def identity_transform(df, column_name):
    return df


if __name__ == "__main__":
    example_ipums_demographic_data_df = pd.read_csv("input/ipums_test_cleaned.csv")

    logger.info(f"DataFrame head {example_ipums_demographic_data_df.head()}")
    logger.info(f"Shape of the DataFrame {example_ipums_demographic_data_df.shape}")

    output_directory_path = "output/"

    assess_diversity = AssessDiversity(
        identity_transform, identity_transform, identity_transform, identity_transform
    )
    assess_diversity.create_diversity_analysis_report(
        example_ipums_demographic_data_df,
        10,
        "age",
        "sex",
        None,
        "race",
        None,
        None,
        output_directory_path,
    )
    grapher = GraphUtility(example_ipums_demographic_data_df, output_directory_path)
    grapher.build_graph()
