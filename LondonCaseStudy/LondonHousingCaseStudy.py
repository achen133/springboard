#[1.1] Import Libs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#[1.2] Loading Data
url_data = "https://data.london.gov.uk/download/uk-house-price-index/70ac0766-8902-4eb5-aab5-01951aaed773/UK%20House%20price%20index.xls"
properties = pd.read_excel(url_data, sheet_name='Average price', index_col=None, engine='openpyxl')


#[2.1] Explore Data
divider = '----------' * 10
print('\n\n\n' + divider + '\n\n\nORIGINAL DATA ' + str(properties.shape) + ':\n\n\n', properties.head(), '\n\n\n') #print original data


#[2.2] Clean Data (Set x&y axis variables for dataframe)
properties_T = properties.T #transpose
properties_T = properties_T.reset_index() #sets integers as index
properties_T.columns = properties_T.iloc[0] #sets col_headers as first row date values
properties_T = properties_T.drop(0)


#[2.3] Clean Data (Filling in N/A data)
properties_T = properties_T.rename(columns = {'Unnamed: 0':'London_Borough', pd.NaT: 'ID'}) #renaming N/A values
properties_T = properties_T.iloc[:, :-1] #take entire df except for last 'ID' column


#[2.4] Transform Data
clean_properties = properties_T.melt(id_vars= ['London_Borough', 'ID']) #unpivot from wide to long format w/ date as variable
clean_properties = clean_properties.rename(columns = {0:'Month', 'value':'Average_price'}) #rename values
#print(clean_properties.dtypes) #check data types


#[2.5] Clean Data (Subset data)
#print(clean_properties['London_Borough'].unique()) #check col headers
#print(clean_properties[clean_properties['London_Borough'] == 'Unnamed: 34'].head()) #check for variables that are not part of dataset
borough_list = clean_properties['London_Borough'].unique()[1:33] #list of accepted boroughs in col headers
clean_properties = clean_properties[clean_properties['London_Borough'].isin(borough_list)] #subset data to include only london boroughs
NaNFreeDF = clean_properties[clean_properties['Average_price'].notna()] #drops NaN values & deletes row (alt: clean_properties.dropna())
df = NaNFreeDF #name final/analysis-ready data as 'df'
print(divider + '\n\n\nFINAL DATA ' + str(df.shape) + ':\n\n\n', df.head(), '\n\n\n') #print final data


#[2.6] Visualize Data
camden_prices = df[df['London_Borough'] == 'Camden'] 
ax = camden_prices.plot(kind='line', x='Month', y='Average_price', ylabel='Price', title='Camden Average Housing Price') #single borough lineplot

df['Year'] = df['Month'].apply(lambda t: t.year) #add 'Year' column to calculate yearly stats
df['Average_price'] = pd.to_numeric(df['Average_price'], errors='coerce', downcast='float') #switch data type of price from object to integer and exclude '-' string
dfg = df.groupby(['London_Borough', 'Year'])['Average_price'].agg('mean') #calculate yearly mean
dfg = dfg.reset_index() #add index
print(divider + '\n\n\nAVERAGE PRICE DATA ' + str(dfg.shape) + ':\n\n\n', dfg.sample(10), '\n\n\n') #print average price data

#[3] Modelling
def create_price_ratio(data_frame, borough): #returns ratio of 1998 amd 2018 price
    subset = data_frame[data_frame['London_Borough'] == borough]
    price_1998 = subset['Average_price'][subset['Year'] == 1998]
    price_2018 = subset['Average_price'][subset['Year'] == 2018]
    ratio = float(price_2018) / float(price_1998)
    return ratio

final = {} #create dict for ratio price
for x in dfg['London_Borough'].unique():
    final[x] = create_price_ratio(dfg, x) #append value to Borough key

df_ratios = pd.DataFrame(final, index=['2018'], columns=borough_list) #create df for ratio price
df_ratios_T = df_ratios.T #transpose
df_ratios = df_ratios_T.reset_index() #reset index
df_ratios.rename(columns={'index':'Borough'}, inplace=True) #rename header
print(divider + '\n\n\nPRICE RATIO DATA ' + str(df_ratios.shape) + ':\n\n\n', df_ratios, '\n\n\n') #print ratio data

top15 = df_ratios.sort_values(by='2018',ascending=False).head(15) #sample of top 15 price increase
print(divider + '\n\n\nTOP 15 PRICE RATIO DATA ' + str(top15.shape) + ':\n\n\n', top15, '\n\n\n' + divider + '\n') #print top15 

ax = top15[['Borough', '2018']].plot(kind='bar', ylabel='Factor Increased', title='Top 15 Boroughs with the Greatest Increase in Housing Prices', rot=60) #top 15 price increase barplot
ax.set_xticklabels(top15.Borough) #set Borough names as x-axis ticks
plt.show()

#[4] Conclusion
#print(df_ratios.std())
#print(df_ratios.mean())
conclusion = '''
   In conclusion, the overall average housing prices for all 32 boroughs in London increased by a factor of 4.7 
   with a standard deviation of 0.57. The three boroughs that saw the greatest increase in average housing prices 
   were Hackney, Waltham Forest, and Southwark by factors of 6.2, 5.8, and 5.5, respectively. On the other hand, 
   the three boroughs that saw the least increase in average housing prices were Hounslow, Richmond upon Thames, 
   and Harrow by factors of 3.98, 4.00, and 4.06, respectively. Price is only a single determining factor within 
   a multitude of options to consider when searching for a desired area of residence. Other factors that can be 
   considered are census data, environmental data, commercial data, specific housing size data, etc.'''

print('\nCONCLUSION:\n' + conclusion + '\n\n')

