import pandas as pd

# Load the dataset
import os

file_path = os.path.join(os.path.dirname(__file__), "charging_station.csv")
df = pd.read_csv(file_path)

# 1. Number of rows and columns
print("Dataset Shape:")
print(df.shape)

# 2. Column names
print("\nColumn Names:")
print(df.columns.tolist())

# 3. Information about columns
print("\nDataset Information:")
df.info()
print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())
print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nPower Class Distribution:")
print(df["power_class"].value_counts(dropna=False))
print("\nTop 10 Countries:")
print(df["country_code"].value_counts().head(10))
import matplotlib.pyplot as plt

# Top 10 countries by number of charging stations
top_countries = df["country_code"].value_counts().head(10)

plt.figure(figsize=(10, 6))
top_countries.plot(kind="bar")

plt.title("Top 10 Countries by EV Charging Stations")
plt.xlabel("Country")
plt.ylabel("Number of Charging Stations")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
print("\nFast DC Charging:")
print(df["is_fast_dc"].value_counts())

print("\nFast DC Charging by Country:")
fast_dc_country = df[df["is_fast_dc"] == True]["country_code"].value_counts().head(10)
print(fast_dc_country)
# Fast DC percentage by country

# Fast DC Percentage by Country

total_by_country = df["country_code"].value_counts()

fast_dc_by_country = (
    df[df["is_fast_dc"] == True]["country_code"]
    .value_counts()
)

country_analysis = pd.DataFrame({
    "Total_Stations": total_by_country,
    "Fast_DC_Stations": fast_dc_by_country
})

country_analysis["Fast_DC_Percentage"] = (
    country_analysis["Fast_DC_Stations"]
    / country_analysis["Total_Stations"] * 100
)

country_analysis = country_analysis.dropna()

print("\nCountry Charging Analysis:")
print(
    country_analysis
    .sort_values("Total_Stations", ascending=False)
    .head(15)
)
# Countries with high station count but lower fast DC percentage

gap_analysis = country_analysis[
    country_analysis["Total_Stations"] >= 1000
].copy()

gap_analysis = gap_analysis.sort_values(
    "Fast_DC_Percentage"
)

print("\nPotential Fast-Charging Gaps:")
print(
    gap_analysis[
        ["Total_Stations", "Fast_DC_Stations", "Fast_DC_Percentage"]
    ].head(15)
)
# Chart: Potential Fast-Charging Gaps

gap_chart = gap_analysis.head(10)

plt.figure(figsize=(10, 6))

gap_chart["Fast_DC_Percentage"].sort_values().plot(
    kind="barh"
)

plt.title("Countries with Lower Fast-DC Charging Share")
plt.xlabel("Fast DC Charging Percentage")
plt.ylabel("Country")

plt.tight_layout()
plt.show()
# Charging Infrastructure by Power Class

power_class_counts = df["power_class"].value_counts()

print("\nCharging Infrastructure by Power Class:")
print(power_class_counts)
# Chart: Charging Infrastructure Mix

plt.figure(figsize=(10, 6))

power_class_counts.plot(kind="bar")

plt.title("EV Charging Infrastructure by Power Class")
plt.xlabel("Power Class")
plt.ylabel("Number of Charging Stations")
plt.xticks(rotation=45, ha="right")

plt.tight_layout()
plt.show()
# AC vs DC Charging by Country

df["charging_type"] = df["power_class"].apply(
    lambda x: "DC" if "DC" in x else "AC" if "AC" in x else "Unknown"
)

ac_dc_by_country = pd.crosstab(
    df["country_code"],
    df["charging_type"]
)

ac_dc_by_country["Total"] = ac_dc_by_country.sum(axis=1)

major_countries = (
    ac_dc_by_country
    .sort_values("Total", ascending=False)
    .head(10)
)

print("\nAC vs DC Charging by Top 10 Countries:")
print(major_countries)
# Chart: AC vs DC Charging by Country

major_countries[["AC", "DC"]].plot(
    kind="bar",
    figsize=(10, 6)
)

plt.title("AC vs DC Charging Infrastructure by Country")
plt.xlabel("Country")
plt.ylabel("Number of Charging Stations")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
# Prepare cleaned dataset for MySQL

clean_df = df[
    [
        "name",
        "city",
        "state_province",
        "country_code",
        "latitude",
        "longitude",
        "ports",
        "power_kw",
        "power_class",
        "is_fast_dc"
    ]
].copy()

clean_df.to_csv(
    "ev_charging_cleaned.csv",
    index=False
)

print("\nCleaned dataset saved as ev_charging_cleaned.csv")
print("Rows:", len(clean_df))