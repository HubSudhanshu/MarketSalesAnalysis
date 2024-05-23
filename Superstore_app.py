import streamlit as st
import pandas as pd 
import plotly.express as px
import os
import warnings
import plotly.graph_objects as go
warnings.filterwarnings('ignore')

st.set_page_config(page_title="superstore USA!!!!", page_icon=":bar_chart:",layout="wide")
st.title(":bar_chart: SUPERSTORE EDA")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

f1 = st.file_uploader(':file_folder: upload a file',type=(["csv","xlsx","xls","txt"]))
if f1 is not None:
    filename = f1.name
    df = pd.read_excel(filename)
    st.write(df)
else:
    directory_path = r"C:\Users\admin\Documents\data\superstore_usa"
    file_path = os.path.join(directory_path, "Superstore_USA.xlsx")
    df = pd.read_excel(file_path)
    st.write(df)
    #os.chdir(r"C:\Users\admin\Documents\data\superstore_usa")
    #df = pd.read_excel("Superstore_USA.xlsx")
    

col1, col2 = st.columns((2))
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Getting the min and max date 

startdate = df["Order Date"].min().date()
enddate = df["Order Date"].max().date()

with col1:
    date1 = st.date_input( " Star Date", startdate)

with col2:
    date2 = st.date_input( " End Date ", enddate)
df = df[(df["Order Date"].dt.date >= date1) & (df["Order Date"].dt.date <= date2)].copy()


# Creating Sidebar for Region 

st.sidebar.header(" Select Region")
region = st.sidebar.multiselect("Pick Your Region",df["Region"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)]

# Creating Sidebar for State

st.sidebar.header(" Select State")
state = st.sidebar.multiselect("Pick Your State",df2["State or Province"].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["State or Province"].isin(state)]


# Creating Sidebar for City
st.sidebar.header(" Select City")
city = st.sidebar.multiselect("Pick Your City", df3["City"].unique())


# Creating Filter For The Data Based On State,City and Region
if not region and not state and not city:
    newdf = df
elif not region and not city:
    newdf = df[df["State or Province"].isin(state)]
elif not state and not city:
    newdf = df[df["Region"].isin(region)]
elif not state and not region:
    newdf= df[df["city"].isin(city)]
elif state and city:
    newdf = df3[df["State or Province"].isin(state) & df3["City"].isin(city)]
elif region and city:
    newdf = df3[df["Region"].isin(region) & df3["City"].isin(city)]
elif region and state:
    newdf = df3[df["Region"].isin(region) & df3["State or Province"].isin(state)]
elif city:
    newdf = df3[df3["City"].isin(city)]
else:
    newdf = df3[df3["Region"].isin(region) & df3["State or Province"].isin(state) & df3["City"].isin(city)]


col3, col4 = st.columns((2))
# Creating Pie Chart For Region Wise Sales
with col3:
    st.subheader("Region wise Sales")
    fig = px.pie(newdf, values = "Sales", names = "Region", hole = 0.5)
    fig.update_traces(text = newdf["Region"], textposition = "outside")
    st.plotly_chart(fig,use_container_width=True)

# Creating Pie Chart For State Wise Sales
with col4:
    st.subheader("State wise Sales")
    fig = px.pie(newdf, values = "Sales", names = "State or Province", hole = 0.5)
    fig.update_traces(text = newdf["State or Province"], textposition = "outside")
    st.plotly_chart(fig,use_container_width=True)


# Creating Bar Chart For Catrgory Wise Sales

category_df = newdf.groupby(by = ["Product Category"], as_index = False)["Sales"].sum()

col1, col2 = st.columns((2))
with col1:
    st.subheader("Category wise Sales")
    fig = px.bar(category_df, x = "Product Category", y = "Sales", text = ['${:,.2f}'.format(x) for x in category_df["Sales"]],
                 template = "seaborn")
    st.plotly_chart(fig,use_container_width=True, height = 200)

# adding Download Widget to Download The Data Based On The Selected Filter
with col1:
    category_df = newdf.groupby(by = ["Product Category"], as_index = False)["Sales"].sum()
    with st.expander("Category_ViewData"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Category.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')


# Creating Bar Chart For Customer Segment 

category_df = newdf.groupby(by = ["Customer Segment"], as_index = False)["Sales"].sum()
with col2:
    st.subheader("Customer Segment Wise Sales")
    fig = px.bar(category_df, x = "Customer Segment", y = "Sales", text = ['${:,.2f}'.format(x) for x in category_df["Sales"]],
                 template = "seaborn")
    st.plotly_chart(fig,use_container_width=True, height = 200)

# adding Download Widget to Download The Data Based On The Selected Filter

with col2:
    category_df = newdf.groupby(by = ["Customer Segment"], as_index = False)["Sales"].sum()
    with st.expander("Customer_Segment_ViewData"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Customer Segment.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')

newdf["month_year"] = newdf["Order Date"].dt.to_period("M")

st.subheader('Time Series Analysis')
linechart = pd.DataFrame(newdf.groupby(newdf["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
fig2 = px.line(linechart, x = "month_year", y="Sales", labels = {"Sales": "Amount"},height=500, width = 1000,template="gridon")
st.plotly_chart(fig2,use_container_width=True)

newdf["year"] = newdf["Order Date"].dt.to_period("Y")
st.subheader("Time Series Analysis with Respect To year")
linechart = pd.DataFrame(newdf.groupby(newdf["year"].dt.strftime("%Y"))["Sales"].sum()).reset_index()
fig2 = px.line(linechart, x = "year", y="Sales", labels = {"Sales": "Amount"},height=500, width = 1000,template="gridon")
st.plotly_chart(fig2,use_container_width=True)

# Create a scatter plot
data1 = px.scatter(newdf, x = "Sales", y = "Profit", size = "Quantity ordered new")
data1['layout'].update(title="Relationship between Sales and Profits using Scatter Plot.",
                       titlefont = dict(size=20),xaxis = dict(title="Sales",titlefont=dict(size=19)),
                       yaxis = dict(title = "Profit", titlefont = dict(size=19)))
st.plotly_chart(data1,use_container_width=True)

# Download orginal DataSet
with st.expander("View Data"):
    st.write(newdf.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))
csv = df.to_csv(index = False).encode('utf-8')
st.download_button('Download Data', data = csv, file_name = "Data.csv",mime = "text/csv")

