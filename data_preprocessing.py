import pandas as pd

# Load the career dataset
data = pd.read_csv("../data/career_data.csv")
# Display the first 5 rows
print("Career Dataset:")
print(data.head())

# Display the available job roles
print("\nJob Roles:")
print(data["Job_Role"].unique())

# Display the number of records
print("\nNumber of Records:", len(data))