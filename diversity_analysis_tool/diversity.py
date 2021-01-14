import os
import logging

import pandas as pd
import numpy as np

from diversity_analysis_tool.graph_construction import GraphUtility
from diversity_analysis_tool.nhs_codes import NHS_ETHNICITY_CODE_DICT, NHS_RACE_CODE_DICT

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class AssessDiversity:
    """
    This class cleans demographic data and puts it into a form that can support further programmatic analysis
    and rendering of graphical visualisations.  It delegates most of its activities to functions which can be
    substituted based on the nature of demographic data you are providing it.

    It assumes the input data frame has the following optional columns:
    age, sex, ethnicity, race, ses, is_deceased.
    """

    def __init__(self, preferred_ethnicity_transformation, preferred_race_transformation,
                 preferred_sex_transformation, preferred_ses_transformation):

        # By default, this class assumes it is processing data coming from an NHS hospital.  It could be adapted
        # to support data sets from other countries (eg: USA) by developing other methods that recognised different
        # kinds of codings for sex, ethnicity, race and socio economic status
        self.transform_ethnicity_routine = preferred_ethnicity_transformation
        self.transform_race_routine = preferred_race_transformation
        self.transform_sex_routine = preferred_sex_transformation
        self.transform_ses_routine = preferred_ses_transformation

        # The class will create results which contain age bands. These can help support more useful demographic
        # reporting and can also help minimise re-identifiability of demographic data.
        self.age_lower_limit = 0
        self.age_upper_limit = 90

    def transform(self, original_df, years_per_age_band, age_column_name, sex_column_name, ethnicity_column_name,
                  race_column_name, ses_column_name, is_deceased_column_name):
        """
        Transform demographic dataframe

        Args:
            original_df: demographic data frame
            years_per_age_band: number of years interval covered in an age band eg 5 would produce age bands like (0,5], (5, 10]...
            age_column_name: column name in the input demographic data frame that describes age. (eg: 'age')
            sex_column_name: column name in the input demographic data frame that describes sex. (eg: 'sex')
            ethnicity_column_name: column name in the input demographic data frame that describes ethnicity. (eg: 'ethnicity')
            race_column_name: column name in the input demographic data frame that describes race. (eg: 'race')
            ses_column_name: column name in the input demographic data frame that describes ses. (eg: 'ses')
            is_deceased_column_name: column name in the input demographic data frame that describes is deceased. (eg: 'is_deceased')
        """
        df = original_df.copy()
        df = create_age_bands(df, age_column_name, self.age_lower_limit, self.age_upper_limit, years_per_age_band)
        if self.transform_sex_routine:
            df = self.transform_sex_routine(df, sex_column_name)
        if self.transform_ethnicity_routine:
            df = self.transform_ethnicity_routine(df, ethnicity_column_name)
        if self.transform_race_routine:
            df = self.transform_race_routine(df, race_column_name)
        if self.transform_ses_routine:
            df = self.transform_ses_routine(df, ses_column_name)

        # Masks the first list with the second list.
        # keeping ses_column_name as socio-economic status can be measured in different ways

        colname_dict = {
            'age_band': age_column_name,
            'sex': sex_column_name,
            'ethnicity': ethnicity_column_name,
            'race': race_column_name,
            'is_deceased': is_deceased_column_name,
            ses_column_name: ses_column_name
        }
        all_columns_list = [k for k, v in colname_dict.items() if v in df.columns.values]
        df = df[all_columns_list]
        df = df.sort_values(by=all_columns_list[0])
        return df

    def create_diversity_analysis_report(self, original_df, years_per_band, age_column_name, sex_column_name,
                                         ethnicity_column_name, race_column_name, ses_column_name,
                                         is_deceased_column_name, output_directory_path):
        """
        The main routine to call from your own analysis for diversity.
        Args:
            df: demographic data frame
            years_per_band: number of years per age band
            age_column_name: column name that describes age
            sex_column_name: column name that describes sex
            ethnicity_column_name: column name that describes ethnicity
            race_column_name: column name that describes race
            ses_column_name: column name that describes ses
            is_deceased_column_name: column name that describes if a person is deceased or not
            output_directory_path: directory where all the CSV and results will be stored.
        """
        df = original_df.copy()
        cleaned_results_df = self.transform(df, years_per_band, age_column_name, sex_column_name,
                                            ethnicity_column_name, race_column_name, ses_column_name,
                                            is_deceased_column_name)

        if not os.path.exists(output_directory_path):
            os.makedirs(output_directory_path)

        # Write results out to a file
        csv_output_file_path = os.path.join(output_directory_path, 'diversity_analysis_report.csv')
        cleaned_results_df.to_csv(
            csv_output_file_path,
            sep="|",
            encoding="utf-8",
            index=False,
        )

        # Write out graphs. Change the boolean field from True False to make it easier to read in visual
        # presentations
        if 'is_deceased' in cleaned_results_df:
            cleaned_results_df['is_deceased'] = cleaned_results_df['is_deceased'].astype(str)
            cleaned_results_df['is_deceased'] = cleaned_results_df['is_deceased'].replace(
                {'True': 'Yes', 'False': 'No'}, regex=False)

        grapher = GraphUtility(cleaned_results_df, output_directory_path)
        grapher.build_graph()


