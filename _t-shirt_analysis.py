#!/usr/bin/env python3
#:  Bincom ICT Solutions.
#:  Python Basic Developer Test
#:
#:  This script analyzes T-shirt color put on by Bincom staffs for the 
#:  week, data scraped from an HTML file,
#:  performs statistical calculations, and includes several algorithmic solutions.

import random
from collections import Counter
import numpy as np
from bs4 import BeautifulSoup
import psycopg2
import os

#TODO: --- Part 1: Data Scraping and Analysis ---

def scrape_color_data(file_path='python_class_question.html'):
    """
    Scrapes color data from the provided HTML file.

    Args:
        file_path (str): The path to the HTML file.

    Returns:
        list: A list of all color strings, or None if the file is not found.
    """
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' was not found in the current directory.")
        return None

    with open(file_path, 'r') as f:
        contents = f.read()

    soup = BeautifulSoup(contents, 'html.parser')
    rows = soup.find('table').find_all('tr')

    all_colors = []
    # Iterate through each row in the table, skipping the header
    for row in rows[1:]:
        # The second 'td' element contains the comma-separated colors(corrected the mistake BLEW instead of BLUE in your dataset)
        color_data = row.find_all('td')[1].text
        # Split the string into a list of colors and remove leading/trailing whitespace
        colors = [color.strip().upper() for color in color_data.split(',')]
        all_colors.extend(colors)

    # Filter out any potential empty strings that might result from trailing commas
    return [color for color in all_colors if color]

def analyze_colors(colors):
    """
    Performs statistical analysis on the list of colors.
    """
    if not colors:
        print("No colors to analyze.")
        return

    print("--- T-Shirt Color Analysis ---")

    color_counts = Counter(colors)

    #TODO: 1. Which color of shirt is the mean color?
    # For categorical data, the "mean" is the mode (most frequent item).
    mean_color = color_counts.most_common(1)[0][0]
    print(f"1. Mean (Most Frequent) Color: {mean_color}")

    #TODO: 2. Which color is mostly worn throughout the week?
    # This is the same as the mean/mode.
    print(f"2. Most Worn Color: {mean_color}")

    #TODO: 3. Which color is the median?
    # To find a median for categorical data, we sort the list alphabetically and find the middle element.
    sorted_colors = sorted(colors)
    n_colors = len(sorted_colors)
    if n_colors % 2 == 0:
        # If even, there are two middle elements. We can present both.
        median_index1 = n_colors // 2 - 1
        median_index2 = n_colors // 2
        median_color = f"{sorted_colors[median_index1]} and {sorted_colors[median_index2]}"
    else:
        median_color = sorted_colors[n_colors // 2]
    print(f"3. Median Color (alphabetically sorted): {median_color}")

    #TODO: 4. Get the variance of the colors
    # We calculate the variance of the frequencies of the colors.
    frequencies = list(color_counts.values())
    variance = np.var(frequencies)
    print(f"4. Variance of Color Frequencies: {variance:.2f}")

    #TODO: 5. if a color is chosen at random, what is the probability that the color is red?
    red_count = color_counts.get('RED', 0)
    total_colors = len(colors)
    prob_red = (red_count / total_colors) if total_colors > 0 else 0
    print(f"5. Probability of choosing RED: {prob_red:.2f} or {prob_red:.2%}")

    #TODO: 6. Save the colors and their frequencies in postgresql database
    save_to_postgres(color_counts)


def save_to_postgres(color_counts):
    """
    Saves the color frequencies to a PostgreSQL database.
    """
    print("\n--- PostgreSQL Database ---")
    try:
        # IMPORTANT: Replace with your actual database credentials
        conn = psycopg2.connect(
            dbname="your_db_name",
            user="your_username",
            password="your_password",
            host="127.0.0.1", # or your host
            port="5432"       # your assigned port
        )
        cur = conn.cursor()

        # Create table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS bincom_color_frequencies (
                id SERIAL PRIMARY KEY,
                color VARCHAR(50) UNIQUE NOT NULL,
                frequency INTEGER NOT NULL
            );
        """)

        print("6. Inserting/Updating color frequencies in the database...")
        # Insert or update data
        for color, freq in color_counts.items():
            cur.execute("""
                INSERT INTO bincom_color_frequencies (color, frequency)
                VALUES (%s, %s)
                ON CONFLICT (color) DO UPDATE
                SET frequency = bincom_color_frequencies.frequency + EXCLUDED.frequency;
            """, (color, freq))

        conn.commit()
        print("   -> Data saved to PostgreSQL successfully.")
        cur.close()
        conn.close()

    except  psycopg2.OperationalError:
        print("   -> Could not connect to PostgreSQL.")
        print("   -> Please check your credentials in the script and ensure the database is running.")
    except Exception as e:
        print(f"   -> An unexpected error occurred: {e}")
        pass


# --- Part 2: Algorithmic Questions ---

#TODO: 7. write a recursive searching algorithm
def recursive_search(arr, target, index=0):
    """
    Recursively searches for a target value in a list.

    Args:
        arr (list): The list to search in.
        target: The value to search for.
        index (int): The current index to check.

    Returns:
        int: The index of the target if found, otherwise -1.
    """
    # Base case: If index is out of bounds, target is not in the list
    if index >= len(arr):
        return -1
    # Base case: If the element at the current index is the target
    if arr[index] == target:
        return index
    # Recursive step: Call the function again for the next index
    return recursive_search(arr, target, index + 1)

#TODO: 8. Write a program that generates random 4 digits number of 0s and 1s and convert the generated number to base 10.
def generate_and_convert_binary():
    """
    Generates a random 4-digit binary number and converts it to decimal.

    Returns:
        tuple: The binary string and its decimal equivalent.
    """
    binary_digits = [str(random.randint(0, 1)) for _ in range(4)]
    binary_number = "".join(binary_digits)
    decimal_number = int(binary_number, 2)
    return binary_number, decimal_number

#TODO: 9. Write a program to sum the first 50 fibonacci sequence.
def sum_fibonacci(n):
    """
    Calculates the sum of the first n Fibonacci numbers.
    """
    if n <= 0:
        return 0

    a, b = 0, 1
    fib_sum = 0
    for _ in range(n):
        fib_sum += a
        a, b = b, a + b
    return fib_sum

def run_algorithms():
    """
    Runs the algorithmic questions and prints their results.
    """
    print("\n--- Algorithmic Questions ---")

    # 7. Recursive search
    print("7. Recursive Search:")
    search_list = [10, 25, 8, 42, 15, 30, 5]
    target_num = 42
    result_index = recursive_search(search_list, target_num)
    print(f"   Searching for {target_num} in {search_list}")
    if result_index != -1:
        print(f"   -> Found at index: {result_index}")
    else:
        print(f"   -> Not found.")

    # 8. Random binary number
    print("\n8. Random Binary to Decimal Conversion:")
    binary_num, decimal_num = generate_and_convert_binary()
    print(f"   Random 4-digit binary: {binary_num}")
    print(f"   -> Converted to decimal (base 10): {decimal_num}")

    # 9. Fibonacci sum
    print("\n9. Sum of the first 50 Fibonacci numbers:")
    fib_sum_50 = sum_fibonacci(50)
    print(f"   -> The sum is: {fib_sum_50}")


# --- Main Execution ---
if __name__ == "__main__":
    # Part 1
    shirt_colors = scrape_color_data()
    if shirt_colors:
        analyze_colors(shirt_colors)
    
    # Part 2
    run_algorithms()
