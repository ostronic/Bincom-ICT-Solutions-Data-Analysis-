#!/usr/bin/env python3
#  Bincom ICT Solutions.
#  Python Basic Developer Test
#
#  This script analyzes T-shirt color data scraped from an HTML file,
#  performs statistical calculations, and includes several algorithmic solutions.

import random
from collections import Counter
import numpy as np
from bs4 import BeautifulSoup
import psycopg2
import json
import sys
from pathlib import Path

#TODO: --- Part 1: Data Scraping and Analysis ---

def get_html_file_path():
    """
    Prompts the user for a file path and validates it using pathlib.

    Returns:
        pathlib.Path: A validated path object to an existing .html file.
    """
    while True:
        try:
            input_path = input("Enter the path to the HTML file (e.g., python_class_question.html): ")
            # Create a Path object for robust path handling
            file_path = Path(input_path)

            # 1. Check if the path exists and is a file
            if not file_path.is_file():
                print(f"Error: The file '{file_path}' does not exist. Please try again.")
                continue

            # 2. Check if the file has a .html extension
            if file_path.suffix.lower() != '.html':
                print(f"Error: The file must have an '.html' extension. You provided: '{file_path.suffix}'")
                continue

            # If all checks pass, return the valid path
            return file_path

        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")


def scrape_color_data(file_path):
    """
    Scrapes color data from the provided HTML file.

    Args:
        file_path (pathlib.Path): The path object for the HTML file.

    Returns:
        list: A list of all color strings, or exits the script on error.
    """
    try:
        with file_path.open('r', encoding='utf-8') as f:
            contents = f.read()

        soup = BeautifulSoup(contents, 'html.parser')

        if not soup.find('table'):
            print(f"Error: No '<table>' element found in '{file_path}'. Cannot scrape data.")
            sys.exit(1)

        rows = soup.find('table').find_all('tr')
        all_colors = []
        for row in rows[1:]: # Skip header row
            cells = row.find_all('td')
            if len(cells) > 1:
                color_data = cells[1].text
                colors = [color.strip().upper() for color in color_data.split(',')]
                all_colors.extend(colors)

        return [color for color in all_colors if color] # Filter out empty strings

    except Exception as e:
        print(f"Error reading or parsing the file '{file_path}': {e}")
        sys.exit(1)


def analyze_colors(colors):
    """
    Performs statistical analysis on the list of colors.
    """
    if not colors:
        print("No colors found in the HTML file to analyze.")
        return

    print("\n--- T-Shirt Color Analysis ---")

    color_counts = Counter(colors)

    # 1. Mean (Most Frequent) Color
    mean_color = color_counts.most_common(1)[0][0]
    print(f"1. Mean (Most Frequent) Color: {mean_color}")

    # 2. Most Worn Color
    print(f"2. Most Worn Color: {mean_color}")

    # 3. Median Color
    sorted_colors = sorted(colors)
    n_colors = len(sorted_colors)
    if n_colors % 2 == 0:
        median_index1 = n_colors // 2 - 1
        median_index2 = n_colors // 2
        median_color = f"{sorted_colors[median_index1]} and {sorted_colors[median_index2]}"
    else:
        median_color = sorted_colors[n_colors // 2]
    print(f"3. Median Color (alphabetically sorted): {median_color}")

    # 4. Variance of Color Frequencies
    frequencies = list(color_counts.values())
    variance = np.var(frequencies)
    print(f"4. Variance of Color Frequencies: {variance:.2f}")

    # 5. Probability of choosing RED
    red_count = color_counts.get('RED', 0)
    total_colors = len(colors)
    prob_red = (red_count / total_colors) if total_colors > 0 else 0
    print(f"5. Probability of choosing RED: {prob_red:.2f} or {prob_red:.2%}")

    # 6. Save to PostgreSQL
    save_to_postgres(color_counts)

def load_db_config(config_file='db_config.json'):
    """Loads database configuration from a JSON file."""
    config_path = Path(config_file)
    if not config_path.is_file():
        print(f"\nError: Database config file '{config_file}' not found.")
        print("Please create it with your database credentials.")
        return None
    with config_path.open('r') as f:
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
        print("   -> Please check credentials in 'db_config.json' and that the database is running.")
        pass
    except Exception as e:
        print(f"   -> An unexpected error occurred: {e}")
        pass


#TODO: --- Part 2: Algorithmic Questions ---

def recursive_search(arr, target, index=0):
    """Recursively searches for a target value in a list."""
    if index >= len(arr): return -1
    if arr[index] == target: return index
    return recursive_search(arr, target, index + 1)

def generate_and_convert_binary():
    """Generates a random 4-digit binary number and converts it to decimal."""
    binary_number = "".join(random.choice('01') for _ in range(4))
    decimal_number = int(binary_number, 2)
    return binary_number, decimal_number

def sum_fibonacci(n):
    """Calculates the sum of the first n Fibonacci numbers."""
    if n <= 0: return 0
    a, b, fib_sum = 0, 1, 0
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
    html_file_path = get_html_file_path()
    shirt_colors = scrape_color_data(html_file_path)
    if shirt_colors:
        analyze_colors(shirt_colors)

    # Part 2: Run algorithms
    run_algorithms()
