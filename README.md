# Diversity Analysis Tool

Characterizing diversity in biodata and producing visualizations


## Usage

#### As a command line tool.

pip install the package. `pip install diversity-analysis-tool`. This is will expose all the command line entry points available.

E.g. to assess the diversity of a your data, use the `assess_diversity` command.
```bash
$ assess_diversity --help
usage: assess_diversity [-h] [-v] input_data output_dir

assess the diversity of your data

positional arguments:
  input_data     Path to the csv file containing the data you want to assess.
  output_dir     Path to a directory where results will stored.

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Increase logging verbosity.

```


To run the tool on the example data run the following command
```bash
$ assess_diversity input/ipums_test_cleaned.csv output
```

#### Development guide

The package is pip installable. During development, you can install it in editable mode `pip install -e <path-to-package>`.
The package will be hot reloaded as you make changes so you do not need to reinstall the package to test it.

<br>

## Documentation of Demographic Variables
[[_TOC_]]

### Age

#### Why it is important in precision medicine
The most significant risk factor for developing dementia is age [1](https://www.dementiastatistics.org/statistics/prevalence-by-age-in-the-uk/https://www.dementiastatistics.org/statistics/prevalence-by-age-in-the-uk/). Aging is also the dominant risk factor in developing clinically significant atherosclerotic lesion formation [2](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5735066/pdf/fgene-08-00216.pdf).  Heart failure is common in the older population and increases progressively with advancing age [3](https://www.ageuk.org.uk/Documents/EN-GB/For-professionals/Research/Age_UK_almanac_FINAL_9Oct15.pdf?dtrk=true). 

Age can also be an issue for the young. Asthma is more common in children than adults [4](https://www.aafa.org/asthma-facts/). Acute tonsillitis is most common in children [5](https://www.mayoclinic.org/diseases-conditions/tonsillitis/symptoms-causes/syc-20378479). About 60% of all babies have jaundice [6](https://www.cdc.gov/ncbddd/jaundice/facts.html).

For many precision medicine analyses, age isn't one field, it's many: age of symptom onset, age at diagnosis, age at certain treatment dates and age of death. Sometimes age in years is sufficient, whereas for others, intervals between events measured in days is more appropriate.

#### Data processing issues
Be aware how dates may be blurred. Health data providers may want to withhold or generalise fields such as birth dates because they may feel it presents significant risk that pseudonymised patient records could be re-identified. They may remove precision by reporting year and month only, or they may impute a day based on some formula. It is important to note the details of how dates were reported, especially across data sources that were made by different organisations.

Prefer using intervals over dates as early as possible in data processing. One way to mitigate concerns of re-identifiability is to work with time intervals rather than specific dates and times as early as possible in data processing. A birth date of October 12, 1954 could always be used to help identify patients in unrelated data sets, but 55 as an 'age of symptom onset' is a less identifiable variable.

Be aware of inaccurate death data. Some of your age calculations may relate to 'age at death', or they may assume a patient is alive when they are not. In some parts of the world, hospitals may record that a patient received a treatment but only record death if it occurs on their premises. If the patient later died at home or died at another hospital, the health records may not accurately indicate if and when someone passed away.  You may need to link patient records from a health provider with data from patient death registries.

Age bands are often used to make data less identifiable. Health data providers may choose to make each patient record have an age band instead of a specific age (eg: 30-34 instead of 32). If you are harmonising multiple patient data sources, you may need to consider how to reconcile between different band intervals or with exact ages.

Check the date format used in your data sets. It's a good idea to convert all dates to a single canonical format so you can apply the same data calculations across all your data sources. For example, 07/06/2008 can be June 7, 2008 in a British health data set or July 6, 2008 in a US data set. 

----------
### Sex and Gender

#### Meanings
Sex refers to biological characteristics, whereas gender is based on socially constructed features. Both variables are most accurately characterised as a spectrum of values, but most often they are treated in data collection as Male or Female. Sex and gender are often wrongfully thought to be interchangeable concepts and this can be reflected when reporting health data.

The spectrum for sex covers male, female and Disorders of Sexual Development (DSD), which are a collection of congenital conditions associated with atypical development of internal and external genital structures [7](https://tinyurl.com/y3sydo74). At a genetic level, sex is not just a matter of XX for female and XY for male. The range is better described as 'a range of chromosome complements, hormone balances, and phenotypic variations that determine sex' [8](https://www.who.int/genomics/gender/en/)

Gender identity is also a spectrum with more than 60 terms associated with it [9](https://www.healthline.com/health/different-genders).

#### Why they are important in precision medicine
There is ample evidence that common demographic factors can be highly correlated with various diseases. For example, sex and gender can be important factors. Women have a higher incidence and prevalence of autoimmune diseases than men, and 85% or more patients of multiple autoimmune diseases are female [10](https://www.frontiersin.org/articles/10.3389/fendo.2019.00265/full). Clinical observation shows that men and women are different in prevalence, symptoms, and responses to treatment of several psychiatric disorders, including schizophrenia [11](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5688947/). Transgender women are 49% more likely to be living with HIV than other adults of reproductive age [12](https://www.who.int/hiv/topics/transgender/en/).

Sex and gender tend to be reported as binary variables in health. The variety of other values those variables can assume is often lost in reporting.


#### Data processing issues

##### Harmonisation of Coding Schemes
The main challenge of processings sex and gender is standardising values across data sets that have been coded with different data dictionary. You may have to do several semantic mapping activities which address both the names and coding values of variables you believe describe sex. This table illustrates the variety of slightly different codings amongst different types of health data sets:


|   | [Phenotypic sex classification (NHS Data Dictionary)](https://tinyurl.com/y3v6yymg) | [CDC Coronavirus Report](https://www.cdc.gov/coronavirus/2019-ncov/downloads/data-dictionary.pdf) | [ISD Scotland Data Dictionary](https://www.ndc.scot.nhs.uk/Dictionary-A-Z/Definitions/index.asp?Search=S&ID=1277&Title=Sex) | [US Health Information Knowledge Base Sex/Gender Hl7](https://ushik.ahrq.gov/ViewItemDetails?system=mdr&itemKey=74266000)|
|:----|:---:|:---:|:---:|:---:|
| **Male** | 1   | 1   | 1   | 1 | M |
| **Female** | 2 | 2 | 2 | 2 | F |
| **Other** | -   | 3 | - | - | O |
| **Indeterminate** | 9 | - | - | - | - |
| **Unknown** | X   | 9 | - | - | U |
| **Ambiguous** | - | - | - | - | A |
| **Not Known** | - | - | - | 0 | - |
| **Not** | - | - | 8 | 9 | - |


##### Here are some questions to keep in mind
* Are variables capturing sex really describing gender? 
* Is there a default value? This can help you tell the difference between a value which may have been pre-populated on an electronic form and one where someone had to make an active decision
* Is the value sex assigned at birth or currently assigned sex?
* Was the sex value self-reported by a patient or assigned by a medical professional? Check whether the variable indicates whether the patient stated their sex or not
* Be aware of the compatibility of meanings of missing value (eg: not applicable, not specified, not known, unknown). Unknown and not known are equivalent but not specified may indicate a patient's intent not to provide information.
* Be aware of the semantic equivalence of miscellaneous coding values (eg: other, indeterminate, ambiguous)
* What was the original data type of variables stored in the system? Some databases store sex as a binary data type that can only record a value as a "0" or a "1". Other systems may use an integer data type for a variable that may have "1" or a "2"

* Look for other information in your data set  to support better diversity
  * Look for ICD 10 codes F64.* for "Gender identity disorders"
  * Examine [Whitchel's](https://tinyurl.com/y3sydo74) paper about Disorders of Sex for a classification of disorders


### Ethnicity and Race

#### Meanings
The concept of race and ethnicity are problematic in precision medicine because they are largely social constructs that don't map well to biological characteristics. Race has only ever alluded to a small number of morphological phenotypes, most of which are not relevant to molecular aspects of disease mechanisms. Ethnicity denotes groups that share a common identity-based ancestry, language or culture [13](https://genderedinnovations.stanford.edu/terms/race.html).

#### Why they are important in precision medicine
Ethnicity and race can be a strong risk factor in disease response. The prevalence of coronary heart disease amongst the South Asian population in the UK is higher compared to the general population [14](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6394505/). Type 2 diabetes is more prevalent in Asian and Black populations than it is in white populations [15](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6948201/). The overall mortality rate for sarcoidosis has been shown to be eight times higher in African Americans than in Caucasians [16](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4314818/pdf/chest_147_2_438.pdf). More recently, it is becoming clear that COVID mortality rates for some ethnic groups are much higher than for White people [17](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/deaths/articles/coronavirusrelateddeathsbyethnicgroupenglandandwales/2march2020to10april2020).

The most important biological concept related to ancestry are haplotypes, which are sets of DNA variations that tend to be inherited together. They can either be a combination of alleles or single nucleotide polymorphisms (SNPs) found on the same chromosome [18](https://www.genome.gov/genetics-glossary/haplotype).

The link between social concepts such as race with biological concepts like haplotypes can be vague and inaccurate. Ethnicity is a more specific indicator of biological ancestry than race, but it too can provide a poor link. Its assignment to patients can vary based on an individual's assessment and be influenced by the culture in which that individual lives. Like assignments of race, assignments of ethnicity are often too reliant on a handful of visible phenotypes. In clinical data sets that contain race and ethnicity fields, the broader the coverage of categories that appear in the data, the more likely it is that at a biological level, there will be more variety in haplotypes.

Although race and ethnicity may be poor proxies for genetic variability, they can be much better proxies for long standing health inequities, which can in turn suggest broader environmental factors that may pressure aspects of genetic expression.  For example, if a racial or ethnic group tends to experience economic deprivation, then people from that group may not be able to afford treatments. If they do not seek health care opportunities at all because of cost barriers, then they will not leave behind any health records which could inform machine learning algorithms. We address deprivation more in our section for Socio-Economic Status.

#### Data processing issues

**Ethnicity and race values are subjective**. If the race or ethnicity of a patient is assigned, you should understand what criteria were used for classification and consider what kinds of biases might have been involved.  More often the values for these variables tend to be assigned by patients themselves, which can also be subjective.

**Ethnicity and race are often conflated**. Both race and ethnicity are social constructs but often race forms broad headings for ethnicity classifications.

**Ethnicity classifications are often not mutually exclusive**. Categories of ethnicity can include aspects of nationality, geography and skin colour which are not mutually exclusive. As an example of how this can happen, consider the [NHS's ethnic category code list](https://www.datadictionary.nhs.uk/data_dictionary/data_field_notes/p/pds/pds_ethnic_category_code_de.asp?shownav=1). 

Now imagine a patient who was born in 1940 in India to a white Welsh mother and a non-white Muslim father who was born and raised in India. In 1947, her family moved from India to Pakistan, a country which only came into existence during the Indian Partition. Later in life she moved to the UK, and became settled in Scotland. Several of these codes may apply and her perception of which ones are most relevant might change over time:

```
CB: Scottish
CX: Mixed White
C3: Other white, white unspecified
C: Any other White background
A: British, Mixed British
J: British Pakistani or Pakistani
H: Indian or British Indian
F: White and Asian
CC: Welsh
```

The vagueness in state-recognised ethnic categories can also change over time. For example, forms for the US census only began to allow participants to specify multiple racial categories in 2000 [19](https://www.pewsocialtrends.org/2015/06/11/multiracial-in-america/).

The value in self-reported ethnicity fields may not be in the accuracy of any one patient's records but in the category coverage of many patients' records. The broader the coverage, the more likely that patient cohorts will appear less homogenous. 

Harmonising different coding systems can be challenging. It can be difficult to standardise race and ethnicity fields across data sources which use different national classification systems. For example the [HL7 FHIR race codes](http://hl7.org/fhir/us/core/stu1/ValueSet-detailed-race.html) are very different from the [NHS ethnicity codes](https://www.datadictionary.nhs.uk/data_dictionary/data_field_notes/p/pds/pds_ethnic_category_code_de.asp?shownav=1). Significant work may be required to reconcile values from American and British based health data.


### Socio-economic Status

#### Meanings
Socioeconomic status (SES) is "...the social standing or class of an individual or group. It is often measured as a combination of education, income and occupation." [20](https://www.apa.org/topics/socioeconomic-status). 

In health research, SES quantifies aspects of health inequalities, some of which may be health inequities. A health inequality is "...any difference in the distribution of health status or health determinants between different population groups" [21](https://www.publichealthontario.ca/-/media/documents/S/2013/socioeconomic-inequality-measures.pdf?la=en). A health inequity is "...a specific type of health inequality that denotes an unjust difference in health." [22](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4481045/)

Young people tend to enjoy better health than old people. This is a health inequality because the difference is related to biology and is not usually considered preventable. In the USA, African-Americans have experienced a disproportionate number of fatalities for COVID-19 relative to their percentage make-up for the general population. This is a health inequity because many causes for the disproportion relate to aspects of social justice [23](https://www.brookings.edu/blog/the-avenue/2020/04/16/mapping-racial-inequity-amid-the-spread-of-covid-19/).

Socio-economic status is often measured either for individuals or for regions. Individual SES measurements can measure income, educational attainment, or occupation. Area-based SES measurements can be based on factors such as average neighbourhood income or be based on complex area deprivation index systems. Often area-based SES measurements are used as a proxy when individual SES data are not available.

#### Why it is important in precision medicine
The importance of SES for health is well appreciated in epidemiology. According to [24](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3951370/): "Individuals with lower SES experience more chronic disease, are less likely to receive preventive care, and have shorter life expectancies." Low SES has almost the same effect on health as smoking or a sedentary lifestyle [25](https://www.imperial.ac.uk/news/177249/early-death-health-linked-socioeconomic-status/#:~:text=The%20research%2C%20published%20in%20The,being%20inactive%20(2.4%20years)). Kivimaki's study found that socioeconomic status was associated with increased risk for 18 of 56 conditions. Globally, poorer older adults experience more dental disease and disability [26](https://www.frontiersin.org/articles/10.3389/fpubh.2020.00231/full). 

Sometimes socioeconomic measurements are left out of processes for patient recruitment for clinical trials data. For example, the prevalence of Chronic Obstructive Pulmonary Disease (COPD) and asthma is associated with socioeconomic status. However, "...deprivation is rarely  considered in typical large-scale efficacy randomised trials that recruit highly selected patient populations [27](https://openres.ersjournals.com/content/6/1/00193-2019). 

Data sources for precision medicine can reflect a bias in SES levels. For example, in the Danish National Birth Cohort, groups with low socioeconomic values for education, occupation and income status are underrepresented compared to the background population [28](https://pubmed.ncbi.nlm.nih.gov/20349116/). UK Biobank participants are more likely to live in less socioeconomically deprived areas than non-participants [29](https://academic.oup.com/aje/article/186/9/1026/3883629).

Patients from low socio-economic levels may experience trouble affording treatments or managing the travel logistics of getting a treatment center. They may also tend to have health journeys that are fragmented across multiple healthcare organisations [30](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6347576/). These problems can mean patients from poorer backgrounds are less represented in data sets.

#### Data processing issues
SES is poorly covered in health data sets.

SES has different scales. The UK uses the National Statistics Socio-Economic Classification (NS-SEC) system [31](https://www.ons.gov.uk/methodology/classificationsandstandards/otherclassifications/thenationalstatisticssocioeconomicclassificationnssecrebasedonsoc2010). UK Biobank uses the Townsend Deprivation Index [32](https://www.statistics.digitalresources.jisc.ac.uk/dataset/2011-uk-townsend-deprivation-scores). In India, Prasad, Pareek, and Kuppuswamy scales are used to measure the SES of a family [33](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3893998/). For small areas, England  uses the English Indices of Deprivation (IoD) [34](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/835115/IoD2019_Statistical_Release.pdf), whereas the Canadian province of Ontario uses the Ontario Marginalization Index [35](https://www.publichealthontario.ca/-/media/documents/S/2013/socioeconomic-inequality-measures.pdf?la=en).

Be aware of the limitations of using area-based indicators for individuals. Remember that just because an individual lives in a neighbourhood with a socioeconomic status does not mean that person has a similar status.

Be aware of how SES is calculated across data sources. For example, some measures of SES rely on an asset-based wealth index, whereas others use income and expenditure.  