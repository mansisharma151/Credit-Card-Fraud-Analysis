import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("creditcard.csv")

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())

print("\nColumn names:")
print(df.columns.tolist())

# Count genuine and fraudulent transactions
print("\nTransaction Class Counts:")
print(df["Class"].value_counts().rename(
    index={0: "Genuine", 1: "Fraud"}
))

# Calculate percentages
print("\nTransaction Percentages:")
print(
    (df["Class"].value_counts(normalize=True) * 100)
    .rename(index={0: "Genuine", 1: "Fraud"})
    .round(4)
)

# Visualize transaction counts
class_counts = df["Class"].value_counts().sort_index()

plt.figure(figsize=(7, 5))
plt.bar(
    ["Genuine", "Fraud"],
    class_counts.values
)
plt.title("Genuine vs Fraudulent Transactions")
plt.xlabel("Transaction Type")
plt.ylabel("Number of Transactions")
plt.tight_layout()
plt.savefig("transaction_counts.png")
plt.show()

# Average transaction amount by class
print("\nAverage Transaction Amount:")

amount_analysis = df.groupby("Class")["Amount"].agg(
    ["count", "mean", "median", "min", "max"]
)

amount_analysis.index = ["Genuine", "Fraud"]
print(amount_analysis.round(2))

# Compare average transaction amounts
average_amounts = df.groupby("Class")["Amount"].mean()

plt.figure(figsize=(7, 5))
plt.bar(
    ["Genuine", "Fraud"],
    average_amounts.values
)
plt.title("Average Transaction Amount: Genuine vs Fraud")
plt.xlabel("Transaction Type")
plt.ylabel("Average Amount")
plt.tight_layout()
plt.savefig("average_transaction_amount.png")
plt.show()


# Divide elapsed time into 2-hour intervals
df["Time_Interval"] = (df["Time"] // 7200).astype(int)

time_analysis = df.groupby("Time_Interval").agg(
    Total_Transactions=("Class", "size"),
    Fraud_Count=("Class", "sum")
)

time_analysis["Fraud_Rate_Percent"] = (
    time_analysis["Fraud_Count"]
    / time_analysis["Total_Transactions"] * 100
).round(4)

print("\nFraud Rate by Time Interval:")
print(time_analysis)

plt.figure(figsize=(10, 5))
plt.bar(
    time_analysis.index,
    time_analysis["Fraud_Rate_Percent"]
)
plt.title("Fraud Rate by 2-Hour Time Interval")
plt.xlabel("Elapsed Time Interval")
plt.ylabel("Fraud Rate (%)")
plt.tight_layout()
plt.savefig("fraud_rate_by_time.png")
plt.show()

# Step 13: Key Business Insights

total_transactions = len(df)
fraud_transactions = (df["Class"] == 1).sum()
genuine_transactions = (df["Class"] == 0).sum()
total_fraud_amount = df.loc[df["Class"] == 1, "Amount"].sum()
average_fraud_amount = df.loc[df["Class"] == 1, "Amount"].mean()
fraud_percentage = (fraud_transactions / total_transactions) * 100

print("\n========== KEY PROJECT INSIGHTS ==========")
print(f"Total Transactions: {total_transactions:,}")
print(f"Genuine Transactions: {genuine_transactions:,}")
print(f"Fraudulent Transactions: {fraud_transactions:,}")
print(f"Fraud Rate: {fraud_percentage:.4f}%")
print(f"Total Amount in Fraud Transactions: {total_fraud_amount:,.2f}")
print(f"Average Fraud Transaction Amount: {average_fraud_amount:,.2f}")

# Save cleaned analysis data for Power BI
df.to_csv("creditcard_analysis.csv", index=False)

print("\nPower BI dataset exported successfully!")
