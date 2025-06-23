import streamlit as st

# Core calculation function
def calculate_units_and_distribute_bill(
    main_prev, main_curr,
    meter1_prev, meter1_curr,
    meter2_prev, meter2_curr,
    meter3_prev, meter3_curr,
    meter4_prev, meter4_curr,
    total_bill
):
    main_units = main_curr - main_prev
    meter1_units = meter1_curr - meter1_prev
    meter2_units = meter2_curr - meter2_prev
    meter3_units = meter3_curr - meter3_prev
    meter4_units = meter4_curr - meter4_prev

    total_sub_meter_units = meter1_units + meter2_units + meter3_units + meter4_units
    extra_units = main_units - total_sub_meter_units

    if extra_units < 0:
        raise ValueError("Main meter units cannot be less than the sum of sub-meter units.")

    shared_extra = extra_units / 3

    adjusted_meter1 = meter1_units
    adjusted_meter2 = meter2_units + shared_extra
    adjusted_meter3 = meter3_units + shared_extra
    adjusted_meter4 = meter4_units + shared_extra

    total_consumption = adjusted_meter1 + adjusted_meter2 + adjusted_meter3 + adjusted_meter4

    meter1_bill = (adjusted_meter1 / total_consumption) * total_bill
    meter2_bill = (adjusted_meter2 / total_consumption) * total_bill
    meter3_bill = (adjusted_meter3 / total_consumption) * total_bill
    meter4_bill = (adjusted_meter4 / total_consumption) * total_bill

    return {
        "Sanjay Sharma's Meter": {'Units': adjusted_meter1, 'Bill Share': round(meter1_bill, 2)},
        "G P Sharma's Meter": {'Units': adjusted_meter2, 'Bill Share': round(meter2_bill, 2)},
        "Rajesh Kumar's Meter": {'Units': adjusted_meter3, 'Bill Share': round(meter3_bill, 2)},
        "Mahipal Sharma's Meter": {'Units': adjusted_meter4, 'Bill Share': round(meter4_bill, 2)},
        'Main Meter Units': main_units,
        'Extra Consumption': extra_units,
        'Shared Extra per Meter (2,3,4)': shared_extra
    }

# Streamlit UI
st.set_page_config(page_title="Electricity Bill Splitter", layout="wide")
st.title("📊 Electricity Bill Splitter")

st.header("🔌 Main Meter Readings")
col_main_prev, col_main_curr = st.columns([2, 2])
main_prev = col_main_prev.number_input("Main Meter Previous Reading", value=5000, key="main_prev")
main_curr = col_main_curr.number_input("Main Meter Current Reading", value=6305, key="main_curr")

st.markdown("---")

st.header("📟 Sub Meter Readings")

# Meter 1
st.subheader("Sanjay Sharma's Meter")
col1_prev, col1_curr = st.columns(2)
meter1_prev = col1_prev.number_input("Previous Reading", value=1000, key="m1_prev")
meter1_curr = col1_curr.number_input("Current Reading", value=1200, key="m1_curr")

# Meter 2
st.subheader("G P Sharma's Meter")
col2_prev, col2_curr = st.columns(2)
meter2_prev = col2_prev.number_input("Previous Reading", value=2000, key="m2_prev")
meter2_curr = col2_curr.number_input("Current Reading", value=2400, key="m2_curr")

# Meter 3
st.subheader("Rajesh Kumar's Meter")
col3_prev, col3_curr = st.columns(2)
meter3_prev = col3_prev.number_input("Previous Reading", value=1500, key="m3_prev")
meter3_curr = col3_curr.number_input("Current Reading", value=1700, key="m3_curr")

# Meter 4
st.subheader("Mahipal Sharma's Meter")
col4_prev, col4_curr = st.columns(2)
meter4_prev = col4_prev.number_input("Previous Reading", value=1800, key="m4_prev")
meter4_curr = col4_curr.number_input("Current Reading", value=2200, key="m4_curr")

st.markdown("---")

st.header("💰 Total Bill Amount")
total_bill = st.number_input("Enter Total Bill Amount (₹)", value=9613.00, format="%.2f", key="total_bill")

if st.button("🔍 Calculate Bill Split"):
    try:
        result = calculate_units_and_distribute_bill(
            main_prev, main_curr,
            meter1_prev, meter1_curr,
            meter2_prev, meter2_curr,
            meter3_prev, meter3_curr,
            meter4_prev, meter4_curr,
            total_bill
        )

        st.success("✅ Calculation Completed!")

        st.markdown(f"### Total Units (Main Meter): **{result['Main Meter Units']} units**")
        st.markdown(f"### Extra Consumption: **{result['Extra Consumption']} units**")
        st.markdown(f"### Shared Extra per Meter (G P Sharma's Meter, Rajesh Kumar's Meter, Mahipal Sharma's Meter): **{round(result['Shared Extra per Meter (2,3,4)'], 2)} units**")

        st.markdown("## 📑 <u><b>Bill Split Details</b></u>", unsafe_allow_html=True)

        for meter, details in result.items():
            if isinstance(details, dict):
                st.markdown(
                    f"""
                    <div style='font-size:24px; font-weight:bold; margin-bottom:20px;'>
                        {meter}: Units = {details['Units']} | Bill Share = ₹{details['Bill Share']}
                    </div>
                    """, unsafe_allow_html=True
                )

    except ValueError as e:
        st.error(f"❌ {str(e)}")
