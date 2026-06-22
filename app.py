import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="HydrogenOrg Wastewater Regeneration Simulator v0.1",
    page_icon="💧",
    layout="wide"
)

st.title("HydrogenOrg Wastewater Regeneration Simulator")
st.caption("Conceptual research prototype v0.1 - Wastewater treatment, water recovery, energy use and resource recovery")

st.sidebar.header("Scenario Settings")
scenario_name = st.sidebar.text_input("Scenario name", "Wastewater Regeneration v0.1")
region = st.sidebar.text_input("Region / test node", "Switzerland")
currency = st.sidebar.selectbox("Currency", ["CHF", "EUR", "USD"], index=0)

st.sidebar.markdown("---")
st.sidebar.header("Layer 1 - Wastewater Input")

wastewater_flow_m3_day = st.sidebar.number_input("Wastewater flow (m3/day)", min_value=1.0, max_value=1000000.0, value=1000.0, step=50.0)
population_equivalent = st.sidebar.number_input("Population equivalent", min_value=1, max_value=10000000, value=5000, step=100)
cod_mg_l = st.sidebar.number_input("COD load (mg/L)", min_value=10.0, max_value=5000.0, value=600.0, step=25.0)
bod_mg_l = st.sidebar.number_input("BOD load (mg/L)", min_value=5.0, max_value=3000.0, value=300.0, step=25.0)
nitrogen_mg_l = st.sidebar.number_input("Nitrogen load (mg/L)", min_value=0.0, max_value=500.0, value=45.0, step=5.0)
phosphorus_mg_l = st.sidebar.number_input("Phosphorus load (mg/L)", min_value=0.0, max_value=200.0, value=8.0, step=1.0)

st.sidebar.markdown("---")
st.sidebar.header("Layer 2 - Treatment Process")

treatment_process = st.sidebar.selectbox(
    "Treatment pathway",
    [
        "Conventional Biological Treatment",
        "Membrane Bioreactor",
        "Anaerobic Digestion + Polishing",
        "Advanced Oxidation + Membrane",
        "Hybrid Regeneration Pathway"
    ],
    index=2
)

treatment_efficiency = st.sidebar.slider("Organic removal efficiency (%)", min_value=20, max_value=99, value=85, step=1)
water_recovery_target = st.sidebar.slider("Water recovery target (%)", min_value=10, max_value=98, value=75, step=1)

st.sidebar.markdown("---")
st.sidebar.header("Layer 3 - Energy Integration")

energy_kwh_per_m3 = st.sidebar.number_input("Treatment energy demand (kWh/m3)", min_value=0.05, max_value=10.0, value=0.75, step=0.05)
renewable_share = st.sidebar.slider("Renewable electricity share (%)", min_value=0, max_value=100, value=70, step=5)
electricity_price = st.sidebar.number_input(f"Electricity price ({currency}/kWh)", min_value=0.00, max_value=2.00, value=0.18, step=0.01)

st.sidebar.markdown("---")
st.sidebar.header("Layer 4 - Resource Recovery")

biogas_recovery_efficiency = st.sidebar.slider("Biogas recovery efficiency (%)", min_value=0, max_value=90, value=45, step=5)
hydrogen_conversion_share = st.sidebar.slider("Biogas-to-H2 conceptual conversion share (%)", min_value=0, max_value=80, value=20, step=5)
nutrient_recovery_efficiency = st.sidebar.slider("Nutrient recovery efficiency (%)", min_value=0, max_value=95, value=35, step=5)

st.sidebar.markdown("---")
st.sidebar.header("Layer 5 - Sludge & Environmental Impact")

sludge_factor_kg_per_kg_cod_removed = st.sidebar.number_input("Sludge factor (kg sludge/kg COD removed)", min_value=0.05, max_value=2.0, value=0.35, step=0.05)
sludge_handling_cost = st.sidebar.number_input(f"Sludge handling cost ({currency}/kg sludge)", min_value=0.0, max_value=10.0, value=0.20, step=0.05)
recovered_water_value = st.sidebar.number_input(f"Recovered water value ({currency}/m3)", min_value=0.0, max_value=20.0, value=0.80, step=0.05)

