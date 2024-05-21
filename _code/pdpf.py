# import pandas as pd
# from pandas_profiling import ProfileReport

# def generate_profile(df):
#     # Generate the profile report
#     profile = ProfileReport(dataframe, explorative=True)
#     return profile


import pandas as pd
from pandas_profiling import ProfileReport
# from pydantic import BaseModel, BaseSettings, Field, PrivateAttr


def generate_profiling_report(df):
    profile = ProfileReport(df, explorative=True)
    return profile.to_html()
