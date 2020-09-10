
from diversity_analysis_tool.diversity import AssessDiversity
from diversity_analysis_tool.diversity import create_age_bands
from diversity_analysis_tool.diversity import transform_nhs_sex
from diversity_analysis_tool.diversity import transform_nhs_ethnicity
from diversity_analysis_tool.diversity import transform_nhs_race

import pandas as pd


def test_transform():
    test_df =  pd.DataFrame([{'person_id': 1, 'sex': 1, 'ethnicity': 'A', 'age': 34,
                              'is_deceased': True},
                             {'person_id': 2, 'sex': 2, 'ethnicity': 'M', 'age': 38,
                              'is_deceased': False},
                             {'person_id': 3, 'sex': 8, 'ethnicity': 'R', 'age': 42,
                              'is_deceased': True}])
    diversity_analyser = AssessDiversity(transform_nhs_ethnicity, transform_nhs_race, transform_nhs_sex)
    actual_results_df =  diversity_analyser.transform(test_df, 5, 'age', 'sex', 'ethnicity', None, None,
                                                      'is_deceased')

    expected_results_df =  pd.DataFrame([{'age_band': '(30, 35]', 'sex': 'Male', 'ethnicity': 'British',
                                          'is_deceased': True},
                                         {'age_band': '(35, 40]', 'sex': 'Female', 'ethnicity': 'Caribbean',
                                          'is_deceased': False},
                                         {'age_band': '(40, 45]', 'sex': 'Not specified', 'ethnicity': 'Chinese',
                                          'is_deceased': True}])
    check_data_sets_equal(actual_results_df, expected_results_df)


def test_transform_age_bands():
    # Works with an odd age banding
    test_df =  pd.DataFrame([{'person_id': 1, 'age': 5},
                             {'person_id': 2, 'age': 21},
                             {'person_id': 3, 'age': 90}])
    actual_results_df = create_age_bands(test_df, 'age', 0, 90, 5)
    expected_results_df =  pd.DataFrame([{'person_id': 1, 'age': 5, 'age_band': '(0, 5]'},
                                         {'person_id': 2, 'age': 21, 'age_band': '(20, 25]'},
                                         {'person_id': 3, 'age': 90, 'age_band': '(85, 90]'}])
    check_data_sets_equal(actual_results_df, expected_results_df)

    # Works with an even age banding
    actual_results_df = create_age_bands(test_df, 'age', 0, 90, 2)
    expected_results_df =  pd.DataFrame([{'person_id': 1, 'age': 5, 'age_band': '(4, 6]'},
                                         {'person_id': 2, 'age': 21, 'age_band': '(20, 22]'},
                                         {'person_id': 3, 'age': 90, 'age_band': '(88, 90]'}])
    check_data_sets_equal(actual_results_df, expected_results_df)

    # Works with a value that is greater than the age limits used to produce bands
    test_df =  pd.DataFrame([{'person_id': 1, 'age': 5},
                             {'person_id': 2, 'age': 21},
                             {'person_id': 3, 'age': 105}])
    actual_results_df = create_age_bands(test_df, 'age', 0, 90, 2)
    expected_results_df =  pd.DataFrame([{'person_id': 1, 'age': 5, 'age_band': '(4, 6]'},
                                         {'person_id': 2, 'age': 21, 'age_band': '(20, 22]'},
                                         {'person_id': 3, 'age': 105, 'age_band': '(90plus]'}])
    check_data_sets_equal(actual_results_df, expected_results_df)


def test_transform_nhs_sex():
    test_df =  pd.DataFrame([{'person_id': 1, 'sex': 1},
                             {'person_id': 2, 'sex': 2},
                             {'person_id': 3, 'sex': 8},
                             {'person_id': 4, 'sex': None},
                             {'person_id': 5, 'sex': float("nan")}])

    actual_results_df = transform_nhs_sex(test_df, 'sex')
    expected_results_df = pd.DataFrame([{'person_id': 1, 'sex': 'Male'},
                                        {'person_id': 2, 'sex': 'Female'},
                                        {'person_id': 3, 'sex': 'Not specified'},
                                        {'person_id': 4, 'sex': 'Unknown'},
                                        {'person_id': 5, 'sex': 'Unknown'}])
    check_data_sets_equal(actual_results_df, expected_results_df)


def test_transform_nhs_ethnicity():
    test_df =  pd.DataFrame([{'person_id': 1, 'ethnicity': 'K'},
                             {'person_id': 2, 'ethnicity': 'R'},
                             {'person_id': 3, 'ethnicity': 'Z'},
                             {'person_id': 4, 'ethnicity': None},
                             {'person_id': 5, 'ethnicity': float("nan")}])

    actual_results_df = transform_nhs_ethnicity(test_df, 'ethnicity')
    expected_results_df = pd.DataFrame([{'person_id': 1, 'ethnicity': 'Bangladeshi'},
                                        {'person_id': 2, 'ethnicity': 'Chinese'},
                                        {'person_id': 3, 'ethnicity': 'Not stated'},
                                        {'person_id': 4, 'ethnicity': 'Unknown'},
                                        {'person_id': 5, 'ethnicity': 'Unknown'}])
    check_data_sets_equal(actual_results_df, expected_results_df)


def test_transform_nhs_race():
    test_df =  pd.DataFrame([{'person_id': 1, 'race': 'A'},
                             {'person_id': 2, 'race': 'M'},
                             {'person_id': 3, 'race': 'S'},
                             {'person_id': 4, 'race': None},
                             {'person_id': 5, 'race': float("nan")}])
    actual_results_df = transform_nhs_race(test_df, 'race')
    expected_results_df = pd.DataFrame([{'person_id': 1, 'race': 'White'},
                                        {'person_id': 2, 'race': 'Black or Black British'},
                                        {'person_id': 3, 'race': 'Other Ethnic Groups'},
                                        {'person_id': 4, 'race': 'Unknown'},
                                        {'person_id': 5, 'race': 'Unknown'}])
    check_data_sets_equal(actual_results_df, expected_results_df)



def check_data_sets_equal(first_df, second_df) -> None:
    """
    Checks whether two data sets are equal.

    Args:
        column_names (list): column names that should appear in branch and master data sets
        first_df (dataframe): a data frame to be compared
        second_df (dataframe): the other data frame to be compared
    Raises:
        GeneralException if the two data frames are not considered equal.
    """
    tmp1_df = first_df.sort_values(list(first_df.columns.values)).reset_index(drop=True)
    tmp2_df = second_df.sort_values(list(first_df.columns.values)).reset_index(drop=True)
    pd.testing.assert_frame_equal(tmp1_df, tmp2_df, check_like=True, check_dtype=False)
