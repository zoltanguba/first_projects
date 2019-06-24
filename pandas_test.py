import pandas as pd

orders = pd.read_csv('pandas.csv')



###  Select top 5 rows
#  print(orders.head())

### Show only the column names of the DataFrame
#print(orders.columns)

###  Select a pandas Series from a DataFrame
#  print(orders['FY'])
#  print(type(orders.FY))

###  Show the dimensions (row and column numbers) of the DataFrame
#  print(orders.shape)

### Create new dolumn in DataFrame
#  orders['test'] = str(orders.FY) + orders.Customer
#  print(orders.head())

### Show statistics on numeric values
#  print(orders.describe())

### Replace characters in column names
#  orders.rename(columns={'FY':'Financial Year'}, inplace=True)
#  print(orders.columns)

#  orders_cols = ['col1', 'col2', 'col3', 'col4', 'col5']
#  orders.columns = orders_cols
#  print(orders.columns)

#  orders = pd.read_csv('pandas.csv', names=orders_cols, header=0)

#  orders.columns = orders.columns.str.replace(' ', '_')

### Drop column
#  orders.drop('FY', axis=1, inplace=True)

### Drop row
#  orders.drop([1, 2], axis=0, inplace=True)

### Sort DataFrame
#  print(orders.Revenue.sort_values())
#  print(orders.sort_values('Revenue', ascending=False))

### Filter rows
#  is_big = orders.Revenue >= 1600
#  print(orders[is_big])
#  print(orders[orders.Revenue >= 1600])
#  print(orders.loc[orders.Revenue >= 1600, 'Customer'])
#  print(orders[(orders.Revenue >= 1600) & (orders.FY == 2017)])
#  print(orders[(orders.Revenue >= 1600) | (orders.FY == 2017)])
#  print(orders[orders.FY.isin([2017, 2018])])

### Calculate meean for numeric columns
#  print(orders.mean(axis=0),)

### Calculate meean for rows
#  print(orders.mean(axis=1),)

### Group by


#  summary = orders.groupby('Customer')

data_input = pd.read_excel('dummy data excel.xlsx')

rev_by_month = []
cos_by_month = []
month = []
revenue = []
year = 2017
coa_rev = 5
coa_cos = 6
yearlyRev = data_input.groupby('Year').get_group(year).groupby('Coa_Class').get_group(coa_rev).groupby('Month')
yearlyCos = data_input.groupby('Year').get_group(year).groupby('Coa_Class').get_group(coa_cos).groupby('Month')
print(yearlyRev)

for Month, revbymonth in yearlyRev:
    temp_rev_list = {'month': '', 'revenue': ''}
    temp_rev_list['month'] = Month
    temp_rev_list['revenue'] = int((yearlyRev.get_group(Month).Amount.sum()))
    rev_by_month.append(temp_rev_list)
print(rev_by_month)

for Month, cosbymonth in yearlyCos:
    temp_cos_list = {'month': '', 'cost': ''}
    temp_cos_list['month'] = Month
    temp_cos_list['cost'] = int((yearlyCos.get_group(Month).Amount.sum()))
    cos_by_month.append(temp_cos_list)
print(cos_by_month)



'''
for Customer, revenue in summary:
    temp_list = {'customer': '', 'revenue': ''}
    temp_list['customer'] = Customer
    temp_list['revenue'] = summary.get_group(Customer).Product
    combined_list.append(temp_list)

    customer_list.append(Customer)
    revenue_list.append(summary.get_group(Customer).Revenue.sum())
#  print(type(summary.get_group(Customer).Revenue.sum()))
#  print(combined_list)


byproductrevenue = summary.get_group('C10')[['Product', 'Revenue']].groupby('Product') #  .get_group('Product41').Revenue.sum()
rev_by_prod = []
product = []
revenue = []
for Product, rev in byproductrevenue:
    temp_rev_by_prod = {'product': '', 'revenue': ''}

    temp_rev_by_prod['product'] = Product
    product.append(Product)

    temp_rev_by_prod['revenue'] = int(byproductrevenue.get_group(Product).Revenue.sum())
    revenue.append(int(byproductrevenue.get_group(Product).Revenue.sum()))

    rev_by_prod.append(temp_rev_by_prod)
#  print(rev_by_prod)
#  print(product, revenue)




#  print(summary.get_group('C10').Revenue.sum())
#  print(orders.groupby('Financial_month').Revenue.sum().values)
#  print(orders.groupby('Customer').Revenue.agg(['count', 'min', 'max', 'mean']))

### Explore
#  print(orders.Customer.value_counts())
#  print(orders.Customer.value_counts(normalize=True))
#  print(pd.crosstab(orders.Customer, orders.Product))
'''