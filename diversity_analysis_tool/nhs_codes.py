# This is a lookup table of NHS ethnicity codes defined here:
# https://www.datadictionary.nhs.uk/data_dictionary/attributes/e/end/ethnic_category_code_de.asp
NHS_ETHNICITY_CODE_DICT = dict(
    A="British",
    B="Irish",
    C="Any other White background",
    D="White and Black Caribbean",
    E="White and Black African",
    F="White and Asian",
    G="Any other mixed background",
    H="Indian",
    J="Pakistani",
    K="Bangladeshi",
    L="Any other Asian background",
    M="Caribbean",
    N="African",
    P="Any other Black background",
    R="Chinese",
    S="Any other ethnic group",
    Z="Not stated",
    Unknown="Unknown",
)

# These are not strictly 'race' categories, but the generic headings under which NHS ethnicity codes are
# organised. As you can see, these categories aren't much use from a biological perspective.
NHS_RACE_CODE_DICT = dict(
    A="White",
    B="White",
    C="White",
    D="Mixed",
    E="Mixed",
    F="Mixed",
    G="Mixed",
    H="Asian or Asian British",
    J="Asian or Asian British",
    K="Asian or Asian British",
    L="Asian or Asian British",
    M="Black or Black British",
    N="Black or Black British",
    P="Black or Black British",
    R="Other Ethnic Groups",
    S="Other Ethnic Groups",
    Z="Not stated",
    Unknown="Unknown",
)
