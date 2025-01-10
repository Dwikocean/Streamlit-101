import streamlit as st
import pandas as pd

# In-Memory Product Data (Replace with Database for Production)
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "Product ID": ["P001", "P002", "P003"],
        "Name": ["T-Shirt", "Jeans", "Sneakers"],
        "Category": ["Shirts", "Pants", "Shoes"],
        "Size": ["M", 32, 42],
        "Stock": [10, 5, 2],
        "Price": [150000, 250000, 500000],
    })

# Discount Threshold
DISCOUNT_THRESHOLD = 3
DISCOUNT_RATE = 0.2

# Function to Apply Discount
def apply_discount(dataframe):
    discounted_products = dataframe[dataframe["Stock"] <= DISCOUNT_THRESHOLD].copy()
    discounted_products["Price"] *= (1 - DISCOUNT_RATE)
    return discounted_products

# Application Title
st.title("Fashion Store Management System")

# Sidebar Menu
menu = st.sidebar.selectbox("Menu", ["Dashboard", "Add Product", "Update Stock", "Cashier", "Sales Report", "Analysis"])

if menu == "Dashboard":
    st.header("Product Dashboard")
    category_filter = st.selectbox("Filter by Category", ["All"] + list(st.session_state.df["Category"].unique()))
    if category_filter != "All":
        filtered_df = st.session_state.df[st.session_state.df["Category"] == category_filter]
    else:
        filtered_df = st.session_state.df

    if not filtered_df.empty:
        st.dataframe(filtered_df)
    else:
        st.write("No products available.")

elif menu == "Add Product":
    st.header("Add New Product")
    with st.form("add_product_form"):
        product_id = st.text_input("Product ID")
        name = st.text_input("Product Name")
        category = st.selectbox("Category", ["Shirts", "Pants", "Shoes", "Accessories"])
        if category == "Shirts":
            size = st.selectbox("Size", ["S", "M", "L", "XL"])
        elif category == "Pants":
            size = st.selectbox("Size", [30, 32, 34, 36, 38])
        elif category == "Shoes":
            size = st.selectbox("Size", [40, 41, 42, 43, 44, 45])
        else:
            size = "One Size"
        stock = st.number_input("Stock", min_value=0, step=1)
        price = st.number_input("Price", min_value=0.0, step=0.01)
        submit = st.form_submit_button("Add Product")

    if submit:
        if product_id and name:
            new_row = {
                "Product ID": product_id,
                "Name": name,
                "Category": category,
                "Size": size,
                "Stock": stock,
                "Price": price,
            }
            st.session_state.df = st.session_state.df.append(new_row, ignore_index=True)
            st.success(f"Product {name} added successfully!")
        else:
            st.error("Product ID and Name are required.")

elif menu == "Update Stock":
    st.header("Update Product Stock and Price")
    if not st.session_state.df.empty:
        product_id = st.selectbox("Select Product", st.session_state.df["Product ID"].unique())
        selected_product = st.session_state.df[st.session_state.df["Product ID"] == product_id].iloc[0]
        new_stock = st.number_input("New Stock", min_value=0, step=1, value=selected_product["Stock"])
        new_price = st.number_input("New Price", min_value=0.0, step=0.01, value=selected_product["Price"])
        if st.button("Update"):
            st.session_state.df.loc[st.session_state.df["Product ID"] == product_id, "Stock"] = new_stock
            st.session_state.df.loc[st.session_state.df["Product ID"] == product_id, "Price"] = new_price
            st.success(f"Product ID {product_id} updated successfully.")
    else:
        st.write("No products available to update.")

elif menu == "Cashier":
    st.header("Cashier System")
    if not st.session_state.df.empty:
        cart = []
        total_price = 0
        with st.form("cashier_form"):
            product_id = st.selectbox("Select Product", st.session_state.df["Product ID"].unique())
            quantity = st.number_input("Quantity", min_value=1, step=1)
            add_to_cart = st.form_submit_button("Add to Cart")

        if add_to_cart:
            selected_product = st.session_state.df[st.session_state.df["Product ID"] == product_id].iloc[0]
            if selected_product["Stock"] >= quantity:
                cart.append({
                    "Product ID": selected_product["Product ID"],
                    "Name": selected_product["Name"],
                    "Quantity": quantity,
                    "Unit Price": selected_product["Price"],
                    "Total": quantity * selected_product["Price"],
                })
                total_price += quantity * selected_product["Price"]
                st.session_state.df.loc[st.session_state.df["Product ID"] == product_id, "Stock"] -= quantity
                st.success(f"Added {quantity} of {selected_product['Name']} to cart.")
            else:
                st.error("Insufficient stock.")

        if cart:
            st.write("Shopping Cart")
            st.table(cart)
            st.write(f"Total Price: {total_price}")

    else:
        st.write("No products available for sale.")

elif menu == "Sales Report":
    st.header("Sales Report")
    st.write("Feature Coming Soon!")

elif menu == "Analysis":
    st.header("Discount Analysis")
    discounted_products = apply_discount(st.session_state.df)
    if not discounted_products.empty:
        st.write("Products with Discounts")
        st.dataframe(discounted_products)
    else:
        st.write("No products eligible for discount.")
