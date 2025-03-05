# Import necessary libraries
import sqlite3
import pandas as pd
from fpdf  import FPDF

# Connect to the database
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Query data from the database
cursor.execute("SELECT * FROM sales_data")
data = cursor.fetchall()

# Convert data to a pandas DataFrame
df = pd.DataFrame(data, columns=['Date', 'Product', 'Quantity', 'Price'])

# Calculate the total sales
df['Total'] = df['Quantity'] * df['Price']
total_sales = df['Total'].sum()
# Create a PDF report using FPDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Sales Report', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_table(self, df):
        self.set_font('Arial', 'B', 12)
        self.cell(40, 10, 'Date', 1)
        self.cell(40, 10, 'Product', 1)
        self.cell(30, 10, 'Quantity', 1)
        self.cell(30, 10, 'Price', 1)
        self.cell(30, 10, 'Total', 1)
        self.ln()

        self.set_font('Arial', '', 12)
        for i in range(len(df)):
            self.cell(40, 10, str(df.ilo[i, 0]), 1)
            self.cell(40, 10, df.ilo[i, 1], 1)
            self.cell(30, 10, str(df.ilo[i, 2]), 1)
            self.cell(30, 10, str(df.ilo[i, 3]), 1)
            self.cell(30, 10, str(df.ilo[i, 4]), 1)
            self.ln()

    def add_total_sales(self, total_sales):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f'Total Sales: {total_sales}', 0, 1, 'R')

# Create an instance of the PDF class
pdf = PDF()
pdf.add_page()
pdf.add_table(df)
pdf.add_total_sales(total_sales)

# Save the PDF
pdf_file = 'sales_report.pdf'
pdf.output(pdf_file)

# Close the database connection
conn.close()

print(f"Report generated and saved as {pdf_file}")
