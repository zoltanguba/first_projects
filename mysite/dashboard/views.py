from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
import pandas as pd
#  Source Data
orders = pd.read_csv('dashboard/reports/pandas.csv')
#  Source DataFrame grouped by Customers
summary = orders.groupby('Customer')

coa_rev = 5
coa_cos = 6
data_input = pd.read_excel('dashboard/reports/dummy data excel.xlsx')


def chart(request):
    return render(request, 'dashboard/chart.html', {})


def dashboard(request):
    return render(request, 'dashboard/dashboard.html', {})


def main_dashboard_data(request):
    distinct_years = data_input.Year.unique()

    if request.method == 'GET':
        year = int(request.GET.get('year', None))

    distinct_months = data_input.groupby('Year').get_group(year).Month.unique()

    rev_by_month = []
    cos_by_month = []
    yearlyRev = data_input.groupby('Year').get_group(year).groupby('Coa_Class').get_group(coa_rev).groupby('Month')
    yearlyCos = data_input.groupby('Year').get_group(year).groupby('Coa_Class').get_group(coa_cos).groupby('Month')

    for Month, revbymonth in yearlyRev:
        temp_rev_list = {'month': '', 'revenue': ''}
        temp_rev_list['month'] = Month
        temp_rev_list['revenue'] = int((yearlyRev.get_group(Month).Amount.sum()))
        rev_by_month.append(temp_rev_list)

    for Month, cosbymonth in yearlyCos:
        temp_cos_list = {'month': '', 'cost': ''}
        temp_cos_list['month'] = Month
        temp_cos_list['cost'] = int((yearlyCos.get_group(Month).Amount.sum()))
        cos_by_month.append(temp_cos_list)

    distinct_years_list = []
    for x in distinct_years:
        distinct_years_list.append(int(x))

    distinct_months_list = []
    for i in distinct_months:
        distinct_months_list.append(int(i))

    data = {
        'rev_by_month': rev_by_month,
        'cos_by_month': cos_by_month,
        'year': year,
        'distinct_years_list': distinct_years_list,
        'distinct_months_list': distinct_months_list
    }

    return JsonResponse(data)


def main_dashboard_salesperson(request):
    if request.method == 'GET':

        year = int(request.GET.get('year', None))

    rev_by_salesperson = []
    yearlySalespersonRev = data_input.groupby('Year').get_group(year).groupby('Coa_Class').get_group(coa_rev).groupby('SalesPerson')

    for SalesPerson, revbysalesperson in yearlySalespersonRev:
        temp_rev_list = {'salesperson': '', 'revenue': ''}
        temp_rev_list['salesperson'] = SalesPerson
        temp_rev_list['revenue'] = int(yearlySalespersonRev.get_group(SalesPerson).Amount.sum())
        rev_by_salesperson.append(temp_rev_list)

    data = {
        'data': rev_by_salesperson
    }

    return JsonResponse(data)


def main_dashboard_monthly_table(request):
    if request.method == 'GET':
        year = int(request.GET.get('year'))
        distinct_months = data_input.groupby('Year').get_group(year).Month.unique()
        month = int(max(distinct_months))

    rev_monthly = []
    cos_monthly = []
    monthlyrevdf = data_input.groupby('Year').get_group(year).groupby('Coa_Class').get_group(coa_rev).groupby('Month')

    # /// REVENUES /////////////////////////////////////////////////////////////
    temp_actual = {'actual_rev': ''}
    temp_mom = {'mom_rev': ''}
    temp_yoy = {'yoy_rev': ''}

    #  Checking if monthly rev is valid and append to the response data if so
    try:
        revenue = int(monthlyrevdf.get_group(month).Amount.sum())
        temp_actual['actual_rev'] = revenue
        rev_monthly.append(temp_actual)
    except KeyError:
        temp_actual['actual_rev'] = "N/A"
        rev_monthly.append(temp_actual)

    #  Checking if mom rev is valid and append to the response data if so
    try:
        momrevenue = int(monthlyrevdf.get_group(month - 1).Amount.sum())
        temp_mom['mom_rev'] = round(revenue/momrevenue, 2)*100
        rev_monthly.append(temp_mom)
    except KeyError:
        temp_mom['mom_rev'] = "N/A"
        rev_monthly.append(temp_mom)

    #  Checking if yoy rev is valid and append to the response data if so
    try:
        yoyrevenue = int(
            data_input.groupby('Year').get_group(year - 1).groupby('Coa_Class').get_group(coa_rev).groupby('Month') \
            .get_group(month).Amount.sum())
        temp_yoy['yoy_rev'] = round(revenue/yoyrevenue, 2)*100
        rev_monthly.append(temp_yoy)
    except KeyError:
        temp_yoy['yoy_rev'] = "N/A"
        rev_monthly.append(temp_yoy)



    data = {
        'revenue': rev_monthly,
        'cost': cos_monthly,
        'year': year,
        'month': month
    }

    return JsonResponse(data)


