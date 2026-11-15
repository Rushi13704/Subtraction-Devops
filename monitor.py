import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset

# Reference input data
reference_data = pd.DataFrame({
    "num1": [10, 20, 30, 40, 50, 60, 70, 80],
    "num2": [2, 4, 6, 8, 10, 12, 14, 16]
})

# Current input data
current_data = pd.DataFrame({
    "num1": [100, 120, 130, 140, 150, 160, 170, 180],
    "num2": [20, 40, 60, 80, 100, 120, 140, 160]
})

# Create data drift report
report = Report([
    DataDriftPreset()
])

# Run report
result = report.run(
    reference_data=reference_data,
    current_data=current_data
)

# Save report
result.save_html("drift_report.html")

print("Data drift report generated successfully!")