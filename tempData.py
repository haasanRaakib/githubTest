import os
import pandas as pd

# Path to the folder containing the CSV files
folder_path = "D:/IDM/temperature_data"  # Ensure this points to your folder

# Initialize data structures
yearly_results = {}
station_yearly_ranges = {}
station_avg_temps = {}

# Define season
season_mapping = {
    12: "Summer", 1: "Summer", 2: "Summer",
    3: "Autumn", 4: "Autumn", 5: "Autumn",
    6: "Winter", 7: "Winter", 8: "Winter",
    9: "Spring", 10: "Spring", 11: "Spring"
}

# Process each file in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".csv"):
        try:
            # Extract year from the file name (e.g., stations_group_1986.csv)
            year = int(file_name.split("_")[-1].split(".")[0])  # Extracts '1986'
        except ValueError:
            print(f"Skipping file: {file_name} (invalid year format)")
            continue

        # Read the CSV file
        file_path = os.path.join(folder_path, file_name)
        data = pd.read_csv(file_path)

        # Initialize yearly data structure
        if year not in yearly_results:
            yearly_results[year] = {"Summer": {'sum': 0, 'count': 0},
                                    "Autumn": {'sum': 0, 'count': 0},
                                    "Winter": {'sum': 0, 'count': 0},
                                    "Spring": {'sum': 0, 'count': 0}}
        
        for _, row in data.iterrows():
            station_name = row['STATION_NAME']

            # Initialize station-year data structure
            if (station_name, year) not in station_yearly_ranges:
                station_yearly_ranges[(station_name, year)] = {"min_temp": float("inf"), "max_temp": float("-inf")}
            
            # Update seasonal and temperature range data
            for month in range(1, 13):
                temp = row.iloc[3 + month]
                season = season_mapping[month]

                # Update yearly seasonal data
                yearly_results[year][season]['sum'] += temp
                yearly_results[year][season]['count'] += 1

                # Update min/max for station's yearly temperature range
                station_yearly_ranges[(station_name, year)]["min_temp"] = min(
                    station_yearly_ranges[(station_name, year)]["min_temp"], temp)
                station_yearly_ranges[(station_name, year)]["max_temp"] = max(
                    station_yearly_ranges[(station_name, year)]["max_temp"], temp)

            # Update overall average temperature for station
            if station_name not in station_avg_temps:
                station_avg_temps[station_name] = {"sum": 0, "count": 0}
            station_avg_temps[station_name]["sum"] += row.iloc[4:16].sum()  # All monthly temps
            station_avg_temps[station_name]["count"] += 12  # Count 12 months per row

# Calculate seasonal averages and temperature ranges
yearly_seasonal_averages = {
    year: {season: (data['sum'] / data['count']) if data['count'] > 0 else None
           for season, data in seasons.items()}
    for year, seasons in yearly_results.items()
}

station_yearly_ranges = {
    (station, year): data["max_temp"] - data["min_temp"]
    for (station, year), data in station_yearly_ranges.items()
}

# largest temperature range per year
largest_temp_range_by_year = {}
for (station, year), temp_range in station_yearly_ranges.items():
    if year not in largest_temp_range_by_year or temp_range > largest_temp_range_by_year[year][1]:
        largest_temp_range_by_year[year] = (station, temp_range)

# warmest and coolest stations
station_avg_temps = {station: data["sum"] / data["count"] for station, data in station_avg_temps.items()}
warmest_temp = max(station_avg_temps.values())
coolest_temp = min(station_avg_temps.values())
warmest_stations = [station for station, avg_temp in station_avg_temps.items() if avg_temp == warmest_temp]
coolest_stations = [station for station, avg_temp in station_avg_temps.items() if avg_temp == coolest_temp]

# Save results
with open("D:/IDM/average_temp.txt", "w") as f:
    f.write("Yearly Seasonal Averages:\n")
    for year, seasons in yearly_seasonal_averages.items():
        f.write(f"\nYear: {year}\n")
        for season, avg_temp in seasons.items():
            f.write(f"  {season}: {avg_temp:.2f}°C\n" if avg_temp is not None else f"  {season}: No Data\n")

with open("D:/IDM/largest_temp_range_station.txt", "w") as f:
    f.write("Stations with the Largest Temperature Range per Year:\n")
    for year, (station, temp_range) in largest_temp_range_by_year.items():
        f.write(f"Year {year}: {station} with range {temp_range:.2f}°C\n")

with open("D:/IDM/warmest_and_coolest_station.txt", "w") as f:
    f.write("Warmest Stations:\n")
    for station in warmest_stations:
        f.write(f"{station}: {warmest_temp:.2f}°C\n")
    f.write("\nCoolest Stations:\n")
    for station in coolest_stations:
        f.write(f"{station}: {coolest_temp:.2f}°C\n")

# print instruction if the analysis is complete
print("Analysis complete. Results saved to files.")