st.sidebar.markdown("---")
st.sidebar.caption("Conceptual research simulator. Not an engineering-certified, environmental-certified or regulatory model.")

KG_PER_MG_PER_L_PER_M3 = 0.001

cod_kg_day = wastewater_flow_m3_day * cod_mg_l * KG_PER_MG_PER_L_PER_M3
bod_kg_day = wastewater_flow_m3_day * bod_mg_l * KG_PER_MG_PER_L_PER_M3
nitrogen_kg_day = wastewater_flow_m3_day * nitrogen_mg_l * KG_PER_MG_PER_L_PER_M3
phosphorus_kg_day = wastewater_flow_m3_day * phosphorus_mg_l * KG_PER_MG_PER_L_PER_M3

cod_removed_kg_day = cod_kg_day * (treatment_efficiency / 100)
bod_removed_kg_day = bod_kg_day * (treatment_efficiency / 100)
cod_remaining_kg_day = cod_kg_day - cod_removed_kg_day

recovered_water_m3_day = wastewater_flow_m3_day * (water_recovery_target / 100)
reject_stream_m3_day = wastewater_flow_m3_day - recovered_water_m3_day

energy_demand_kwh_day = wastewater_flow_m3_day * energy_kwh_per_m3
renewable_energy_kwh_day = energy_demand_kwh_day * (renewable_share / 100)
grid_energy_kwh_day = energy_demand_kwh_day - renewable_energy_kwh_day
electricity_cost_day = energy_demand_kwh_day * electricity_price

CH4_M3_PER_KG_COD = 0.35
CH4_KWH_PER_M3 = 9.97
H2_KG_PER_KWH_EQUIV = 1 / 33.33

methane_potential_m3_day = cod_removed_kg_day * CH4_M3_PER_KG_COD
methane_recovered_m3_day = methane_potential_m3_day * (biogas_recovery_efficiency / 100)
biogas_energy_kwh_day = methane_recovered_m3_day * CH4_KWH_PER_M3
conceptual_h2_kg_day = biogas_energy_kwh_day * (hydrogen_conversion_share / 100) * H2_KG_PER_KWH_EQUIV

nitrogen_recovered_kg_day = nitrogen_kg_day * (nutrient_recovery_efficiency / 100)
phosphorus_recovered_kg_day = phosphorus_kg_day * (nutrient_recovery_efficiency / 100)

sludge_kg_day = cod_removed_kg_day * sludge_factor_kg_per_kg_cod_removed
sludge_cost_day = sludge_kg_day * sludge_handling_cost

water_value_day = recovered_water_m3_day * recovered_water_value
net_operating_value_day = water_value_day - electricity_cost_day - sludge_cost_day

GRID_CO2_KG_PER_KWH = 0.35
WATER_SUPPLY_CO2_KG_PER_M3 = 0.35
co2_avoided_energy = renewable_energy_kwh_day * GRID_CO2_KG_PER_KWH
co2_avoided_water = recovered_water_m3_day * WATER_SUPPLY_CO2_KG_PER_M3
co2_avoided_total = co2_avoided_energy + co2_avoided_water

risk_score = 0
risk_score += 20 if treatment_efficiency < 70 else 6
risk_score += 18 if renewable_share < 50 else 5
risk_score += 18 if reject_stream_m3_day > wastewater_flow_m3_day * 0.4 else 6
risk_score += 18 if sludge_kg_day > cod_removed_kg_day * 0.5 else 8
risk_score = min(risk_score, 100)

st.subheader(scenario_name)
st.caption(f"Region / node: {region} | Process: {treatment_process}")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Recovered water", f"{recovered_water_m3_day:.0f} m3/day")
c2.metric("COD removed", f"{cod_removed_kg_day:.0f} kg/day")
c3.metric("Energy demand", f"{energy_demand_kwh_day:.0f} kWh/day")
c4.metric("Conceptual H2", f"{conceptual_h2_kg_day:.2f} kg/day")
c5.metric("CO2 avoided", f"{co2_avoided_total:.0f} kg/day")