def main_dashboard_customer_chart(request):
    if request.method == 'GET':
        year = int(request.GET.get('year'))

    rev_yearly = []

    customerRevDf = data_input.groupby('Year').get_group(year).groupby('Coa_Class').get_group(coa_rev).groupby('Customer')

    for Customer, revbycustomer in customerRevDf:
        temp_list = {'Customer': '', 'Revenue': ''}
        temp_list['Customer'] = Customer
        temp_list['Revenue'] = int(customerRevDf.get_group(Customer).Amount.sum())
        rev_yearly.append(temp_list)

    data = {
        'rev_yearly': rev_yearly
    }

    return JsonResponse(data)


def main_dashboard_product_chart(request):
    if request.method == 'GET':
        year = int(request.GET.get('year'))

    product_rev_yearly = []

    productRevDf = data_input.groupby('Year').get_group(year).groupby('Coa_Class').get_group(coa_rev).groupby('Product')

    for Product, revbyproduct in productRevDf:
        temp_list = {'Product': '', 'Revenue': ''}
        temp_list['Product'] = Product
        temp_list['Revenue'] = int(productRevDf.get_group(Product).Amount.sum())
        product_rev_yearly.append(temp_list)

    data = {
        'product_rev_yearly': product_rev_yearly
    }

    return JsonResponse(data)


def sub_dashboard_view(request):
    if request.method == 'GET':
        identifier = request.GET.get('identifier')
        year = int(request.GET.get('year'))

#  ////////////////////////////////////////// MONTHLY SUB-DASHBOARD VIEW //////////////////////////////////////////

        if identifier == 'month':
            month = int(request.GET.get('id'))

        #  Customer chart data
            rev_cust = []

            customerRevDf = data_input.groupby('Year').get_group(year).groupby('Coa_Class').get_group(coa_rev).groupby(
                'Month').get_group(month).groupby('Customer')

            for Customer, revbycustomer in customerRevDf:
                temp_list = {'Customer': '', 'Revenue': ''}
                temp_list['Customer'] = Customer
                temp_list['Revenue'] = int(customerRevDf.get_group(Customer).Amount.sum())
                rev_cust.append(temp_list)

        #  Salesperson chart data
            rev_sales = []

            salesRevDf = data_input.groupby('Year').get_group(year).groupby('Coa_Class').get_group(coa_rev).groupby(
                'Month').get_group(month).groupby('SalesPerson')

            for SalesPerson, revbysalesperson in salesRevDf:
                temp_list = {'salesperson': '', 'revenue': ''}
                temp_list['salesperson'] = SalesPerson
                temp_list['revenue'] = int(salesRevDf.get_group(SalesPerson).Amount.sum())
                rev_sales.append(temp_list)

        #  Product chart data
            rev_product = []

            productRevDf = data_input.groupby('Year').get_group(year).groupby('Coa_Class').get_group(coa_rev).groupby(
                'Month').get_group(month).groupby('Product')

            for Product, revbyproduct in productRevDf:
                temp_list = {'Product': '', 'Revenue': ''}
                temp_list['Product'] = Product
                temp_list['Revenue'] = int(productRevDf.get_group(Product).Amount.sum())
                rev_product.append(temp_list)


            data = {
                'rev_cust': rev_cust,
                'rev_sales': rev_sales,
                'rev_product': rev_product
            }

            return JsonResponse(data)
