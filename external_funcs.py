import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import re


def fill_mins_to_subway(df):

    ''' Fills the nulls of mins_to_subway using the average mins_to_subway for the corresponding zip code '''

    avg_subway_time_per_zip = df[['addr_zip', 'min_to_subway']].groupby('addr_zip').mean()
    avg_subway_time_per_zip = avg_subway_time_per_zip.fillna(avg_subway_time_per_zip.max())
    return df['min_to_subway'].fillna(df[df['min_to_subway'].isnull()].apply(lambda row: avg_subway_time_per_zip.loc[row['addr_zip']][0], axis=1))


def fill_size_sqft(df):
    ''' 
    Use Linear Regression to fill the size_sqft using bathrooms and bedrooms count. 
    '''
    data = df[['size_sqft', 'bathrooms', 'bedrooms']]
    # Setup and fit model
    train_data = data.loc[data['size_sqft'] != 0]
    clf = LinearRegression()
    features = ['bathrooms', 'bedrooms']
    clf.fit(train_data[features], train_data['size_sqft'])

    df.loc[df['size_sqft'] == 0, 'size_sqft'] = np.NaN

    test_data = df.loc[df['size_sqft'].isna()]
    predicted_sqft = clf.predict(test_data[features])
    sqft_predict = pd.Series(index= test_data.index, data = predicted_sqft)

    return df['size_sqft'].fillna(sqft_predict)


def fill_floor_count(df):
    
    ''' 
    Use Linear Regression to fill the floorcount using the given features. If the row does not contain all the features used to model, 
    then the floorcount will remain null. 
    '''

    # Setup to model floor_count after certain features
    df = pd.get_dummies(df, columns=['borough'])
    data = df[['floor_count','floornumber', 'has_childrens_playroom', 'has_pool', 'has_concierge', 'has_garage', 'has_gym', 'borough_Queens', 'borough_Bronx', 'borough_Manhattan', 'borough_Brooklyn', 'borough_Staten Island']]
    data = data.dropna(subset=['floor_count', 'floornumber', 'has_childrens_playroom', 'has_pool', 'has_concierge', 'has_garage', 'has_gym', 'borough_Queens', 'borough_Bronx', 'borough_Manhattan', 'borough_Brooklyn', 'borough_Staten Island'])

    # Setup and fit model
    clf = LinearRegression()
    features = ['floornumber', 'has_childrens_playroom', 'has_pool', 'has_concierge', 'has_garage', 'has_gym', 'borough_Queens', 'borough_Bronx', 'borough_Manhattan', 'borough_Brooklyn', 'borough_Staten Island']
    clf.fit(data[features], data['floor_count'])

    # Anything with floor count of 0 is labeled as NaN
    df.loc[df['floor_count'] == 0, 'floor_count'] = np.NaN

    # Make all NaN into test set
    test = df.loc[(df['floor_count'].isna()) & (df['floornumber'].isna() == 0)]

    # Predict with the model and round up to get floor count 
    imputed_floorcount = np.ceil(clf.predict(test[features]))

    df.loc[(df['floor_count'].isna()) & (df['floornumber'].isna() == 0), 'floor_count'] = imputed_floorcount

    return df[['floor_count', 'floornumber']].apply(lambda row: max(row['floor_count'], row['floornumber']), axis=1)