tabs = st.tabs([
    "Overview",
    "Layer 1 Wastewater Input",
    "Layer 2 Treatment",
    "Layer 3 Water Recovery",
    "Layer 4 Energy & H2",
    "Layer 5 Environmental Impact",
    "Roadmap"
])

with tabs[0]:
    st.subheader("System Overview")
    overview = pd.DataFrame({
        "Layer": ["Layer 1", "Layer 2", "Layer 3", "Layer 4", "Layer 5"],
        "Module": [
            "Wastewater Input",
            "Treatment Process",
            "Water Recovery",
            "Energy & Hydrogen Recovery",
            "Environmental Impact"
        ],
        "Key Output": [
            f"{wastewater_flow_m3_day:.0f} m3/day wastewater",
            f"{cod_removed_kg_day:.0f} kg/day COD removed",
            f"{recovered_water_m3_day:.0f} m3/day recovered water",
            f"{conceptual_h2_kg_day:.2f} kg/day conceptual H2",
            f"Risk score {risk_score}/100"
        ],
        "Status": [
            "Prototype active",
            "Prototype active",
            "Prototype active",
            "Conceptual",
            "Conceptual"
        ]
    })
    st.dataframe(overview, use_container_width=True)

    flow = pd.DataFrame({
        "Flow": ["Input wastewater", "Recovered water", "Reject stream", "COD removed", "Sludge"],
        "Value": [
            wastewater_flow_m3_day,
            recovered_water_m3_day,
            reject_stream_m3_day,
            cod_removed_kg_day,
            sludge_kg_day
        ]
    }).set_index("Flow")
    st.bar_chart(flow)

with tabs[1]:
    st.subheader("Layer 1 - Wastewater Input Characterization")
    l1 = pd.DataFrame({
        "Parameter": [
            "Wastewater flow",
            "Population equivalent",
            "COD concentration",
            "BOD concentration",
            "Nitrogen concentration",
            "Phosphorus concentration",
            "Daily COD load",
            "Daily BOD load",
            "Daily nitrogen load",
            "Daily phosphorus load"
        ],
        "Value": [
            f"{wastewater_flow_m3_day:.0f} m3/day",
            f"{population_equivalent:,}",
            f"{cod_mg_l:.0f} mg/L",
            f"{bod_mg_l:.0f} mg/L",
            f"{nitrogen_mg_l:.0f} mg/L",
            f"{phosphorus_mg_l:.1f} mg/L",
            f"{cod_kg_day:.1f} kg/day",
            f"{bod_kg_day:.1f} kg/day",
            f"{nitrogen_kg_day:.1f} kg/day",
            f"{phosphorus_kg_day:.1f} kg/day"
        ]
    })
    st.dataframe(l1, use_container_width=True)

with tabs[2]:
    st.subheader("Layer 2 - Treatment Process")
    l2 = pd.DataFrame({
        "Parameter": [
            "Treatment pathway",
            "Organic removal efficiency",
            "COD removed",
            "BOD removed",
            "COD remaining",
            "Estimated sludge"
        ],
        "Value": [
            treatment_process,
            f"{treatment_efficiency} %",
            f"{cod_removed_kg_day:.1f} kg/day",
            f"{bod_removed_kg_day:.1f} kg/day",
            f"{cod_remaining_kg_day:.1f} kg/day",
            f"{sludge_kg_day:.1f} kg/day"
        ]
    })
    st.dataframe(l2, use_container_width=True)

with tabs[3]:
    st.subheader("Layer 3 - Water Recovery Balance")
    l3 = pd.DataFrame({
        "Parameter": [
            "Water recovery target",
            "Recovered water",
            "Reject stream",
            "Recovered water value",
            "Water value per day"
        ],
        "Value": [
            f"{water_recovery_target} %",
            f"{recovered_water_m3_day:.1f} m3/day",
            f"{reject_stream_m3_day:.1f} m3/day",
            f"{recovered_water_value:.2f} {currency}/m3",
            f"{water_value_day:.2f} {currency}/day"
        ]
    })
    st.dataframe(l3, use_container_width=True)

