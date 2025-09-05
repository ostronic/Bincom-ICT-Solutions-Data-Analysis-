#!/usr/bin/env python3
#  Bincom ICT Solutions.
#  Python Basic Developer Test
#
#  This script analyzes T-shirt color data scraped from an HTML file,
#  performs statistical calculations, and includes several algorithmic solutions.


from bs4 import BeautifulSoup
from collections import Counter

import json
import numpy as np
import os
import psycopg2
import random
import sys

#TODO: --- Part 1: Data Scraping and Analysis ---

def scrape_color_data(file_path):
    """
    Scrapes color data from the provided HTML file.

    Args:
        file_path (str): The path to the HTML file.

    Returns:
        list: A list of all color strings, or exits the script if the file is not found.
    """
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(1) # Exit the script if the file doesn't exist

    with open(file_path, 'r', encoding='utf-8') as f:
        contents = f.read()

    soup = BeautifulSoup(contents, 'html.parser')

    if not soup.find('table'):
        print(f"Error: No '<table>' element found in '{file_path}'. Cannot scrape data.")
        sys.exit(1)

    rows = soup.find('table').find_all('tr')
    all_colors = []
    # Iterate through each row in the table, skipping the header
    for row in rows[1:]:
        cells = row.find_all('td')
        if len(cells) > 1:
            # The second 'td' element should contain the comma-separated colors
            color_data = cells[1].text
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
        print("No colors found in the HTML file to analyze.")
        return

    print("--- T-Shirt Color Analysis ---")

    color_counts = Counter(colors)

    #TODO: 1. Which color of shirt is the mean color?
    mean_color = color_counts.most_common(1)[0][0]
    print(f"1. Mean (Most Frequent) Color: {mean_color}")

    #TODO: 2. Which color is mostly worn throughout the week?
    print(f"2. Most Worn Color: {mean_color}")

    #TODO: 3. Which color is the median?
    sorted_colors = sorted(colors)
    n_colors = len(sorted_colors)
    if n_colors % 2 == 0:
        median_index1 = n_colors // 2 - 1
        median_index2 = n_colors // 2
        median_color = f"{sorted_colors[median_index1]} and {sorted_colors[median_index2]}"
    else:
        median_color = sorted_colors[n_colors // 2]
    print(f"3. Median Color (alphabetically sorted): {median_color}")

    #TODO: 4. Get the variance of the colors
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

def load_db_config(config_file='db_config.json'):
    """Loads database configuration from a JSON file."""
    if not os.path.exists(config_file):
        print(f"\nError: Database config file '{config_file}' not found.")
        print("Please create it with your database credentials (see db_config.json.template).")
        return None
    with open(config_file, 'r') as f:
        return json.load(f)

def save_to_postgres(color_counts):
    """
    Saves the color frequencies to a PostgreSQL database using external credentials.
    """
    print("\n--- PostgreSQL Database ---")

    db_config = load_db_config()
    if not db_config:
        print("   -> Skipping database operation.")
        return

    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS bincom_color_frequencies (
                id SERIAL PRIMARY KEY,
                color VARCHAR(50) UNIQUE NOT NULL,
                frequency INTEGER NOT NULL
            );
        """)

        print("6. Inserting/Updating color frequencies in the database...")
        for color, freq in color_counts.items():
            cur.execute("""
                INSERT INTO bincom_color_frequencies (color, frequency)
                VALUES (%s, %s)
                ON CONFLICT (color) DO UPDATE
                SET frequency = EXCLUDED.frequency;
            """, (color, freq))

        conn.commit()
        print("   -> Data saved to PostgreSQL successfully.")
        cur.close()
        conn.close()

    except psycopg2.OperationalError as e:
        print(f"   -> Could not connect to PostgreSQL: {e}")
        print("   -> Please check your credentials in 'db_config.json' and ensure the database is running.")
        pass
    except Exception as e:
        print(f"   -> An unexpected error occurred: {e}")
        pass

#TODO: --- Part 2: Algorithmic Questions ---

def recursive_search(arr, target, index=0):
    """Recursively searches for a target value in a list."""
    if index >= len(arr):
        return -1
    if arr[index] == target:
        return index
    return recursive_search(arr, target, index + 1)

def generate_and_convert_binary():
    """Generates a random 4-digit binary number and converts it to decimal."""
    binary_digits = [str(random.randint(0, 1)) for _ in range(4)]
    binary_number = "".join(binary_digits)
    decimal_number = int(binary_number, 2)
    return binary_number, decimal_number

def sum_fibonacci(n):
    """Calculates the sum of the first n Fibonacci numbers."""
    if n <= 0:
        return 0
    a, b = 0, 1
    fib_sum = 0
    for _ in range(n):
        fib_sum += a
        a, b = b, a + b
    return fib_sum

def run_algorithms():
    """Runs the algorithmic questions and prints their results."""
    print("\n--- Algorithmic Questions ---")

    # 7. Recursive search
    print("7. Recursive Search:")
    search_list = [10, 25, 8, 42, 15, 30, 5]
    try:
        target_input = input(f"   Enter a number to search for in the list {search_list}: ")
        target_num = int(target_input)
        result_index = recursive_search(search_list, target_num)
        if result_index != -1:
            print(f"   -> Found at index: {result_index}")
        else:
            print(f"   -> {target_num} was not found.")
    except ValueError:
        print("   -> Invalid input. Please enter an integer.")

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
    # Part 1: Get user input for file and run analysis
    html_file = input("Enter the path to the HTML file (e.g., python_class_question.html): ")
    shirt_colors = scrape_color_data(html_file)
    if shirt_colors:
        analyze_colors(shirt_colors)

    # Part 2: Run algorithms
    run_algorithms()
