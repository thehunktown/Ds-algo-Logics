import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

np.random.seed(42)

n_samples = 5000

years = np.random.randint(2005, 2023, size=n_samples)
car_age = 2025 - years
mileage = np.random.uniform(10, 25, size=n_samples)
engine_power = np.random.uniform(60, 200, size=n_samples)
seats = np.random.choice([4, 5, 6, 7], size=n_samples)
owner_type = np.random.choice([0, 1, 2], size=n_samples)  

price = (
    15
    + (engine_power * 0.3)
    + (mileage * 0.8)
    - (car_age * 1.5)
    - (owner_type * 2.0)
    + np.random.normal(0, 3, size=n_samples)  
)

# Create DataFrame
df = pd.DataFrame({
    'year': years,
    'mileage': mileage,
    'engine_power': engine_power,
    'seats': seats,
    'owner_type': owner_type,
    'car_age': car_age,
    'price': price
})

print("Sample Data:")
print(df.head())
