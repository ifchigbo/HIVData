import numpy as np
import pandas as pd
from IPython.display import display
df = pd.read_csv("HIV_AIDS_Diagnoses_by_Neighborhood__Sex__and_Race_Ethnicity.csv", encoding='utf-8')
# Load the dataset from the CSV Library


#Check t verify the datatypes of the variables in the dataset
def getDatatypes():
    try:
        return df.dtypes
    except BaseException as error:
        print(error)

def getPercentageofNaN():
    try:
        return df.isna().sum() / df.shape[0] * 100
    except BaseException as error:
        print(error)

# Convert Columns that are not numeric to numeric - float64
def convertColumnstoNumeric():
    try:
        # Get the List of numeric columns
        numeric_columns = ['TOTAL NUMBER OF HIV DIAGNOSES', 'HIV DIAGNOSES PER 100,000 POPULATION',
                           'TOTAL NUMBER OF CONCURRENT HIV/AIDS DIAGNOSES',
                           'PROPORTION OF CONCURRENT HIV/AIDS DIAGNOSES AMONG ALL HIV DIAGNOSES',
                           'TOTAL NUMBER OF AIDS DIAGNOSES',"AIDS DIAGNOSES PER 100,000 POPULATION"]
        for items in numeric_columns:
            df[items] = pd.to_numeric(df[items], errors = 'coerce')
        #DataCleaning Processing
        # 1. Remove the \n character from the datasets
        df['Neighborhood (U.H.F)'] = df['Neighborhood (U.H.F)'].str.replace('\n','')
        df['RACE/ETHNICITY'] = df['RACE/ETHNICITY'].str.replace('\n', '')
        df['Borough'] = df['Borough'].str.replace('\n','')
    except BaseException as error:
        print(error)

#Consolidate Niegborhood Datatset
def consolidateNeigborhoodNames():
    convertColumnstoNumeric()
    try:
        df['Neighborhood (U.H.F)'] = df['Neighborhood (U.H.F)'].str.replace(' -','-').str.replace('- ','-').str.replace(' ','')
        df['Neighborhood (U.H.F)'] = [names.lower() for names in df['Neighborhood (U.H.F)']]
        #df['Borough'] = [bor.lower() for bor in df['Borough']]
        df['SEX'] = [gender.lower() for gender in df['SEX']]
    except BaseException as error:
        print(error,  " I am here ")



def consolidateRaceEth():
    consolidateNeigborhoodNames()
    try:
        df['RACE/ETHNICITY'] = df['RACE/ETHNICITY'].str.replace(' ','').str.replace('Latino/Hispanic','Hispanic').str.replace('Other/Unknown','Unknown')
        df['RACE/ETHNICITY'] = [names.lower() for names in df['RACE/ETHNICITY']]
    except BaseException as error:
        print(error)


def comparisonBoroughNeigh():
    #I will be using this method to compare neigborhood with same name that have a  corresponding borough and those that do no have a corresponding borough
    #With this i will be able to fill nan values on the borough column
    #since the neighborhood appears one than once for the corresponding borough - this enables me to be ablel to put in the right names for the corresponfing borough with similar names
    consolidateRaceEth()
    try:
        return df[['Neighborhood (U.H.F)','Borough']]
    except BaseException as error:
        print(error)

def cleanedDataSet():
    try:
        # For any niegborhood with an unknown value find its corresponding borough with an unkonwn value
        df.loc[df['Neighborhood (U.H.F)'] == 'unknown', 'Borough'] = df['Borough'].fillna('unknown')
        my_neighborhood = []
        my_borough = []
        # iterate over the unique values in the 'Neighborhood (U.H.F)' column
        for neighborhood in df['Neighborhood (U.H.F)'].unique():
            # select the first row of the DataFrame for the current neighborhood
            neighborhood_df = df[(df['Neighborhood (U.H.F)'] == neighborhood) & (df['Borough'].notna())][
                ['Borough', 'Neighborhood (U.H.F)']].head(1)
            neighborhood_df.to_dict()
            my_neighborhood.append(neighborhood_df['Neighborhood (U.H.F)'].to_string(index=False))
            my_borough.append(neighborhood_df['Borough'].to_string(index=False))
        zip_records = zip(my_neighborhood, my_borough)
        dataset_values = dict(zip_records)
        #The Section below fullfils the requirement of getting neighborhoods with known borough and filling known neighborhood boroughs with same name
        count = 0
        mylist = list(dataset_values.keys())
        while count < df.shape[0]:
            id = df['Neighborhood (U.H.F)'][count]
            print(id)
            print(dataset_values[id])
            if id in mylist:
                # print("found")
                df.loc[count, ['Borough']] = dataset_values[id]
            else:
                print("not found ")
            count += 1
        df['Borough'] = [bor.lower() for bor in df['Borough']]
    except BaseException as error:
        print(error)


def finalDataFomarting():
    try:
        None
    except BaseException as error:
        print(error)