# ==========================
# Age Transformation Methods
# ==========================
def create_age_bands(original_df, age_field_name, start_age=0, end_age=90, years_per_band=5):
    """
    Creates a new column which has an age band corresponding to the 'age' field in the input data. Age bands
    are created using a years_per_band, which is usually five. The age bands will look something like this:
    (0, 5], (5, 10], (10, 15].... Values which are above the age band range will have a form '[end_age]plus'
    eg: 90plus.

    Generally a maximum category like '90plus' is used to reduce the identifiability of very old people.
    Args:
        original_df: original demographic data frame
        age_field_name: tha name of the age field in the input data (eg: 'age')
        start_age: minimum age in the age bands, almost always going to be zero
        end_age: the maximum upper limit for an age
        years_per_band: the interval in an age band
    Returns: a data frame with a new column called 'age_band'
    """
    df = original_df.copy()

    banded_field_name = "age_band"

    bin_buckets = [item for item in range(start_age, end_age + 1, years_per_band)]
    bin_buckets.append(999)
    lbs = ['(%d, %d]' % (bin_buckets[i], bin_buckets[i + 1]) for i in range(len(bin_buckets) - 1)]

    df[banded_field_name] = pd.cut(x=df[age_field_name], bins=bin_buckets, labels=lbs, include_lowest=True).astype(str)
    df[banded_field_name] = df[banded_field_name].str.strip()

    current_last_band_name = f"({end_age}, 999]"
    last_band_name = f"({end_age}plus]"

    df[banded_field_name] = df[banded_field_name].replace(
        current_last_band_name, last_band_name, regex=False
    )

    df[banded_field_name] = df[banded_field_name].astype(str)
    df[banded_field_name] = df[banded_field_name].apply(lambda x: str(x[x.find("(") + 1:x.find("]")]))
    df[banded_field_name] = df[banded_field_name].apply(lambda x: x.replace(',', ' -'))

    return df


# =====================================
# Sex Transformation Methods
# =====================================
def transform_nhs_sex(original_df, sex_column_name):
    """
    Transforms numeric codes into words based on 'Sex of Patients', an NHS concept that means: 'The sex of
    PATIENTS intended to use a WARD indicated in the WARD OPERATIONAL PLANS, with the addition of Home Leave.'
    The definition is here:
    https://www.datadictionary.nhs.uk/data_dictionary/attributes/s/ses/sex_of_patients_de.asp?shownav=1
    Args:
        original_df:  original demographic data frame
        sex_column_name: the name of the column in the input data describing sex (eg: 'sex')
    Returns: a data frame where the sex column has words instead of numeric codes
    """
    if not sex_column_name in original_df:
        logger.info("No sex field is present")
        return original_df

    df = original_df.copy()

    df[sex_column_name] = df[sex_column_name].astype('Int64')
    df[sex_column_name] = df[sex_column_name].astype(str)
    replace_dict = {
        pd.NA: -999,
        '1': 'Male',
        '2': 'Female',
        '8': 'Not specified',
        '9': 'Home Leave',
        '-999': 'Unknown',
    }
    df[sex_column_name] = df[sex_column_name].replace(replace_dict, regex=False)
    return df


def transform_desktop_application_database_sex(original_df, sex_column_name):
    """
    This is an example based on a hospital database application that has its own bespoke coding
    for sex. Think about how you would handle empty values and make sense of whether 'Not specified'
    is the equivalent to 'Unknown'. Also, what value should be assigned if the code is some form of
    empty (eg: None)?
    Args:
        original_df: original demographic data frame
        sex_column_name: column name that describes age
    Returns: Transformed demographic data frame with replaced sex column
    """
    if not sex_column_name in original_df:
        logger.info("No sex field is present")
        return original_df

    df = original_df.copy()
    df[sex_column_name] = df[sex_column_name].astype('Int64')
    df[sex_column_name] = df[sex_column_name].replace(np.nan, 'Unknown', regex=True)
    df[sex_column_name] = df[sex_column_name].astype(str)
    replace_dict = {
        '0': 'Male',
        '1': 'Female',
        '2': 'Unknown',
    }
    df[sex_column_name] = df[sex_column_name].replace(replace_dict, regex=False)
    return df


# ================================
# Ethnicity Transformation Methods
# ================================

def transform_nhs_ethnicity(df, ethnicity_column_name):
    """
    Substitutes NHS ethnicity codes with full word form (eg: 'R' maps to 'Chinese'
    Args:
        df: demographic data frame
        ethnicity_column_name: the name of the column in the input data that describes ethnicity
    Returns: Dataframe with updated ethnicity column

    """
    df1 = df[ethnicity_column_name].replace(np.nan, '', regex=True)
    df1[ethnicity_column_name].fillna('Unknown', inplace=True)
    df1[ethnicity_column_name] = df1[ethnicity_column_name].apply(lambda x: NHS_ETHNICITY_CODE_DICT[x])
    return df1


# ===========================
# Race Transformation Methods
# ===========================

def transform_nhs_race(df, race_column_name):
    """
    More precisely these are ethnic groupings but they are often used to speak of racial groups
    Args:
        df: demographic data
        race_column_name: the column name in the demographic data that describes race
    Returns: Dataframe with updated race column
    """
    if not race_column_name:
        print("There is no race column")
        return df

    df[race_column_name].fillna('Unknown', inplace=True)
    df[race_column_name] = df[race_column_name].apply(lambda x: NHS_RACE_CODE_DICT[x])
    return df


def transform_ses_order(df, ses_column_name):
    """
    Orders the ses_column_name level by ses_level if given in data frame
    Args:
        df: demographic data
        ses_column_name: the column name in the demographic data that describes socio-economic status
    Returns: Dataframe sorted by ses level.
    """
    if 'ses_level' not in df.columns.values:
        return df

    # ordering the levels by ses_level:
    level_order = sorted(set(zip(df.ses_level, df[ses_column_name])))
    level_order = [lev[1] for lev in level_order]
    df[ses_column_name] = df[ses_column_name].astype('category')
    df[ses_column_name].cat.reorder_categories(level_order, inplace=True)

    return df