def fill_floornumber_rules(df):

    '''
    Fills floornumber using various rules applied to the unit.
    NOTE: The floor_count is necessary for this function to work.
    NOTE: I'll condense after first deadline to make cleaner
    '''
    df_clean = df.dropna(subset=['unit']).copy(deep=True)
    df_clean['unit_split'] = df_clean['unit'].apply(lambda row: re.findall(r"[^\W\d_]+|\d+", row))
    df_clean['unit_num'] = df_clean['unit_split'].apply(lambda row: list(filter(lambda x: x.isnumeric(), row)))
    df_clean['unit_str'] = df_clean['unit_split'].apply(lambda row: list(filter(lambda x: x.isnumeric() == 0, row)))

    def fill_floornumber1(df):
        # Fill according to first number in apt unit
        floornumber_fill = df.loc[(df['floornumber'].isna()) & (df['unit_num'].apply(lambda row: len(row) > 0))].apply(
        lambda row: int(row['unit_num'][0][0]) if int(row['unit_num'][0][0]) <= row['floor_count'] else np.NaN, axis = 1).dropna()

        return floornumber_fill
    
    def fill_floornumber2(df):
        # Fill according to letter in apt unit, s.t A = 1, B = 2,...
        floornumber_fill = df.loc[(df['unit_num'].apply(lambda row: len(row) == 0)) & (df['floornumber'].isna()) & 
        (df['unit_str'].apply(lambda row: len(row) > 0 and len(row[0]) == 1))].apply(
        lambda row: float(ord(row['unit_str'][0]) - 64) if float(ord(row['unit_str'][0]) - 64) <= row['floor_count'] else np.NaN, axis = 1).dropna()

        return floornumber_fill
    
    def fill_floornumber3(df):
        floornumber_fill = df.loc[df['addr_unit'].apply(lambda row: bool(re.match(r".*TOP.*", row)))].apply(lambda row: row['floor_count'], axis = 1)
        return floornumber_fill if len(floornumber_fill) > 0 else None
    
    def fill_floornumber4(df):
        floornumber_fill = df.loc[df['addr_unit'].apply(lambda row: bool(re.match(r".*UP.*", row)))].apply(lambda row: row['floor_count'], axis = 1)
        return floornumber_fill if len(floornumber_fill) > 0 else None

    def fill_floornumber5(df):
        floornumber_fill = df.loc[df['addr_unit'].apply(lambda row: bool(re.match(r".*G.*.*N.*", row)) or bool(re.match(r".*G.*.*D.*",row)))].apply(lambda row: 1, axis = 1)
        return floornumber_fill if len(floornumber_fill) > 0 else None

    def fill_floornumber6(df):
        # Penthouse
        floornumber_fill = df.loc[df['addr_unit'].apply(lambda row: bool(re.match(r".*PENT.*", row)))].apply(
            lambda row: row['floor_count'] , axis = 1)
        return floornumber_fill if len(floornumber_fill) > 0 else None

    def fill_floornumber7(df):
        # PH = Penthouse
        floornumber_fill = df.loc[df['addr_unit'].apply(lambda row: bool(re.match(r".*PH.*", row)))].apply(
            lambda row: row['floor_count'] , axis = 1)
        return floornumber_fill if len(floornumber_fill) > 0 else None

    def fill_floornumber8(df):
        floornumber_fill = df.loc[df['addr_unit'].apply(lambda row: bool(re.match(r".*ONE.*", row)))].apply(
            lambda row: 1 , axis = 1)
        return floornumber_fill if len(floornumber_fill) > 0 else None

    def fill_floornumber9(df):
        floornumber_fill = df.loc[df['addr_unit'].apply(lambda row: bool(re.match(r".*TWO.*", row)))].apply(
            lambda row: 2 , axis = 1)
        return floornumber_fill if len(floornumber_fill) > 0 else None

    def fill_floornumber10(df):
        floornumber_fill = df.loc[df['addr_unit'].apply(lambda row: bool(re.match(r".*THREE.*", row)))].apply(
            lambda row: 3 , axis = 1)
        return floornumber_fill if len(floornumber_fill) > 0 else None

    def fill_floornumber11(df):
        # Parlor 
        floornumber_fill = df.loc[df['addr_unit'].apply(lambda row: bool(re.match(r".*PA.*L.*R.*", row)))].apply(
            lambda row: 1, axis = 1)
        return floornumber_fill if len(floornumber_fill) > 0 else None

    def fill_floornumber12(df):
        # Lower Level
        floornumber_fill = df.loc[df['addr_unit'].apply(lambda row: bool(re.match(r".*LL.*", row)))].apply(
            lambda row: 1, axis = 1)
        return floornumber_fill if len(floornumber_fill) > 0 else None
    
    def fill_floornumber13(df):
        floornumber_fill = df.loc[df['addr_unit'].apply(lambda row: bool(re.match(r".*WALK-IN.*", row)))].apply(
        lambda row: 1 , axis = 1)
        return floornumber_fill if len(floornumber_fill) > 0 else None
    
    def fill_floornumber_re(df):
        # Combines all the regex fills
        return fill_floornumber3(df).append(fill_floornumber4(df)).append(fill_floornumber5(df)).append(
            fill_floornumber6(df)).append(fill_floornumber7(df)).append(fill_floornumber8(df)).append(
            fill_floornumber9(df)).append(fill_floornumber10(df)).append(fill_floornumber11(df)).append(
            fill_floornumber12(df)).append(fill_floornumber13(df))
    
    # Ordering matters, so that earlier rules get precendence 
    return df_clean['floornumber'].fillna(fill_floornumber1(df_clean)).fillna(
        fill_floornumber_re(df_clean)).fillna(fill_floornumber2(df_clean))


def fill_floornumber_default(df):
    '''
    Fills floornumber with floor_count. Last when fill_floornumber function doesn't work
    '''
    floornumber_fill = df.loc[df['floornumber'].isna()].apply(lambda row: row['floor_count'], axis=1)
    return floornumber_fill


def fill_floornumber_final(df):
    '''combines fill_floornumber_rules and fill_floornumber_default for ease of use'''
    return df.floornumber.fillna(fill_floornumber_rules(df)).fillna(fill_floornumber_default(df))


def number_privileges(df):
    '''
    Number of privileges sums up the values of all columns that have "has" as well as "is furnished" and "allows_pets"
    '''

    r = re.compile(r"has.*")
    fancy_stuff = list(filter(r.match, df.columns))
    fancy_stuff.extend(['is_furnished','allows_pets'])
    
    return np.sum(df[fancy_stuff].values,1)


def number_of_parks(parks_df, df):
    '''
    Given parks_df with appropriate addresses, will return number of parks in a 500m radius for each address
    '''
    parks_df.set_index('addr_street', inplace=True)
    num_parks = pd.Series(parks_df['number_of_parks'])
    return df.apply(lambda row: int(num_parks[row['addr_street']]), axis=1)


def park_level(df):
    return df['number_of_parks'].apply(lambda x: 3 if x > 12 else (2 if x > 6 else 1))


def number_of_schools(schools_df, df):
    '''
    Given schools_df with appropriate addresses, will return number of schools in a 400m radius for each address
    '''

    schools_df.set_index('addr_street', inplace=True)
    num_schools = pd.Series(schools_df['number_of_schools'])
    return df.apply(lambda row: int(num_schools[row['addr_street']]), axis=1)


def school_level(df):
    return df['number_of_schools'].apply(lambda x: 1 if x > 19 else 0)