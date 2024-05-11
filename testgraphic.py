import matplotlib.pyplot as plt
import json

# Load data from JSON file
with open('results.json', 'r') as file:
    results = json.load(file)

# Extract the labels and sizes
labels = list(results.keys())
sizes = [float(result[:-1]) for result in results.values()]  # Remove the '%' and convert to float

# Create the pie chart
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()
