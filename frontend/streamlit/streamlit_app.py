import os
import requests
from google.cloud import bigquery
import random
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st

pd.set_option('display.max_rows', None, 'display.max_columns', None)

#######################################
# PAGE SETUP
#######################################
st.set_page_config(page_title="AlphaBeam Dashboard", page_icon=":bar_chart:", layout="wide")

st.title("AlphaBeam Dashboard")
# st.markdown("_Prototype v0.4.1_")

with st.sidebar:
    # st.header("AlphaBeam Chat Engine")
    # Function to send user query to the Flask API
    def send_query(user_query):
        api_url = "http://34.69.102.150/retrieval"  # Replace with your actual Flask API URL
        response = requests.post(api_url, json={"projectName": "semantic_layer_4", 
                                                "query": user_query,
                                                "reset_chat": True})
        if response.status_code == 200:
            return response.json().get("result", "Error processing request")
        else:
            return "Error communicating with the AI engine"

    # Initialize session_state to store user messages
    if 'user_messages' not in st.session_state:
        st.session_state.user_messages = []

    # Streamlit app layout
    def main():
        st.title("AlphaBeam Chat Engine")

        # User input
        user_input = st.text_input("Enter your query:")

        # Send button
        if st.button("Send") and user_input:
            # Store user message in session_state
            st.session_state.user_messages.append(("You", user_input))

            # Display user message
            st.text(f"You: {user_input}")

            # Send user query to the Flask API
            bot_response = send_query(user_input)

            # Store bot response in session_state
            st.session_state.user_messages.append(("AI Engine", bot_response))

            # Display bot response
            st.text(f"AI Engine: {bot_response}")

        # Display chat history
        st.text("Chat History:")
        for sender, message in st.session_state.user_messages:
            st.text(f"{sender}: {message}")
    if __name__ == "__main__":
        main()    

# ######################################
# DATA LOADING: Connect to Google bigquery
# ######################################

def merge_table(table1, table2, left_on, right_on):
    new_df = pd.merge(table1, table2, left_on=left_on, right_on=right_on)
    return new_df


customers = pd.read_csv("frontend/streamlit/dataset/customer.csv")
products = pd.read_csv("frontend/streamlit/dataset/product.csv")
sales = pd.read_csv("frontend/streamlit/dataset/sales.csv")

df = merge_table(merge_table(customers, sales, left_on='customer_key', right_on='customer_key'), products, left_on='product_key', right_on='product_key')
df["Profit"] = df["revenue_total"] - df["product_cost_total"]      

best_revenue = df.groupby('product_name')['revenue_total'].sum().reset_index().sort_values(by='revenue_total', ascending=True).head(10)
best_category = pd.melt(df[["product_category", 'product_cost_total', 'revenue_total', 'Profit']], 
                    id_vars='product_category', var_name='Variable', value_name='Value')

# #######################################
# # VISUALIZATION METHODS
# #######################################

def plot_metric(label, value, prefix="", suffix="", show_graph=False, color_graph=""):
    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            value=value,
            gauge={"axis": {"visible": False}},
            number={
                "prefix": prefix,
                "suffix": suffix,
                "font.size": 28,
            },
            title={
                "text": label,
                "font": {"size": 24},
            },
        )
    )

    if show_graph:
        fig.add_trace(
            go.Scatter(
                y=random.sample(range(0, 101), 30),
                hoverinfo="skip",
                fill="tozeroy",
                fillcolor=color_graph,
                line={
                    "color": color_graph,
                },
            )
        )

    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        margin=dict(t=50, b=0),
        showlegend=False,
        plot_bgcolor="white",
        height=100,
        
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_bottom_left():
    best_product = best_revenue

    fig = px.bar(
    best_product,
    y="product_name",
    x="revenue_total",
    barmode="group",
    text_auto=".2s",
    title="10 Best Selling Products",
    height=500,
)

    fig.update_traces(
    marker_color='#8690FF',  # Set the bar color to light purple
    textfont_size=10,
    textangle=0,
    textposition="outside",
    cliponaxis=False,
)

    fig.update_layout(
    xaxis=dict(title="Total Revenue (USD)", showticklabels=True),  # Turn off x-axis labels tickangle=45, tickmode="linear",
    yaxis=dict(title="Product Name", tickmode="linear", automargin=True, showticklabels=True),
    margin=dict(l=50, r=50, t=50, b=50),  # Adjust margins to create space
)
    st.plotly_chart(fig, use_container_width=True)



def plot_bottom_right():
    # Melt the DataFrame to have a 'Variable' column
    best_cat = best_category

    # Create a bar chart
    fig = px.bar(best_cat, 
             x='product_category', 
             y='Value', 
             color='Variable',
             barmode="group",
             title='Category Review using Sales Revenue and Profit Margin',
             color_discrete_map={'product_cost_total': '#8690FF', 'revenue_total': 'teal', 'Profit': 'navy'},
             labels={'Value': 'Column Value'}, 
             height=550,)


    fig.update_traces(
       textfont_size=10, 
       textangle=0, 
       textposition="outside", 
       cliponaxis=False
    )


    fig.update_layout(
        xaxis=dict(title="Product Category", tickangle=0, tickmode="linear", showticklabels=True),  # Turn off x-axis labels
        yaxis=dict(title="Volume (USD)", showticklabels=True),
        margin=dict(l=50, r=50, t=100, b=50),  # Adjust margins to create space
        legend_orientation='h',
        legend=dict(y=1.02, x=0.5, xanchor='center', yanchor='bottom', title_text=''),
    )

    st.plotly_chart(fig, use_container_width=True)


# #######################################
# # STREAMLIT LAYOUT
# #######################################


column_1, column_2, column_3, column_4= st.columns(4)

with column_1:
    plot_metric(
        "Total Cost",
        df["product_cost_total"].sum(),
        prefix="$",
        suffix="",
        show_graph=True,
        color_graph="#b2d8d8",
    )

with column_2:
    plot_metric(
            "Total Product Sold",
            df["quantity_total"].sum(),
            prefix="",
            suffix="",
            show_graph=True,
            color_graph="#b2d8d8",
        )


with column_3:
    plot_metric(
        "Total Revenue",
        df["revenue_total"].sum(),
        prefix="$",
        suffix="",
        show_graph=True,
        color_graph="#b2d8d8",
    )


with column_4:
    plot_metric(
            "Profit Margin",
            df["Profit"].sum(),
            prefix="$",
            suffix="",
            show_graph=True,
            color_graph="#b2d8d8",
        )

bottom_left_column, bottom_right_column = st.columns((2,3))


with bottom_left_column:
    plot_bottom_left()

with bottom_right_column:
    plot_bottom_right()