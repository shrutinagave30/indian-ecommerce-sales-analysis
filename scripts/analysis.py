import pandas as pd
import os


# =========================================================
# Step 1: Load CSV data
# =========================================================

def load_merged_data():
    file_path = os.path.join("data", "merged_orders.csv")

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            "merged_orders.csv not found in /data folder"
        )

    df = pd.read_csv(file_path)

    print("Loaded merged_orders.csv")
    print(df.head())

    return df


# =========================================================
# Step 2: Clean Date Column
# =========================================================

def clean_date(df):
    """
    Convert Order Date into datetime format.
    """

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        format="%d-%m-%Y",
        errors="coerce"
    )

    invalid_dates = df["Order Date"].isna().sum()

    if invalid_dates > 0:
        print(
            f"Warning: {invalid_dates} rows had invalid dates "
            "and were set to NaT"
        )

    print("Converted 'Order Date' to datetime format")

    return df


# =========================================================
# Step 3: Add Time Features
# =========================================================

def add_time_features(df):
    """
    Create useful time-based columns for analysis.
    """

    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["Month_Name"] = df["Order Date"].dt.strftime("%b")
    df["Quarter"] = df["Order Date"].dt.quarter
    df["Day"] = df["Order Date"].dt.day
    df["Weekday"] = df["Order Date"].dt.weekday
    df["Weekday_Name"] = df["Order Date"].dt.strftime("%A")

    print(
        "Added Year, Month, Quarter, Day, Weekday columns"
    )

    return df


# =========================================================
# Step 4: Save Cleaned File
# =========================================================

def save_clean_file(df):
    output_path = os.path.join(
        "data",
        "merged_orders_cleaned.csv"
    )

    df.to_csv(output_path, index=False)

    print(f"Saved cleaned file to {output_path}")


# =========================================================
# Step 5: Monthly Sales Analysis
# =========================================================

def monthly_sales_analysis(df):
    """
    Calculate monthly sales and profit.
    """

    monthly_df = (
        df.groupby(
            ["Year", "Month", "Month_Name"]
        )
        .agg(
            Total_Sales=("Amount", "sum"),
            Total_Profit=("Profit", "sum")
        )
        .reset_index()
        .sort_values(["Year", "Month"])
    )

    print("\nMonthly Sales Analysis:")
    print(monthly_df)

    output_path = os.path.join(
        "data",
        "monthly_sales.csv"
    )

    monthly_df.to_csv(
        output_path,
        index=False
    )

    print("Saved monthly_sales.csv to data/")

    return monthly_df


# =========================================================
# Step 6: Compare Monthly Sales with Sales Targets
# =========================================================

def compare_sales_vs_target(df):
    """
    Compare monthly sales with sales targets.

    Calculates:
    - Sales vs Target Difference
    - Target Achievement Percentage
    """

    target_path = os.path.join(
        "data",
        "Sales Target.csv"
    )

    if not os.path.exists(target_path):
        raise FileNotFoundError(
            "Sales Target.csv not found in /data folder"
        )

    targets = pd.read_csv(target_path)

    print("\nLoaded Sales Target.csv:")
    print(targets.head())

    # Convert target month into datetime
    targets["Month_Date"] = pd.to_datetime(
        targets["Month of Order Date"],
        format="%b-%y"
    )

    # Extract Year and Month
    targets["Year"] = targets["Month_Date"].dt.year
    targets["Month"] = targets["Month_Date"].dt.month

    # Merge monthly sales with targets
    merged = pd.merge(
        df,
        targets,
        on=["Year", "Month"],
        how="left"
    )

    # Calculate difference between actual sales and target
    merged["Difference"] = (
        merged["Total_Sales"] - merged["Target"]
    )

    # Calculate target achievement percentage
    merged["Achievement_pct"] = (
        merged["Total_Sales"] /
        merged["Target"]
    ) * 100

    # Arrange columns
    cols_order = [
        "Year",
        "Month",
        "Month_Name",
        "Total_Sales",
        "Total_Profit",
        "Category",
        "Target",
        "Difference",
        "Achievement_pct"
    ]

    merged = merged[
        [column for column in cols_order if column in merged.columns]
    ]

    print("\nMonthly Sales vs Target:")
    print(merged)

    output_path = os.path.join(
        "data",
        "monthly_sales_vs_target.csv"
    )

    merged.to_csv(
        output_path,
        index=False
    )

    print("Saved monthly_sales_vs_target.csv to data/")

    return merged


