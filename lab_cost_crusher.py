# lab_cost_crusher.py ─ FIXED VERSION (works 100% on Streamlit Cloud)
import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="Lab Cost Crusher", layout="centered")
st.title("Lab Cost Crusher – Cost Analyzer")

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()

# Sidebar inputs
st.sidebar.header("Add New Reagent Purchase")
item = st.sidebar.text_input("Reagent / Item Name", "Exo-Flow 32 Capture Kit")
vendor = st.sidebar.text_input("Vendor", "SBI")
catalog = st.sidebar.text_input("Catalog # (optional)", "EXOFLOW32A-1")
size = st.sidebar.text_input("Size / Quantity", "32 tests")
price = st.sidebar.number_input("Price ($)", min_value=0.0, value=420.0)
units = st.sidebar.number_input("Units in Package", min_value=1, value=32)
shipping = st.sidebar.number_input("Shipping Cost ($)", min_value=0.0, value=0.0)
notes = st.sidebar.text_area("Notes (optional)", "")

st.sidebar.markdown("### Alternative Vendor (optional)")
alt_vendor = st.sidebar.text_input("Alternative Vendor", "")
alt_price = st.sidebar.number_input("Alternative Price ($)", min_value=0.0, value=0.0)
alt_units = st.sidebar.number_input("Alternative Units", min_value=0, value=1)
alt_shipping = st.sidebar.number_input("Alt Shipping ($)", min_value=0.0, value=0.0)

# Calculations
total_cost = price + shipping
price_per_unit = total_cost / units if units > 0 else 0
alt_total = alt_price + alt_shipping
alt_per_unit = alt_total / alt_units if alt_units > 0 and alt_total > 0 else 0
savings = total_cost - alt_total if alt_total > 0 else 0

# Display results
col1, col2 = st.columns(2)
with col1:
    st.metric("Your Price per Unit", f"${price_per_unit:.3f}")
with col2:
    if alt_total > 0:
        delta = f"${savings:+.2f} savings" if savings > 0 else f"-${abs(savings):.2f}"
        st.metric("Alternative Price per Unit", f"${alt_per_unit:.3f}", delta)

# Save + Download
if st.sidebar.button("Add & Prepare Download", type="primary"):
    new_row = {
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Item": item, "Vendor": vendor, "Catalog": catalog, "Size": size,
        "Price": price, "Shipping": shipping, "Total Cost": total_cost,
        "Units": units, "Price per Unit": round(price_per_unit, 4),
        "Notes": notes, "Alt Vendor": alt_vendor or "",
        "Alt Price": alt_price or "", "Alt Per Unit": round(alt_per_unit, 4) if alt_total > 0 else "",
        "Potential Savings": round(savings, 2) if savings > 0 else 0
    }
    st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_row])], ignore_index=True)
    st.sidebar.success(f"Added {item}! Ready to download below")

# Show table + download
if not st.session_state.df.empty:
    st.markdown("### Current Month Expenses")
    st.dataframe(st.session_state.df)

    month_str = datetime.now().strftime("%Y-%m")
    csv = st.session_state.df.to_csv(index=False)
    st.download_button(
        label="Download Lab_Expenses_" + month_str + ".csv",
        data=csv,
        file_name=f"Lab_Expenses_{month_str}.csv",
        mime="text/csv",
        type="primary"
    )
    st.info("💡 CSV opens perfectly in Excel/Google Sheets – import as table for charts!")
else:
    st.info("Add your first purchase on the left → download appears here!")



