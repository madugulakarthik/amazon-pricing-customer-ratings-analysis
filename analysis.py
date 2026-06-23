
## Improt libraries
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt 

## load data
df = pd.read_excel("Amazon_sales_data.xlsm")
pd.set_option("display.max_column",None)
pd.set_option("display.width", 1000)


## data validation 
df["calculated_discount_price"] = df["actual_price"] * (1 - df["discount_percentage"])

df["difference"] = df["discounted_price"] - df["calculated_discount_price"]

print("\nData validation check :")
print(df[["actual_price","discount_percentage","discounted_price","calculated_discount_price","difference"]].head()) 

print("\nNumber of mismatches :")
print((abs(df["difference"]) > 1).sum())

## Average difference

df["abs_difference"] = abs(df["difference"])
avg_abs_diff = df["abs_difference"].mean()

print(f"Average absolute differemce: {avg_abs_diff:.2f}")
print("Minimum difference:", df['abs_difference'].min())
print("Max difference:", df['abs_difference'].max())

print("\nTop 5 highest differences")

top5 = df.sort_values(by='abs_difference', ascending=False).head()

top5_display = top5.copy()
top5_display['short_name'] = top5_display['product_name'].str[:40] + "..."

print(top5_display[['short_name','actual_price','discounted_price','abs_difference']].to_string(index=False))

## First model (discount% vs rating)

print("Model 1: discount% vs rating")

x = df[["discount_percentage"]]
y = df["rating"]

model = LinearRegression()
model.fit(x,y)

y_pred = model.predict(x)

plt.scatter(x,y)
plt.plot(x,y_pred)
plt.xlabel("Discount Percentage")
plt.ylabel("Rating")
plt.title("Prediction: Discount vs Rating")
plt.savefig("prediction_plot.png")
print("Graph saved as prediction_plot.png")

## second model (price vs rating)

print("\nModel 2: price vs rating ")

x_price = df[["discounted_price"]]
y_price = df["rating"]

model_price = LinearRegression()
model_price.fit(x_price,y_price)

y_pred_price = model_price.predict(x_price)

plt.figure()

plt.scatter(x_price,y_price)
plt.plot(x_price,y_pred_price)

plt.xlabel("discounted price")
plt.ylabel("rating")
plt.title("prediction : price vs rating")

plt.savefig("price_vs_rating.png")
print("price vs rating graph saved")

## third model (multiple regression)

print("\nModel 3: multiple regression (price + discount)")

x_multi = df[["discount_percentage" , "discounted_price"]]
y_multi = df["rating"]

model_multi = LinearRegression()
model_multi.fit(x_multi,y_multi)

y_pred_multi = model_multi.predict(x_multi)

coeff = [float(c) for c in model_multi.coef_]

print("Intercept:", f"{model_multi.intercept_:.2f}")
print("Coefficients:", ", ".join(f"{c:.6f}" for c in coeff))