# =========================================================
# Step 7: Save Main Outputs
# =========================================================

def save_outputs(monthly_df, sales_vs_target_df):
    """
    Save important analysis results into outputs folder.
    """

    output_dir = "outputs"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Monthly sales
    monthly_path = os.path.join(
        output_dir,
        "monthly_sales.csv"
    )

    monthly_df.to_csv(
        monthly_path,
        index=False
    )

    print(
        f"Saved monthly sales to {monthly_path}"
    )

    # Monthly sales vs target
    target_path = os.path.join(
        output_dir,
        "monthly_sales_vs_target.csv"
    )

    sales_vs_target_df.to_csv(
        target_path,
        index=False
    )

    print(
        f"Saved monthly sales vs target to {target_path}"
    )

    print("\nAll key outputs saved successfully!")


# =========================================================
# Step 8: Top Customers
# =========================================================

def top_customers(df, top_n=10):
    """
    Identify the top customers by revenue.
    """

    top_cust = (
        df.groupby("CustomerName")["Amount"]
        .sum()
        .reset_index()
    )

    top_cust = (
        top_cust
        .sort_values(
            by="Amount",
            ascending=False
        )
        .head(top_n)
    )

    print("\nTop Customers by Revenue:")
    print(top_cust)

    output_path = os.path.join(
        "outputs",
        "top_customers.csv"
    )

    top_cust.to_csv(
        output_path,
        index=False
    )

    print(
        f"Saved top customers to {output_path}"
    )

    return top_cust


# =========================================================
# NEW: Step 8A - Customer Performance Analysis
# =========================================================

def customer_performance_analysis(df):
    """
    Analyze customer performance using:
    - Total Sales
    - Total Profit
    - Number of Orders
    - Total Quantity
    - Profit Margin
    - Sales Rank
    """

    customer_df = (
        df.groupby("CustomerName")
        .agg(
            Total_Sales=("Amount", "sum"),
            Total_Profit=("Profit", "sum"),
            Order_Count=("Order ID", "nunique"),
            Total_Quantity=("Quantity", "sum")
        )
        .reset_index()
    )

    # Calculate profit margin
    customer_df["Profit_Margin_pct"] = (
        customer_df["Total_Profit"]
        / customer_df["Total_Sales"].replace(0, pd.NA)
    ) * 100

    customer_df["Profit_Margin_pct"] = (
        customer_df["Profit_Margin_pct"].round(2)
    )

    # Rank customers by total sales
    customer_df["Sales_Rank"] = (
        customer_df["Total_Sales"]
        .rank(
            method="dense",
            ascending=False
        )
        .astype(int)
    )

    # Sort highest sales first
    customer_df = customer_df.sort_values(
        "Total_Sales",
        ascending=False
    )

    print("\nCustomer Performance Analysis:")
    print(customer_df.head(10))

    # Save output
    output_path = os.path.join(
        "outputs",
        "customer_performance.csv"
    )

    customer_df.to_csv(
        output_path,
        index=False
    )

    print(
        f"Saved customer performance -> {output_path}"
    )

    return customer_df


# =========================================================
# Step 9: Category Sales
# =========================================================

def category_sales(df):
    """
    Calculate sales and profit by category.
    """

    cat_df = (
        df.groupby("Category")[["Amount", "Profit"]]
        .sum()
        .reset_index()
    )

    cat_df = cat_df.sort_values(
        by="Amount",
        ascending=False
    )

    print("\nCategory-wise Sales & Profit:")
    print(cat_df)

    output_path = os.path.join(
        "outputs",
        "category_sales.csv"
    )

    cat_df.to_csv(
        output_path,
        index=False
    )

    print(
        f"Saved category-wise sales to {output_path}"
    )

    return cat_df


# =========================================================
# Step 10: State Sales
# =========================================================

def state_sales(df):
    """
    Calculate sales and profit by state.
    """

    state_df = (
        df.groupby("State")[["Amount", "Profit"]]
        .sum()
        .reset_index()
    )

    state_df = state_df.sort_values(
        by="Amount",
        ascending=False
    )

    print("\nState-wise Sales & Profit:")
    print(state_df)

    output_path = os.path.join(
        "outputs",
        "state_sales.csv"
    )

    state_df.to_csv(
        output_path,
        index=False
    )

    print(
        f"Saved state-wise sales to {output_path}"
    )

    return state_df


# =========================================================
# Step 11: Monthly Trends
# =========================================================

