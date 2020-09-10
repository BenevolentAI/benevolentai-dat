import argparse
import logging
import os
import pandas as pd
from diversity_analysis_tool.diversity import AssessDiversity

logger = logging.getLogger("diversity_analysis_tool.main")
logger.setLevel(logging.INFO)


def main():
    """
    Command line entry point for assessing diversity in data
    """
    parser = argparse.ArgumentParser(description="assess the diversity of your data")
    parser.add_argument("input_data", type=str, help="Path to the csv file containing the data you want to assess.")
    parser.add_argument("output_dir", type=str, help="Path to a directory where results will stored.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase logging verbosity.")
    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    if not os.path.isfile(args.input_data):
        logger.error(f"{args.input_data} is not a valid path to a file")
        exit(1)
    if not os.path.isdir(args.output_dir):
        logger.error(f"{args.output_dir} does not exist, creating directory")


    data_df = pd.read_csv(args.input_data)
    logger.debug("Converted data to pandas data frame. Creating AssessDiversity instance")
    assess_diversity = AssessDiversity(None, None, None)
    assess_diversity.create_diversity_analysis_report(data_df, 5, 'age', 'sex', 'ethnicity',
                                                      'race', None, 'educ', 'is_deceased', args.output_dir)
    logger.info("Assessment complete. See {} for results".format(args.output_dir))
