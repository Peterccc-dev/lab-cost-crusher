# lab_cost_crusher.py
import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Lab Cost Crusher", layout="centered")
st.title("🔬 Lab Cost Crusher")

# Sidebar inputs
st.sidebar.header("Add New Reagent Purchase")
item = st.sidebar.text_input("Reagent / Item Name", "Item")
vendor = st.sidebar.text_input("Vendor", "Thermo Fisher")
catalog = st.sidebar.text_input("Catalog # (optional)", "3122")
size = st.sidebar.text_input("Size / Quantity", "50")
price = st.sidebar.number_input("Price ($)", min_value=0.0, value=420.0)
units = st.sidebar.number_input("Units in Package", min_value=1, value=32)
shipping = st.sidebar.number_input("Shipping Cost ($)", min_value=0.0, value=0.0)
notes = st.sidebar.text_area("Notes (optional)", "")

st.sidebar.markdown("### Alternative Vendor (optional)")
alt_vendor = st.sidebar.text_input("Alternative Vendor", "Thermo Fisher")
alt_price = st.sidebar.number_input("Alternative Price ($)", min_value=0.0, value=0.0)
alt_units = st.sidebar.number_input("Alternative Units", min_value=1, value=1)
alt_shipping = st.sidebar.number_input("Alt Shipping ($)", min_value=0.0, value=0.0)

# Calculations
total_cost = price + shipping
price_per_unit = total_cost / units if units > 0 else 0

alt_total = alt_price + alt_shipping
alt_per_unit = alt_total / alt_units if alt_units > 0 else 0
savings = total_cost - alt_total if alt_total > 0 else 0

# Display results
col1, col2 = st.columns(2)
with col1:
    st.metric("Your Price per Unit", f"${price_per_unit:.3f}")
with col2:
    if alt_total > 0:
        st.metric("Alternative Price per Unit", f"${alt_per_unit:.3f}", 
                 f"{savings:+.2f} savings" if savings > 0 else f"-{abs(savings):.2f}")

if st.sidebar.button("💾 Save to Monthly Excel", type="primary"):
    # Create monthly file
    month_str = datetime.now().strftime("%Y-%m")
    filename = f"Lab_Expenses_{month_str}.xlsx"
    
    new_row = {
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Item": item,
        "Vendor": vendor,
        "Catalog": catalog,
        "Size": size,
        "Price": price,
        "Shipping": shipping,
        "Total Cost": total_cost,
        "Units": units,
        "Price per Unit": round(price_per_unit, 4),
        "Notes": notes,
        "Alt Vendor": alt_vendor if alt_total > 0 else "",
        "Alt Price": alt_price if alt_total > 0 else "",
        "Alt Per Unit": round(alt_per_unit, 4) if alt_total > 0 else "",
        "Potential Savings": round(savings, 2) if savings > 0 else 0
    }
    
    if os.path.exists(filename):
        df = pd.read_excel(filename)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        df = pd.DataFrame([new_row])
    
    df.to_excel(filename, index=False)
    st.sidebar.success(f"Saved to {filename}!")

# Show current month table
st.markdown("### Current Month Expenses")
month_file = f"Lab_Expenses_{datetime.now().strftime('%Y-%m')}.xlsx"
if os.path.exists(month_file):
    df = pd.read_excel(month_file)
    st.dataframe(df.style.format({"Price per Unit": "${:.3f}", "Alt Per Unit": "${:.3f}"}))
    st.bar_chart(df[["Item", "Total Cost"]].set_index("Item"))
else:
    st.info("No expenses yet this month — add your first one on the left!")