with tabs[4]:
    st.subheader("Layer 4 - Energy Integration and Hydrogen Recovery")
    l4 = pd.DataFrame({
        "Parameter": [
            "Treatment energy demand",
            "Daily energy demand",
            "Renewable share",
            "Renewable energy",
            "Grid energy",
            "Methane potential",
            "Methane recovered",
            "Biogas energy",
            "Biogas-to-H2 conversion share",
            "Conceptual H2 output"
        ],
        "Value": [
            f"{energy_kwh_per_m3:.2f} kWh/m3",
            f"{energy_demand_kwh_day:.1f} kWh/day",
            f"{renewable_share} %",
            f"{renewable_energy_kwh_day:.1f} kWh/day",
            f"{grid_energy_kwh_day:.1f} kWh/day",
            f"{methane_potential_m3_day:.1f} m3 CH4/day",
            f"{methane_recovered_m3_day:.1f} m3 CH4/day",
            f"{biogas_energy_kwh_day:.1f} kWh/day",
            f"{hydrogen_conversion_share} %",
            f"{conceptual_h2_kg_day:.2f} kg/day"
        ]
    })
    st.dataframe(l4, use_container_width=True)

with tabs[5]:
    st.subheader("Layer 5 - Environmental Impact")
    l5 = pd.DataFrame({
        "Indicator": [
            "Recovered water",
            "N recovered",
            "P recovered",
            "Sludge generation",
            "Sludge handling cost",
            "Electricity cost",
            "Recovered water value",
            "Net operating value",
            "CO2 avoided",
            "Environmental risk score"
        ],
        "Value": [
            f"{recovered_water_m3_day:.1f} m3/day",
            f"{nitrogen_recovered_kg_day:.2f} kg/day",
            f"{phosphorus_recovered_kg_day:.2f} kg/day",
            f"{sludge_kg_day:.1f} kg/day",
            f"{sludge_cost_day:.2f} {currency}/day",
            f"{electricity_cost_day:.2f} {currency}/day",
            f"{water_value_day:.2f} {currency}/day",
            f"{net_operating_value_day:.2f} {currency}/day",
            f"{co2_avoided_total:.1f} kg/day",
            f"{risk_score}/100"
        ]
    })
    st.dataframe(l5, use_container_width=True)

    if risk_score < 35:
        st.success("Environmental risk score is low for the selected conceptual assumptions.")
    elif risk_score < 65:
        st.info("Environmental risk score is moderate. Optimize treatment efficiency, sludge handling and renewable energy share.")
    else:
        st.warning("Environmental risk score is high. Review treatment assumptions, reject stream and sludge generation.")

with tabs[6]:
    st.subheader("Development Roadmap")
    roadmap = pd.DataFrame({
        "Version": ["v0.1", "v0.2", "v0.3", "v0.4", "v1.0"],
        "Focus": [
            "Wastewater input, treatment, water recovery and resource balance",
            "Technology comparison between membrane, anaerobic and hybrid systems",
            "Hydrogen and nutrient recovery optimization",
            "Lifecycle impact and scenario database integration",
            "Public research demo with documentation and contributor path"
        ],
        "Status": ["Current", "Next", "Planned", "Planned", "Planned"]
    })
    st.dataframe(roadmap, use_container_width=True)

export = pd.DataFrame({
    "Scenario": [scenario_name],
    "Region": [region],
    "Wastewater m3/day": [wastewater_flow_m3_day],
    "Recovered water m3/day": [recovered_water_m3_day],
    "COD removed kg/day": [cod_removed_kg_day],
    "Energy demand kWh/day": [energy_demand_kwh_day],
    "Conceptual H2 kg/day": [conceptual_h2_kg_day],
    "Sludge kg/day": [sludge_kg_day],
    "CO2 avoided kg/day": [co2_avoided_total],
    "Net operating value day": [net_operating_value_day],
    "Risk score": [risk_score]
})

st.download_button(
    "Download scenario summary CSV",
    export.to_csv(index=False).encode("utf-8"),
    "hydrogenorg_wastewater_regeneration_v01_summary.csv",
    "text/csv"
)