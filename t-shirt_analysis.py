#!/usr/bin/env python3
#:  Bincom ICT Solutions.
#:  Python Basic Developer Test
#:  Background:
#:      You have been provided with a web page showing the colors of dresses put on by Bincom staffs for the week. 
#:      We are planning to produce Tshirts for staffs and we have issues deciding the colors to be used. 
#:      We want to make our decision based on the analysis of the data presented in the web page.
#: You can use re

from bs4 import BeautifulSoup

import csv
import os
import numpy as np
import re
import sys

# Target(color) Names
colours = ['ARSH', 'RED', 'BLUE', 'CREAM', 'BROWN', 'GREEN', 'YELLOW', 'ORANGE', 'PINK', 'WHITE']

# Dataset
data = {'DAY' : ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY'], \
        'COLOURS' : ['ARSH', 'RED', 'BLUE', 'CREAM', 'BROWN', 'GREEN', 'YELLOW', 'ORANGE', 'PINK', 'WHITE']}
data_pandas = pd.DataFrame(data)
try:
    print(data_pandas)
except Exception as e:
    print(f'{e}')

# Dataset scrape from html
def table_data():
    pass

#Key Features:
#TODO: 1.      Which color of shirt is the mean color?

#TODO:  2.      Which color is mostly worn throughout the week?

#TODO:  3.      Which color is the median?

#TODO:  4.      BONUS Get the variance of the colors

#TODO:  5.      BONUS if a colour is chosen at random, what is the probability that the color is red?

#TODO:  6.      Save the colours and their frequencies in postgresql database

#TODO:  7.      BONUS write a recursive searching algorithm to search for a number entered by user in a list of numbers.

#TODO:  8.      Write a program that generates random 4 digits number of 0s and 1s and convert the generated number to base 10.

#TODO:  9.      Write a program to sum the first 50 fibonacci sequence.
