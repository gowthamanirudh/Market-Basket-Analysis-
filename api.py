import pandas as pd
from fastapi import FastAPI

app = FastAPI(
    title="Market Basket Analysis API",
    description="An API to serve association rules for market basket analysis.",
    version="1.0.0"
)

@app.get("/rules", tags=["Association Rules"])
def get_association_rules():
    """
    Reads the generated association rules from the `association_rules.csv` file 
    and returns them as a JSON response.
    """
    try:
        # Load the rules from the CSV file
        rules_df = pd.read_csv("association_rules.csv")
        # Convert the DataFrame to a list of dictionaries for the JSON response
        return rules_df.to_dict(orient="records")
    except FileNotFoundError:
        return {"error": "The `association_rules.csv` file was not found. Please run the analysis script first."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
