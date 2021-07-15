from diversity_analysis_tool.diversity import AssessDiversity
from diversity_analysis_tool.diversity import transform_nhs_ethnicity
from diversity_analysis_tool.diversity import transform_nhs_race
from diversity_analysis_tool.diversity import transform_nhs_sex
from diversity_analysis_tool.diversity import transform_ses_order

import pandas as pd

if __name__ == "__main__":
    example_demographic_data_df = pd.DataFrame(
        [
            {
                "person_id": 1,
                "sex": 1,
                "ethnicity": "A",
                "race": "A",
                "age": 34,
                "is_deceased": True,
            },
            {
                "person_id": 2,
                "sex": 1,
                "ethnicity": "M",
                "race": "M",
                "age": 38,
                "is_deceased": False,
            },
            {
                "person_id": 3,
                "sex": 2,
                "ethnicity": "M",
                "race": "M",
                "age": 38,
                "is_deceased": False,
            },
            {
                "person_id": 4,
                "sex": 1,
                "ethnicity": "M",
                "race": "M",
                "age": 38,
                "is_deceased": False,
            },
            {
                "person_id": 5,
                "sex": 2,
                "ethnicity": "M",
                "race": "M",
                "age": 38,
                "is_deceased": False,
            },
            {
                "person_id": 6,
                "sex": 2,
                "ethnicity": "M",
                "race": "M",
                "age": 38,
                "is_deceased": False,
            },
            {
                "person_id": 7,
                "sex": 2,
                "ethnicity": "K",
                "race": "K",
                "age": 78,
                "is_deceased": False,
            },
            {
                "person_id": 8,
                "sex": 2,
                "ethnicity": "K",
                "race": "K",
                "age": 102,
                "is_deceased": False,
            },
            {
                "person_id": 9,
                "sex": 2,
                "ethnicity": "K",
                "race": "K",
                "age": 103,
                "is_deceased": False,
            },
            {
                "person_id": 10,
                "sex": 2,
                "ethnicity": "K",
                "race": "K",
                "age": 15,
                "is_deceased": False,
            },
            {
                "person_id": 11,
                "sex": 2,
                "ethnicity": "K",
                "race": "K",
                "age": 15,
                "is_deceased": False,
            },
            {
                "person_id": 12,
                "sex": 2,
                "ethnicity": "K",
                "race": "K",
                "age": 15,
                "is_deceased": False,
            },
            {
                "person_id": 13,
                "sex": 2,
                "ethnicity": "K",
                "race": "K",
                "age": 15,
                "is_deceased": False,
            },
            {
                "person_id": 14,
                "sex": 8,
                "ethnicity": "R",
                "race": "R",
                "age": 42,
                "is_deceased": True,
            },
        ]
    )

    output_directory_path = "output/"

    assess_diversity = AssessDiversity(
        transform_nhs_ethnicity,
        transform_nhs_race,
        transform_nhs_sex,
        transform_ses_order,
    )
    assess_diversity.create_diversity_analysis_report(
        example_demographic_data_df,
        5,
        "age",
        "sex",
        "ethnicity",
        "race",
        None,
        "is_deceased",
        output_directory_path,
    )
