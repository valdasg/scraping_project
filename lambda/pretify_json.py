# Make neccesary imports
import pandas as pd
from common_functions import get_salary_definition, calc_nett_salary, get_salary
import boto3, os, json
from io import BytesIO


def pretify_json(bucket, key):
    # Create S3 connection
    s3_client = boto3.client('s3')
    
    # Read file body and load it as string
    json_obj = (s3_client.get_object(Bucket=bucket, Key=key))['Body'].read()
    json_dict = json.loads(json_obj)
    
    # Create pandas dataframe
    df = pd.DataFrame(json_dict)
    
    # Prepare salary and salary payment field
    salary = pd.Series(df['salary'])
    payment_way = pd.Series(df['salary_payment'])
    df['salary_n'] = salary.apply(get_salary)
    df['salary_payment_way'] = payment_way.apply(get_salary_definition)

    # Delete obsolete fields
    del df['salary_payment']
    del df['salary']

    # Separate salaries from and to
    df['salary_from'] = df['salary_n'].apply(lambda x: x.get('salary_from'))
    df['salary_to'] = df['salary_n'].apply(lambda x: x.get('salary_to'))

    # delete obsolete salary field
    del df['salary_n']


    # Convert all salaries to nett
    df['salary_from'] = df.apply(lambda x: calc_nett_salary(x['salary_from'], x['salary_payment_way']), axis=1)
    df['salary_from'] = df.apply(lambda x: calc_nett_salary(x['salary_to'], x['salary_payment_way']), axis=1)

    # delete obsolete salary payment field, since all salaries are converted to nett
    del df['salary_payment_way']

    # Return json file
    return df.to_json(orient='records', lines=True)


