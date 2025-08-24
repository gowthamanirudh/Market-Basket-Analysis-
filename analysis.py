import os
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# --- Step 1: Load and Inspect Data ---

# Define the path to the dataset, making it relative to the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'Online Retail.xlsx')

print("--- Attempting to load the dataset... ---")

# Load the Excel file into a pandas DataFrame
try:
    df = pd.read_excel(file_path, engine='openpyxl')
    print("--- Dataset loaded successfully! ---")

    # --- Step 2: Clean the Data ---

    print("\n--- Starting Data Cleaning... ---")
    df.dropna(subset=['CustomerID', 'Description'], inplace=True)
    df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
    df = df[df['Quantity'] > 0]
    df['Description'] = df['Description'].str.strip()
    df['CustomerID'] = df['CustomerID'].astype(int)
    print("--- Data Cleaning Complete! ---")

    # --- Step 3: Transform the Data ---
    print("\n--- Starting Data Transformation... ---")

    basket = (df[df['Country'] == "United Kingdom"]
              .groupby(['InvoiceNo', 'Description'])['Quantity']
              .sum().unstack().reset_index().fillna(0)
              .set_index('InvoiceNo'))

    def encode_units(x):
        if x <= 0:
            return 0
        if x >= 1:
            return 1

    basket_sets = basket.map(encode_units)
    
    if 'POSTAGE' in basket_sets.columns:
        basket_sets.drop('POSTAGE', inplace=True, axis=1)

    print("--- Data Transformation Complete! ---")

    # --- Step 4: Find Frequent Itemsets and Association Rules ---
    print("\n--- Generating Frequent Itemsets... ---")

    # Generate frequent itemsets with a minimum support of 2%
    frequent_itemsets = apriori(basket_sets, min_support=0.02, use_colnames=True)

    print("--- Generating Association Rules... ---")
    # Generate the rules with a minimum lift of 1
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

    # Sort the rules by lift in descending order
    rules = rules.sort_values(by='lift', ascending=False)

    print("\n--- Top Association Rules Found: ---")
    print(rules.head(10))

    # --- Step 5: Save the Results ---
    output_path = os.path.join(script_dir, 'association_rules.csv')
    rules.to_csv(output_path, index=False)
    print(f"\n--- Association rules saved to {output_path} ---")

    # --- Project Complete ---
    print("\n--- Analysis Complete. ---")

except FileNotFoundError:
    print(f"Error: The file was not found at {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")