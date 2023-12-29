from aeropost_form import read_and_extract_data, manifest_form,perform_calculation
from flask import Flask, render_template, request


 
# Calculate INSURANCE charges based on TOTAL PRODUCT PRICE
    insurance_rates = {(1, 99.99): 1.95, (100, 159.99): 3.90, (160, 199.99): 3.96, (200, 299.99): 6.10,
                       (300, 399.99): 8.54, (400, 499.99): 10.67, (500, 599.99): 12.80, (600, 699.99): 14.94,
                       (700, 799.99): 17.07, (800, 899.99): 19.21, (900, 999.99): 21.34, (1000, 1099.99): 23.48,
                       (1100, 1199.99): 25.61, (1200, 1299.99): 27.74, (1300, 1399.99): 29.88, (1400, 1499.99): 32.01,
                       (1500, float('inf')): 45.76}

        weight_itm = "" #per item weight
        freight_itm = "" #per item freight
        insurance_itm = "" #per item insurance


        cost_con = ""
        weight_con = "" #per consolidated weight // sum of all items weight
        freight_con = "" #per consolidated freight
        insurance_con = "" #per consolidated insurance
        billNum_con = "" # ABBEY(consignee)-101PM(++)-7123(bill number)
        content_con = ""# billNum + consignee + contents


        cost_tot = "" # sum of all costs
        weight_tot = "" #total gross weight // fill by user
        freight_tot = "" #total gross freight // sum of all freight
        insurance_tot = "" #total gross insurance // sum of all insurance