def monthly_trends(monthly_df):
    """
    Create monthly sales and profit trends.
    """

    trends_df = (
        monthly_df
        .groupby(
            ["Year", "Month", "Month_Name"]
        )[["Total_Sales", "Total_Profit"]]
        .sum()
        .reset_index()
    )

    print("\nMonthly Sales Trends:")
    print(trends_df)

    output_path = os.path.join(
        "outputs",
        "monthly_trends.csv"
    )

    trends_df.to_csv(
        output_path,
        index=False
    )

    print(
        f"Saved monthly trends to {output_path}"
    )

    return trends_df


# =========================================================
# Step 12: Category Profitability
# =========================================================

def category_profitability(df):
    """
    Calculate sales, profit, quantity and profit margin
    for each category.
    """

    cat = (
        df.groupby("Category")
        .agg(
            Total_Sales=("Amount", "sum"),
            Total_Profit=("Profit", "sum"),
            Total_Quantity=("Quantity", "sum")
        )
        .reset_index()
    )

    # Profit Margin = Profit / Sales * 100
    cat["Profit_Margin_pct"] = (
        cat["Total_Profit"] /
        cat["Total_Sales"].replace(0, pd.NA)
    ) * 100

    cat["Profit_Margin_pct"] = (
        cat["Profit_Margin_pct"].round(2)
    )

    cat = cat.sort_values(
        "Total_Profit",
        ascending=False
    )

    output_path = os.path.join(
        "outputs",
        "category_profitability.csv"
    )

    cat.to_csv(
        output_path,
        index=False
    )

    print(
        f"Saved category profitability -> {output_path}"
    )

    return cat


# =========================================================
# Step 13: State Profitability
# =========================================================

def state_profitability(df):
    """
    Calculate sales, profit, quantity and profit margin
    for each state.
    """

    st = (
        df.groupby("State")
        .agg(
            Total_Sales=("Amount", "sum"),
            Total_Profit=("Profit", "sum"),
            Total_Quantity=("Quantity", "sum")
        )
        .reset_index()
    )

    # Profit Margin = Profit / Sales * 100
    st["Profit_Margin_pct"] = (
        st["Total_Profit"] /
        st["Total_Sales"].replace(0, pd.NA)
    ) * 100

    st["Profit_Margin_pct"] = (
        st["Profit_Margin_pct"].round(2)
    )

    st = st.sort_values(
        "Total_Profit",
        ascending=False
    )

    output_path = os.path.join(
        "outputs",
        "state_profitability.csv"
    )

    st.to_csv(
        output_path,
        index=False
    )

    print(
        f"Saved state profitability -> {output_path}"
    )

    return st


# =========================================================
# Step 14: Monthly Profit Trend
# =========================================================

def monthly_profit_trend(df):
    """
    Create month-level sales and profit summary.
    """

    # Create time features if they don't already exist
    if (
        "Year" not in df.columns
        or "Month" not in df.columns
        or "Month_Name" not in df.columns
    ):

        df["Order Date"] = pd.to_datetime(
            df["Order Date"],
            errors="coerce",
            dayfirst=True
        )

        df["Year"] = df["Order Date"].dt.year
        df["Month"] = df["Order Date"].dt.month
        df["Month_Name"] = (
            df["Order Date"].dt.strftime("%b")
        )

    monthly = (
        df.groupby(
            ["Year", "Month", "Month_Name"]
        )
        .agg(
            Total_Sales=("Amount", "sum"),
            Total_Profit=("Profit", "sum")
        )
        .reset_index()
        .sort_values(["Year", "Month"])
    )

    output_path = os.path.join(
        "outputs",
        "monthly_profit_trend.csv"
    )

    monthly.to_csv(
        output_path,
        index=False
    )

    print(
        f"Saved monthly profit trend -> {output_path}"
    )

    return monthly


# =========================================================
# Step 15: Subcategory Profit Analysis
# =========================================================

