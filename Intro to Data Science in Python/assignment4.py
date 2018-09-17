import pandas as pd
import numpy as np

"""
from scipy.stats import ttest_ind
This assignment requires more individual learning than previous assignments - you are encouraged to check out the pandas documentation to find functions or methods you might not have used yet, or ask questions on Stack Overflow and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.

Definitions:

A quarter is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
A recession is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
A recession bottom is the quarter within a recession which had the lowest GDP.
A university town is a city which has a high percentage of university students compared to the total population of the city.
Hypothesis: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (price_ratio=quarter_before_recession/recession_bottom)

The following data files are available for this assignment:

From the Zillow research data site there is housing data for the United States. In particular the datafile for all homes at a city level, City_Zhvi_AllHomes.csv, has median home sale prices at a fine grained level.
From the Wikipedia page on college towns is a list of university towns in the United States which has been copy and pasted into the file university_towns.txt.
From Bureau of Economic Analysis, US Department of Commerce, the GDP over time of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file gdplev.xls. For this assignment, only look at GDP data from the first quarter of 2000 onward.
Each function in this assignment below is worth 10%, with the exception of run_ttest(), which is worth 50%.

"""

def get_list_of_university_towns():
    
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    with open("university_towns.txt") as f:
        townslist = f.readlines()
    
    townslist = [x.rstrip() for x in townslist]  
    townslist2 = list()
    for i in townslist:
        if i[-6:] == '[edit]':
            temp_state = i[:-6]
        elif '(' in i:
            town = i[:i.index('(') - 1]
            townslist2.append([temp_state, town])
        else:
            town = i
            townslist2.append([temp_state, town])

    college_towns = pd.DataFrame(townslist2, columns=['State','RegionName'])
    return college_towns

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    gdp_levels = pd.read_excel('gdplev.xls', skiprows=219)
    gdp_levels = gdp_levels[['1999q4', 12323.3]]
    gdp_levels = gdp_levels.rename(columns={'1999q4': 'Quarter',
                                            12323.3: 'GDP (billions)'})
    
    for i in range(0,gdp_levels.shape[0]-1):
        if gdp_levels['GDP (billions)'][i] > gdp_levels['GDP (billions)'][i+1] and gdp_levels['GDP (billions)'][i+1] > gdp_levels['GDP (billions)'][i+2]:
                start_date = gdp_levels['Quarter'][i-1]
                
    return start_date

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    
    gdp = pd.read_excel("gdplev.xls", skiprows=219)
    gdp = gdp[['1999q4', 12323.3]]
    gdp = gdp.rename(columns={'1999q4':'Quarter', 12323.3:'GDP in billions'})
    
    startdate = get_recession_start()
    
    rise_list = list()
    for i in range(gdp.index[gdp['Quarter'] == startdate][0], gdp.shape[0] - 2):
        if gdp['GDP in billions'][i] < gdp['GDP in billions'][i + 1] < gdp['GDP in billions'][i + 2]:
            rise_list.append(gdp['Quarter'][i + 2])
    enddate = rise_list[0]
    return enddate

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3''' 
    
    gdp = pd.read_excel("gdplev.xls", skiprows=219)
    gdp = gdp[['1999q4', 12323.3]]
    gdp = gdp.rename(columns={'1999q4':'Quarter', 12323.3:'GDP in billions'})
   
    startdate = get_recession_start()
    enddate = get_recession_end()
    
    rise_list = list()
    for i in range(gdp.index[gdp['Quarter'] == startdate][0], gdp.shape[0] - 2):
        if gdp['GDP in billions'][i] < gdp['GDP in billions'][i + 1] < gdp['GDP in billions'][i + 2]:
            rise_list.append(gdp['Quarter'][i + 2])
    enddate = rise_list[0]
    
    temp_min = 10000000

    for i in range(gdp.index[gdp['Quarter'] == startdate][0], gdp.index[gdp['Quarter'] == enddate][0]):
        if gdp['GDP in billions'][i] < temp_min:
            temp_min = gdp['GDP in billions'][i]
            bottomdate = gdp['Quarter'][i]
        
    return bottomdate

def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    houses = pd.read_csv('City_Zhvi_AllHomes.csv')
    for i in range(2000,2017):
        if i == 2016:
            houses[str(i) + 'q1'] = houses[[str(i)+'-01', str(i)+'-02', str(i)+'-03']].mean(axis=1)
            houses[str(i) + 'q2'] = houses[[str(i)+'-04', str(i)+'-05', str(i)+'-06']].mean(axis=1)
            houses[str(i) + 'q3'] = houses[[str(i)+'-07', str(i)+'-08']].mean(axis=1)
        else:
            houses[str(i) + 'q1'] = houses[[str(i)+'-01', str(i)+'-02', str(i)+'-03']].mean(axis=1)
            houses[str(i) + 'q2'] = houses[[str(i)+'-04', str(i)+'-05', str(i)+'-06']].mean(axis=1)
            houses[str(i) + 'q3'] = houses[[str(i)+'-07', str(i)+'-08', str(i)+'-09']].mean(axis=1)
            houses[str(i) + 'q4'] = houses[[str(i)+'-10', str(i)+'-11', str(i)+'-12']].mean(axis=1)

    houses = houses.drop(houses.columns[[0] + list(range(3,251))],axis=1)
    houses = houses.replace({'State':states})
    houses = houses.set_index(['State', 'RegionName'])
    return houses

def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    towns = get_list_of_university_towns()
    startdate = get_recession_start()
    bottomdate = get_recession_bottom()
    houses = convert_housing_data_to_quarters()
    
    houses = houses.reset_index()
    houses['recession_diff'] = houses[startdate] - houses[bottomdate]
    
    towns_houses = pd.merge(houses, towns, how='inner', on=['State', 'RegionName'])
    towns_houses['ctown'] = True
    houses = pd.merge(houses, towns_houses, how='outer', on = ['State', 'RegionName',
                                                              bottomdate, startdate, 
                                                              'recession_diff'])
    houses['ctown'] = houses['ctown'].fillna(False)
    unitowns = houses[houses['ctown'] == True]
    not_unitowns = houses[houses['ctown'] == False]
    
    t, p = ttest_ind(unitowns['recession_diff'].dropna(), not_unitowns['recession_diff'].dropna())
    different = True if p < 0.01 else False
    better = "university town" if unitowns['recession_diff'].mean() < not_unitowns['recession_diff'].mean() else "non-university town"
    
            
    return different, p, better

run_ttest()

