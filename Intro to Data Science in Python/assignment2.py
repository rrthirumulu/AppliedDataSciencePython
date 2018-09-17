import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
df.head()

# Question 0: What is the first country in df?
def answer_zero():
    return df.iloc[0]	
answer_zero() 

# Which country has won the most gold medals in summer games?
def answer_one():
    return df['Gold'].argmax()
answer_one()

# Which country had the biggest difference between their summer and winter gold medal counts?
def answer_two():
    return (df['Gold']-df['Gold.1']).argmax()
answer_two()

# Which country has the biggest difference between their summer gold medal counts and winter gold medal counts relative to their total gold medal count?
def answer_three():
    copy_df = df.copy()
    copy_df = copy_df[(copy_df['Gold']>0) & (copy_df['Gold.1']>0)]
    return ((copy_df['Gold'] - copy_df['Gold.1'])/copy_df['Gold.2']).argmax()
answer_three()

# Write a function that creates a Series called "Points" which is a weighted value where each gold medal (`Gold.2`) counts for 3 points, 
# silver medals (`Silver.2`) for 2 points, and bronze medals (`Bronze.2`) for 1 point
def answer_four():
    df['Points'] = (df['Gold.2'])*3 + (df['Silver.2'])*2 + (df['Bronze.2'])
    return df['Points']
answer_four()

# 2nd part which analyzes census data
census_df = pd.read_csv('census.csv')
census_df.head()

# Which state has the most counties in it? (hint: consider the sumlevel key carefully! You'll need this for future questions too...)
def answer_five():
    return census_df['STNAME'].value_counts().argmax()
answer_five()

# Only looking at the three most populous counties for each state, what are the three most populous states (in order of highest population to lowest population)? Use CENSUS2010POP.
def answer_six():
    copy_df = census_df.copy()
    copy_df = copy_df.groupby(['STNAME'])
    states_pop = pd.DataFrame(columns=['pop'])
    for i, c in copy_df:
        states_pop.loc[i] = [c.sort_values(by='CENSUS2010POP', ascending=False)[1:4]['CENSUS2010POP'].sum()]
    top3 = states_pop.nlargest(3,'pop')
    return list(top3.index)
answer_six()

# Which county has had the largest absolute change in population within the period 2010-2015?
def answer_seven():
    pop = census_df[['STNAME','CTYNAME','POPESTIMATE2015','POPESTIMATE2014','POPESTIMATE2013','POPESTIMATE2012','POPESTIMATE2011','POPESTIMATE2010']]
    pop = pop[pop['STNAME']!=pop['CTYNAME']]
    index = (pop.max(axis=1)-pop.min(axis=1)).argmax()
    return census_df.loc[index]['CTYNAME']
answer_seven()

# Create a query that finds the counties that belong to regions 1 or 2, whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.
def answer_eight():
    return census_df[(census_df['REGION']<3 ) & (census_df['CTYNAME'] == 'Washington County') & (census_df['POPESTIMATE2015']>census_df['POPESTIMATE2014'])][['STNAME','CTYNAME']]
answer_eight()