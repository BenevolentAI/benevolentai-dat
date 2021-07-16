import pandas as pd
import numpy as np

# Converted raw IPUMS data set in .csv to cleaned dataframe
# Cleaned dataframe is an example input to diversity_analysis_tool
def rename_by_code(df):
    # Sex
    df.loc[(df.SEX == 1), "SEX"] = "Male"
    df.loc[(df.SEX == 2), "SEX"] = "Female"

    # Race
    df.loc[(df.RACE == 1), "RACE"] = "White"
    df.loc[(df.RACE == 2), "RACE"] = "Black/African American/Negro"
    df.loc[(df.RACE == 3), "RACE"] = "American Indian or Alaska Native"
    df.loc[(df.RACE == 4), "RACE"] = "Chinese"
    df.loc[(df.RACE == 5), "RACE"] = "Japanese"
    df.loc[(df.RACE == 6), "RACE"] = "Other Asian or Pacific Islander"
    df.loc[(df.RACE == 7), "RACE"] = "Other race, nec"
    df.loc[(df.RACE == 8), "RACE"] = "Two major races"
    df.loc[(df.RACE == 9), "RACE"] = "Three or more major races"

    # Keeping the level for ordering in plots
    df["SES_LEVEL"] = df.EDUC

    # Education
    df.loc[(df.EDUC == 0), "EDUC"] = "N/A or no schooling"
    df.loc[(df.EDUC == 1), "EDUC"] = "Nursery school to grade 4"
    df.loc[(df.EDUC == 2), "EDUC"] = "Grade 5, 6, 7, or 8"
    df.loc[(df.EDUC == 3), "EDUC"] = "Grade 9"
    df.loc[(df.EDUC == 4), "EDUC"] = "Grade 10"
    df.loc[(df.EDUC == 5), "EDUC"] = "Grade 11"
    df.loc[(df.EDUC == 6), "EDUC"] = "Grade 12"
    df.loc[(df.EDUC == 7), "EDUC"] = "1 year of college"
    df.loc[(df.EDUC == 8), "EDUC"] = "2 years of college"
    df.loc[(df.EDUC == 9), "EDUC"] = "3 years of college"
    df.loc[(df.EDUC == 10), "EDUC"] = "4 years of college"
    df.loc[(df.EDUC == 11), "EDUC"] = "5+ years of college"

    return df


def clean_ipums(filename, outputfile, save_to_file=True):
    df = pd.read_csv(filename)

    # ses: either inctot or educ could represent socioeconomic status
    subset_cols = ["YEAR", "SEX", "AGE", "RACE", "EDUC"]
    df = df[subset_cols]
    df = rename_by_code(df)
    # lower case columm names
    df.columns = map(str.lower, df.columns)

    if save_to_file:
        df.to_csv(outputfile, index=False)


if __name__ == "__main__":
    ipums_filename = "../input/usa_00004.csv"
    outfilename = "../input/ipums_test_cleaned.csv"
    clean_ipums(ipums_filename, outfilename, save_to_file=True)