def subcategory_profit(df, top_n=10):
    """
    Identify the top and bottom sub-categories by profit.
    """

    sub = (
        df.groupby("Sub-Category")
        .agg(
            Total_Sales=("Amount", "sum"),
            Total_Profit=("Profit", "sum"),
            Total_Quantity=("Quantity", "sum")
        )
        .reset_index()
    )

    # Profit margin
    sub["Profit_Margin_pct"] = (
        sub["Total_Profit"] /
        sub["Total_Sales"].replace(0, pd.NA)
    ) * 100

    sub["Profit_Margin_pct"] = (
        sub["Profit_Margin_pct"].round(2)
    )

    sub_sorted = sub.sort_values(
        "Total_Profit",
        ascending=False
    )

    top = sub_sorted.head(top_n)

    bottom = (
        sub_sorted
        .tail(top_n)
        .sort_values("Total_Profit")
    )

    output_top = os.path.join(
        "outputs",
        f"subcategory_profit_top{top_n}.csv"
    )

    output_bottom = os.path.join(
        "outputs",
        f"subcategory_profit_bottom{top_n}.csv"
    )

    top.to_csv(
        output_top,
        index=False
    )

    bottom.to_csv(
        output_bottom,
        index=False
    )

    print(
        f"Saved top {top_n} sub-categories -> {output_top}"
    )

    print(
        f"Saved bottom {top_n} sub-categories -> {output_bottom}"
    )

    return top, bottom


# =========================================================
# Step 16: Loss-Making Orders Analysis
# =========================================================

def loss_making_analysis(df):
    """
    Identify loss-making orders and analyze them
    by category.

    A loss-making order is an order where Profit < 0.
    """

    # Select orders where profit is negative
    loss_orders = df[df["Profit"] < 0].copy()

    # Overall loss metrics
    total_loss_orders = len(loss_orders)

    total_loss = loss_orders["Profit"].sum()

    loss_sales = loss_orders["Amount"].sum()

    print("\nLoss-Making Orders Analysis:")

    print(
        f"Number of loss-making orders: "
        f"{total_loss_orders}"
    )

    print(
        f"Sales from loss-making orders: "
        f"{loss_sales:.2f}"
    )

    print(
        f"Total loss: "
        f"{total_loss:.2f}"
    )

    # Analyze loss-making orders by category
    loss_by_category = (
        loss_orders
        .groupby("Category")
        .agg(
            Loss_Orders=("Order ID", "count"),
            Sales=("Amount", "sum"),
            Loss=("Profit", "sum")
        )
        .reset_index()
        .sort_values("Loss")
    )

    print("\nLoss-Making Orders by Category:")
    print(loss_by_category)

    # Save result
    output_path = os.path.join(
        "outputs",
        "loss_making_orders_by_category.csv"
    )

    loss_by_category.to_csv(
        output_path,
        index=False
    )

    print(
        f"Saved loss analysis -> {output_path}"
    )

    return loss_by_category


# =========================================================
# Main Runner
# =========================================================

if __name__ == "__main__":

    # -----------------------------------------------------
    # Load and preprocess data
    # -----------------------------------------------------

    df = load_merged_data()

    df = clean_date(df)

    df = add_time_features(df)

    save_clean_file(df)

    print(
        "\nBase preprocessing completed successfully."
    )

    # -----------------------------------------------------
    # Monthly sales analysis
    # -----------------------------------------------------

    monthly_df = monthly_sales_analysis(df)

    print(
        "\nBase preprocessing + Monthly sales completed."
    )

    # -----------------------------------------------------
    # Sales vs Target
    # -----------------------------------------------------

    sales_vs_target_df = compare_sales_vs_target(
        monthly_df
    )

    print(
        "\nMonthly sales analysis + target comparison completed."
    )

    # -----------------------------------------------------
    # Save main outputs
    # -----------------------------------------------------

    save_outputs(
        monthly_df,
        sales_vs_target_df
    )

    print(
        "\nFull analysis completed!"
    )

    # -----------------------------------------------------
    # Existing deeper analysis
    # -----------------------------------------------------

    top_customers(df)

    category_sales(df)

    state_sales(df)

    monthly_trends(monthly_df)

    # -----------------------------------------------------
    # NEW: Customer Performance Analysis
    # -----------------------------------------------------

    customer_performance = customer_performance_analysis(df)

    # -----------------------------------------------------
    # Profitability analysis
    # -----------------------------------------------------

    category_profit = category_profitability(df)

    state_profit = state_profitability(df)

    monthly_profit = monthly_profit_trend(df)

    # -----------------------------------------------------
    # Subcategory analysis
    # -----------------------------------------------------

    top_sub, bottom_sub = subcategory_profit(
        df,
        top_n=10
    )

    # -----------------------------------------------------
    # Loss-making order analysis
    # -----------------------------------------------------

    loss_analysis = loss_making_analysis(df)

    # -----------------------------------------------------
    # Completion message
    # -----------------------------------------------------

    print(
        "\n=============================================="
    )

    print(
        "All analysis completed successfully!"
    )

    print(
        "Check the 'outputs/' folder for CSV files."
    )

    print(
        "=============================================="
    )