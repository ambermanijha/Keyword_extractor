import pandas as pd

# Specify the file path
file_path = r'C:\Users\sooda\Desktop\DHI\webautomation_data_amazon.com_107493_353898_2024-08-23-11-13-48.csv'

# Load the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Drop all columns except 'title', 'rating', and 'price'
df = df[['title', 'rating', 'price']]

# Save the modified DataFrame to a new CSV file
new_file_path = r'C:\Users\sooda\Desktop\DHI\teddy_bear_listings_filtered.csv'
df.to_csv(new_file_path, index=False)

print(f"Filtered data saved to {new_file_path}")
