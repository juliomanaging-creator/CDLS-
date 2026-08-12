import os
import json
from datetime import datetime
import pandas as pd

class DealJacketManager:
    def __init__(self, dealer_name="My Dealership"):
        self.jacket_directory = 'deal_jackets'
        os.makedirs(self.jacket_directory, exist_ok=True)
        self.jackets = {}
        self._load_existing_jackets()

    def _load_existing_jackets(self):
        """Loads all local .json jackets into memory for the dashboard."""
        for filename in os.listdir(self.jacket_directory):
            if filename.endswith('.json'):
                with open(os.path.join(self.jacket_directory, filename), 'r') as f:
                    data = json.load(f)
                    self.jackets[data['vin']] = data

    def export_to_accounting_csv(self, filename="salsa_cost_report.csv"):
        """Compiles all local jackets into the Emerald Accountant Export format."""
        data = []
        for vin, jacket in self.jackets.items():
            totals = jacket.get('totals', {})
            data.append({
                'VIN': vin,
                'Vehicle': f"{jacket['vehicle']['year']} {jacket['vehicle']['make']}",
                'Purchase_Date': jacket['purchase_date'],
                'Purchase_Price': totals.get('purchase_price', 0),
                'Auction_Fees': totals.get('auction_fees', 0),
                'Parts_Total': totals.get('parts_total', 0),
                'Labor_Total': totals.get('labor_total', 0),
                'Other_Fees': totals.get('other_total', 0),
                'Total_Investment': totals.get('total_cost', 0),
                'Status': jacket['status']
            })
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        return filename