#  ////////////////////////////////////////// CUSTOMER SUB-DASHBOARD VIEW //////////////////////////////////////////
        elif identifier == 'customer':
            customer = request.GET.get('id')

        #  Yearly chart data
            rev_yearly = []

            yearlyRevDf = data_input.groupby('Year').get_group(year).groupby('Coa_Class').get_group(coa_rev).groupby(
                'Customer').get_group(customer).groupby('Month')

            for Month, revbycustomer in yearlyRevDf:
                temp_list = {'month': '', 'revenue': ''}
                temp_list['month'] = Month
                temp_list['revenue'] = int(yearlyRevDf.get_group(Month).Amount.sum())
                rev_yearly.append(temp_list)

        #  Salesperson chart data
            rev_sales = []

            salesRevDf = data_input.groupby('Year').get_group(year).groupby('Coa_Class').get_group(coa_rev).groupby(
                'Customer').get_group(customer).groupby('SalesPerson')

            for SalesPerson, revbysalesperson in salesRevDf:
                temp_list = {'salesperson': '', 'revenue': ''}
                temp_list['salesperson'] = SalesPerson
                temp_list['revenue'] = int(salesRevDf.get_group(SalesPerson).Amount.sum())
                rev_sales.append(temp_list)

        #  Product chart data
            rev_product = []

            productRevDf = data_input.groupby('Year').get_group(year).groupby('Coa_Class').get_group(coa_rev).groupby(
                'Customer').get_group(customer).groupby('Product')

            for Product, revbyproduct in productRevDf:
                temp_list = {'Product': '', 'Revenue': ''}
                temp_list['Product'] = Product
                temp_list['Revenue'] = int(productRevDf.get_group(Product).Amount.sum())
                rev_product.append(temp_list)


            data = {
                'rev_yearly': rev_yearly,
                'rev_sales': rev_sales,
                'rev_product': rev_product
            }

            return JsonResponse(data)



        elif identifier == 'salesperson':
            salesperson = request.GET.get('id')

        #  Yearly chart data
            rev_yearly = []

            yearlyRevDf = data_input.groupby('Year').get_group(year).groupby('Coa_Class').get_group(coa_rev).groupby(
                'SalesPerson').get_group(salesperson).groupby('Month')

            for Month, revbysalesperson in yearlyRevDf:
                temp_list = {'month': '', 'revenue': ''}
                temp_list['month'] = Month
                temp_list['revenue'] = int(yearlyRevDf.get_group(Month).Amount.sum())
                rev_yearly.append(temp_list)

        #  Customer chart data
            rev_cust = []

            customerRevDf = data_input.groupby('Year').get_group(year).groupby('Coa_Class').get_group(
                coa_rev).groupby('SalesPerson').get_group(salesperson).groupby('Customer')

            for Customer, revbycustomer in customerRevDf:
                temp_list = {'Customer': '', 'Revenue': ''}
                temp_list['Customer'] = Customer
                temp_list['Revenue'] = int(customerRevDf.get_group(Customer).Amount.sum())
                rev_cust.append(temp_list)

        #  Product chart data
            rev_product = []

            productRevDf = data_input.groupby('Year').get_group(year).groupby('Coa_Class').get_group(coa_rev).groupby(
                'SalesPerson').get_group(salesperson).groupby('Product')

            for Product, revbyproduct in productRevDf:
                temp_list = {'Product': '', 'Revenue': ''}
                temp_list['Product'] = Product
                temp_list['Revenue'] = int(productRevDf.get_group(Product).Amount.sum())
                rev_product.append(temp_list)

            data = {
                'rev_yearly': rev_yearly,
                'rev_cust': rev_cust,
                'rev_product': rev_product
            }

            return JsonResponse(data)

        elif identifier == 'product':
            product = request.GET.get('id')

        #  Yearly chart data
            rev_yearly = []

            yearlyRevDf = data_input.groupby('Year').get_group(year).groupby('Coa_Class').get_group(coa_rev).groupby(
                'Product').get_group(product).groupby('Month')

            for Month, revbysalesperson in yearlyRevDf:
                temp_list = {'month': '', 'revenue': ''}
                temp_list['month'] = Month
                temp_list['revenue'] = int(yearlyRevDf.get_group(Month).Amount.sum())
                rev_yearly.append(temp_list)

        #  Customer chart data
            rev_cust = []

            customerRevDf = data_input.groupby('Year').get_group(year).groupby('Coa_Class').get_group(coa_rev).groupby(
                'Product').get_group(product).groupby('Customer')

            for Customer, revbycustomer in customerRevDf:
                temp_list = {'Customer': '', 'Revenue': ''}
                temp_list['Customer'] = Customer
                temp_list['Revenue'] = int(customerRevDf.get_group(Customer).Amount.sum())
                rev_cust.append(temp_list)

        #  Salesperson chart data
            rev_sales = []

            salesRevDf = data_input.groupby('Year').get_group(year).groupby('Coa_Class').get_group(coa_rev).groupby(
                'Product').get_group(product).groupby('SalesPerson')

            for SalesPerson, revbysalesperson in salesRevDf:
                temp_list = {'salesperson': '', 'revenue': ''}
                temp_list['salesperson'] = SalesPerson
                temp_list['revenue'] = int(salesRevDf.get_group(SalesPerson).Amount.sum())
                rev_sales.append(temp_list)

            data = {
                'rev_yearly': rev_yearly,
                'rev_cust': rev_cust,
                'rev_sales': rev_sales
            }
            return JsonResponse(data)
















#  TEST DASHBOARD VIEWS

def get_revenue_by_customer(request, *args, **kwargs):
    combined_list = []

    for Customer, revenue in summary:
        temp_list = {'customer': '', 'revenue': ''}
        temp_list['customer'] = Customer
        temp_list['revenue'] = int((summary.get_group(Customer).Revenue.sum()))
        combined_list.append(temp_list)

    data = {
        'combined_list': combined_list
    }

    return JsonResponse(data)


def get_revenue_by_product(request, *args, **kwargs):
    if request.method == 'GET':
        customer = request.GET.get('customer', None)

    byproductrevenue = summary.get_group(customer)[['Product', 'Revenue']].groupby('Product')
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

    data = {
        'rev_by_prod': rev_by_prod,
        'product': product,
        'revenue': revenue
    }

    return JsonResponse(data)

'''
def get_data1(request, *args, **kwargs):
    orders = pd.read_csv('dashboard/reports/pandas.csv')
    customer_list = []
    revenue_list = []
    revenue_library = {}
    summary = orders.groupby('Customer')
    for Customer, revenue in summary:
        revenue_library[Customer] = summary.get_group(Customer).Revenue.sum()
        customer_list.append(Customer)
        revenue_list.append(int(summary.get_group(Customer).Revenue.sum()))

    data = {
        'customer': customer_list,
        'revenue': revenue_list
    }

    return JsonResponse(data)


'''