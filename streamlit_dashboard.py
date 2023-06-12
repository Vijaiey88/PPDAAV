import pandas as pd 
import plotly.express as px
import streamlit as st 
import warnings
import mysql.connector
import geopandas as gpd
warnings.filterwarnings("ignore")

st. set_page_config(page_title='Phonepe Data Visualization Dashboard',
                    layout="wide")

st.markdown('<h1 style="color:purple; background-color:white; padding: 10px;">PhonePe Pulse Data Analysis and Visualization</h1>', unsafe_allow_html=True)

st.markdown(
    """
    <style>
        .st-b8 {
            width: 100% !important; /* Set the desired width of the selectbox */
            height: 60px !important; /* Set the desired height of the selectbox */
            font-size: 30px !important; /* Set the desired font size of the selectbox */
        }
    </style>
    """,
    unsafe_allow_html=True
)

with st.container():
    menu_items = ["About", "Search", "Insights", "Geo visualization"]
    selected_menu = st.empty()
    selected_menu_item = selected_menu.selectbox('', menu_items)

# Handle menu selection
if selected_menu_item == "About":
    st.markdown('<h2 style="color:purple; background-color:white; padding: 10px;">Phonepe</h2>', unsafe_allow_html=True)
    with st.container():
        media_column,text_column=st.columns((1,2,))
    with media_column:
        st.video('https://youtu.be/c_1H6vivsiA')
    with text_column:
        st.markdown("""<span style="font-size: 17px;">PhonePe launched Pulse in 2021, with the aim of demystifying data on the Indian digital payments ecosystem. 
                 Pulse is India’s first and only interactive geospatial platform offering deep insights, in-depth conversations and interesting 
                 facts on how the payments landscape in the country is evolving.</span>
                 
<span style="font-size: 17px;">PhonePe Pulse, a feature offered by the digital payments platform PhonePe, has contributed to the growth and development of digital payments
in India. PhonePe Pulse is a data analytics platform that provides valuable insights into digital payment trends and behaviors. By leveraging 
the vast amount of transaction data processed through the PhonePe platform, Pulse offers real-time analytics, visualizations, and reports that 
help businesses and policymakers make data-driven decisions.</span>

<span style="font-size: 17px;">The availability of PhonePe Pulse has empowered businesses to gain a deeper understanding of consumer preferences, spending patterns,
and market trends. This information enables businesses to tailor their products and services, optimize marketing strategies, and enhance 
customer experiences. With access to Pulse, businesses can identify emerging trends, forecast demand, and make informed decisions to drive growth 
and innovation in the digital payments ecosystem.</span>

<span style="font-size: 17px;">From a policymaking perspective, PhonePe Pulse plays a crucial role in providing valuable insights for government entities. By analyzing
transaction data on a macro level, policymakers can gain a comprehensive understanding of economic trends, consumer behavior, and the impact of policies 
related to digital payments. This data-driven approach allows for more targeted policy interventions, efficient resource allocation, and evidence-based 
decision-making to foster economic development and financial inclusion.</span>

<span style="font-size: 17px;">Moreover, PhonePe Pulse contributes to the overall transparency and accountability of digital payments. By tracking and analyzing transaction data,
Pulse helps detect and prevent fraudulent activities, ensuring a secure and trustworthy digital payments environment. The availability of this data also 
aids in combating corruption, tax evasion, and illicit financial activities, promoting a more transparent and accountable financial ecosystem.</span>

<span style="font-size: 17px;">Overall, PhonePe Pulse has emerged as a valuable tool in the realm of digital payments, providing businesses and policymakers with actionable insights to drive
growth, enhance efficiency, and promote financial inclusion. By harnessing the power of data analytics, PhonePe Pulse contributes to the ongoing development of
the digital payments landscape in India, making it a significant catalyst for progress in the country.</span>

<span style="font-size: 17px;">PhonePe Pulse is your window to the world of how India transacts with interesting trends, deep insights and in-depth analysis based on our data put together 
by the PhonePe team.</span>""", unsafe_allow_html=True)
    with media_column:
        st.image('https://media.licdn.com/dms/image/C4D22AQEx2-WHPvwoJw/feedshare-shrink_800/0/1676351663830?e=1688601600&v=beta&t=So3jGNDCL1rKLseU3D05du-MaVx4yEilBjqDQRYFuDE')

if selected_menu_item == "Search":
    # Establish a connection to the MySQL database
    connection = mysql.connector.connect(host='localhost', user='root', password='Ajith568.', database='phonepe')
    
    
    table_mapping = {
    "Statewise Various Payment Type of Transaction Amount and Count": "ats",
    "Statewise User Count by Mobile Brand": "aus",
    "Districtwise Total Transaction Count and Amount": "mts",
    "Districtwise Registered User Count": "mus",
    "Top 10 States with Districts of Total Transaction Amount and Count": "ttsd",
    "Top 10 States with Pincodes of Total Transaction Amount and Count": "ttsp",
    "Top 10 States with Districts of Registered Users": "tusd",
    "Top 10 States with Pincoddes of Registered Users": "tusp"
      }

    # Retrieve the list of tables from the database
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    table_names = [table[0] for table in tables]
    
    # Create a list of display names for the selectbox
    display_names = list(table_mapping.keys())
    
    # Display the tables in a dropdown selectbox
    st.markdown('<h3 style="font-size: 25px;">Select a table :</h3>', unsafe_allow_html=True)
    selected_display_name = st.selectbox("", display_names)
    
    # Retrieve the actual table name based on the selected display name
    selected_table = table_mapping[selected_display_name]

    # Perform further operations or queries based on the selected table
    if selected_table:
        # Retrieve distinct states from the table
        state_query = f"SELECT DISTINCT state FROM {selected_table}"
        cursor.execute(state_query)
        states = [state[0] for state in cursor.fetchall()]

        # Create selectboxes for state, year, and quarter in a single row
        col1, col2, col3 = st.columns([2,1,1])

        with col1:
            st.markdown('<h3 style="font-size: 25px;">Select a state :</h3>', unsafe_allow_html=True)
            selected_state = st.selectbox("", states)

        with col2:
            st.markdown('<h3 style="font-size: 25px;">Select a year :</h3>', unsafe_allow_html=True)
            selected_year = st.selectbox("", range(2018, 2023), format_func=str)

        with col3:
            st.markdown('<h3 style="font-size: 25px;">Select a quarter :</h3>', unsafe_allow_html=True)
            selected_quarter = st.selectbox("", [1, 2, 3, 4], format_func=str)

        if selected_state and selected_year and selected_quarter:
            query = f"SELECT * FROM {selected_table} WHERE state = '{selected_state}' AND year = {selected_year} AND quarter = {selected_quarter}"
            df = pd.read_sql(query, connection)
            # Convert the DataFrame to HTML
            table_html = df.to_html(index=False)
            # Wrap the table HTML in a centered div
            centered_table_html = f'<div style="display: flex; justify-content: center;"><table>{table_html}</table></div>'
            # Display the centered table
            st.write(centered_table_html, unsafe_allow_html=True)
        else:
            st.write("Please select a state, year, and quarter.")
    else:
        st.write("No table selected.")
    
    
    # Close the database connection
    cursor.close()
    connection.close()
   
if selected_menu_item == "Insights":
    # Establish a connection to the MySQL database
    connection = mysql.connector.connect(host='localhost', user='root', password='Ajith568.', database='phonepe')

    table_mapping = {
        "Statewise Various Payment Type of Transaction Amount and Count": "ats",
        "Statewise User Count by Mobile Brand": "aus",
        "Districtwise Total Transaction Count and Amount": "mts",
        "Districtwise Registered User Count": "mus",
        "Top 10 States with Districts of Total Transaction Amount and Count": "ttsd",
        "Top 10 States with Pincodes of Total Transaction Amount and Count": "ttsp",
        "Top 10 States with Districts of Registered Users": "tusd",
        "Top 10 States with Pincodes of Registered Users": "tusp"
    }

    # Retrieve the list of tables from the database
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    table_names = [table[0] for table in tables]

    # Create a list of display names for the selectbox
    display_names = list(table_mapping.keys())

    # Display the tables in a dropdown selectbox
    st.markdown('<h3 style="font-size: 25px;">Select a table:</h3>', unsafe_allow_html=True)
    selected_display_name = st.selectbox("", display_names)

    # Retrieve the actual table name based on the selected display name
    selected_table = table_mapping[selected_display_name]

    # Perform operations on the selected table
    if selected_table in table_names:
        # Perform query and retrieve data
        query = f"SELECT * FROM {selected_table}"
        df = pd.read_sql(query, connection)

            
        # Generate insights based on the selected table and transaction
        if selected_display_name == "Statewise Various Payment Type of Transaction Amount and Count":
            # Create select box options
            years = (df['Year'].unique())
            quarters = (df['Quarter'].unique())
            transaction_names = (df['Transaction Name'].unique())
        
            # Sidebar select box
            selected_year = st.sidebar.selectbox('Select Year', years)
            selected_quarter = st.sidebar.selectbox('Select Quarter', quarters)
            selected_transaction = st.sidebar.selectbox('Select Transaction', transaction_names)

            # Filter data based on selected options
            filtered_df = df[(df['Year'] == selected_year) & (df['Quarter'] == selected_quarter) & (df['Transaction Name'] == selected_transaction)]

            # Visualize data using charts
            chart_type = st.sidebar.selectbox('Select Chart Type', ['Bar Chart', 'Pie Chart'])
           
            if chart_type == 'Bar Chart':
                fig = px.bar(filtered_df, x='State', y='Total Amount', color='State', title='Total Amount by State')
                fig.update_layout(height=750, width=1000,title_font=dict(size=24)) 
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("""<span style="font-size: 24px;">Total Amount by State (Bar Chart): By selecting "Bar Chart" as the chart type, 
                            the code generates a bar chart that visualizes the total amount of transactions (on the y-axis) for each state (on the x-axis). 
                            Each state is represented by a different color in the chart. This visualization helps you compare the total transaction amounts across
                            different states, allowing you to identify states with higher or lower transaction volumes.</span>""", unsafe_allow_html=True)
            elif chart_type == 'Pie Chart':
                fig = px.pie(filtered_df, values='Total Count', names='State', title='Total Count by State')
                fig.update_layout(height=750, width=1000, title_font=dict(size=24)) 
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("""<span style="font-size: 24px;">By selecting "Pie Chart" as the chart type, 
                                the code generates a pie chart that illustrates the distribution of total transaction counts among the different states.
                                Each state is represented by a slice of the pie, with the size of the slice indicating the proportion of total counts it represents. 
                                This visualization provides an overview of the relative transaction volumes across states.</span>""", unsafe_allow_html=True)
                                         
        if selected_display_name == "Statewise User Count by Mobile Brand":
            # Create select box options
            years = (df['Year'].unique())
            quarters = (df['Quarter'].unique())
            brands = (df['Mobile Brand'].unique())

            # Sidebar select box
            selected_year = st.sidebar.selectbox('Select Year', years)
            selected_quarter = st.sidebar.selectbox('Select Quarter', quarters)
            selected_brand = st.sidebar.selectbox('Select Mobile Brand', brands)

            # Filter data based on selected options
            filtered_df = df[(df['Year'] == selected_year) & (df['Quarter'] == selected_quarter) & (df['Mobile Brand'] == selected_brand)]

            # Visualize data using charts
            chart_type = st.sidebar.selectbox('Select Chart Type', ['Bar Chart', 'Pie Chart'])

            if chart_type == 'Bar Chart':
                fig = px.bar(filtered_df, x='State', y='User Count', color='State', title='User Count by State')
                fig.update_layout(height=750, width=1000,title_font=dict(size=24)) 
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("""<span style="font-size: 24px;">By selecting "Bar Chart" as the chart type in the sidebar,
                            The chart represents the user count by state, with each state distinguished by a different color. 
                            This visualization provides a clear comparison of user counts across different states for the selected 
                            mobile brand, allowing you to identify any variations or trends.</span>""", unsafe_allow_html=True)
            elif chart_type == 'Pie Chart':
                fig = px.pie(filtered_df, values='Percentage', names='State', title='Percentage by State')
                fig.update_layout(height=750, width=1000,title_font=dict(size=24))
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("""<span style="font-size: 24px;">By selecting "Pie Chart" as the chart type in the sidebar. 
                            The chart represents the percentage distribution by state. Each state is represented as a slice of the pie,
                            and the size of each slice corresponds to the percentage value. This visualization helps you understand the relative proportions
                            of user counts for the selected mobile brand in different states.</span>""", unsafe_allow_html=True)
                            
        if selected_display_name == "Districtwise Total Transaction Count and Amount":
            # Create select box options
            years = (df['Year'].unique())
            quarters = (df['Quarter'].unique())
            states = (df['State'].unique())

            # Sidebar select box
            selected_year = st.sidebar.selectbox('Select Year', years)
            selected_quarter = st.sidebar.selectbox('Select Quarter', quarters)
            selected_state = st.sidebar.selectbox('Select State', states)

            # Filter data based on selected options
            filtered_df = df[(df['Year'] == selected_year) & (df['Quarter'] == selected_quarter) & (df['State'] == selected_state)]

            # Visualize data using charts
            chart_type = st.sidebar.selectbox('Select Chart Type', ['Bar Chart', 'Pie Chart'])

            if chart_type == 'Bar Chart':
                fig = px.bar(filtered_df, x='District', y='Total Amount', color='District', title='Total Amount by District')
                fig.update_layout(height=750, width=1000,title_font=dict(size=24)) 
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("""<span style="font-size: 24px;"> By selecting "Bar Chart" as the chart type in the sidebar.
                            The chart represents the total amount of transactions by district, with each district distinguished by a different color. 
                            This visualization provides a clear comparison of transaction amounts across different districts within the selected state, 
                            enabling you to identify variations or trends in transaction volumes.</span>""", unsafe_allow_html=True)
            elif chart_type == 'Pie Chart':
                fig = px.pie(filtered_df, values='Total Count', names='District', title='Total Count by District')
                fig.update_layout(height=750, width=1000,title_font=dict(size=24)) 
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("""<span style="font-size: 24px;"> By selecting "Pie Chart" as the chart type in the sidebar.
                            The chart represents the total count of transactions by district as a percentage. Each district is represented as a 
                            slice of the pie, and the size of each slice corresponds to the percentage value. This visualization helps you understand 
                            the relative distribution of transaction counts across different districts within 
                            the selected state.</span>""", unsafe_allow_html=True)

        if selected_display_name == "Districtwise Registered User Count":
            # Create select box options
            years = (df['Year'].unique())
            quarters = (df['Quarter'].unique())
            states = (df['State'].unique())

            # Sidebar select box
            selected_year = st.sidebar.selectbox('Select Year', years)
            selected_quarter = st.sidebar.selectbox('Select Quarter', quarters)
            selected_state = st.sidebar.selectbox('Select State', states)

            # Filter data based on selected options
            filtered_df = df[(df['Year'] == selected_year) & (df['Quarter'] == selected_quarter) & (df['State'] == selected_state)]

            # Visualize data using charts
            chart_type = st.sidebar.selectbox('Select Chart Type', ['Bar Chart', 'Pie Chart'])

            if chart_type == 'Bar Chart':
                fig = px.bar(filtered_df, x='District', y='Registered Users', color='District', title='Registered Users by District')
                st.plotly_chart(fig, use_container_width=True)
                fig.update_layout(height=750, width=1000,title_font=dict(size=24))
                st.markdown("""<span style="font-size: 24px;"> By selecting "Bar Chart" as the chart type in the sidebar. 
                            The chart represents the registered user count by district, with each district distinguished by a different color. 
                            This visualization provides a clear comparison of user counts across different districts within the selected state,
                            allowing you to identify variations or trends in user registrations.</span>""", unsafe_allow_html=True)
                 
            elif chart_type == 'Pie Chart':
                fig = px.pie(filtered_df, values='App Opened', names='District', title='App Opened by District')
                st.plotly_chart(fig, use_container_width=True)
                fig.update_layout(height=750, width=1000,title_font=dict(size=24))
                st.markdown("""<span style="font-size: 24px;">By selecting "Pie Chart" as the chart type in the sidebar.
                            The chart represents the app usage by district as a percentage. Each district is represented as a slice of the pie, 
                            and the size of each slice corresponds to the percentage value. This visualization helps you understand the relative 
                            distribution of app usage across different districts within the selected state.</span>""", unsafe_allow_html=True) 

        if selected_display_name == "Top 10 States with Districts of Total Transaction Amount and Count":
            # Create select box options
            years = sorted(df['Year'].unique())
            quarters = sorted(df['Quarter'].unique())

            # Sidebar select box for year and quarter
            selected_year = st.sidebar.selectbox('Select Year', years)
            selected_quarter = st.sidebar.selectbox('Select Quarter', quarters)

            # Filter data based on selected year and quarter
            filtered_df = df[(df['Year'] == selected_year) & (df['Quarter'] == selected_quarter)]

            # Calculate the total transaction amount by state
            state_amounts = filtered_df.groupby('State')['Total Amount'].sum().reset_index()
            state_amounts = state_amounts.sort_values('Total Amount', ascending=False)
            top_states = state_amounts.head(10)['State'].tolist()
    
            # Sidebar select box for state
            selected_state = st.sidebar.selectbox('Select State', top_states)

            # Filter data based on selected state
            state_filtered_df = filtered_df[filtered_df['State'] == selected_state]

            # Visualize data using charts
            chart_type = st.sidebar.selectbox('Select Chart Type', ['Bar Chart', 'Pie Chart'])
            
            st.markdown("""<span style="font-size: 24px;">Ranking of States: The top 10 states with the highest total transaction amounts are displayed 
                        in the select box for state selection. This ranking helps identify the states with the most significant transaction volumes within 
                        the selected year and quarter.</span>""", unsafe_allow_html=True)
            
            if chart_type == 'Bar Chart':
                fig = px.bar(state_filtered_df, x='District', y='Total Amount', color='District', title=f'Total Amount by District in {selected_state}')
                st.plotly_chart(fig, use_container_width=True)
                fig.update_layout(height=750, width=1000,title_font=dict(size=24))
                st.markdown("""<span style="font-size: 24px;">By selecting "Bar Chart" as the chart type in the sidebar.
                            The chart represents the total transaction amount by district within the selected state. Each district is distinguished
                            by a different color, and the bar height represents the transaction amount. This visualization provides a clear comparison 
                            of transaction amounts across different districts within the chosen state.</span>""", unsafe_allow_html=True)
                
            elif chart_type == 'Pie Chart':
                fig = px.pie(state_filtered_df, values='Total Count', names='District', title=f'Total Count by District in {selected_state}')
                st.plotly_chart(fig, use_container_width=True)
                fig.update_layout(height=750, width=1000,title_font=dict(size=24))
                st.markdown("""<span style="font-size: 24px;"> By selecting "Pie Chart" as the chart type in the sidebar. The chart represents
                            the total transaction count by district within the selected state as a percentage. Each district is represented as a 
                            slice of the pie, and the size of each slice corresponds to the percentage value. This visualization helps you understand
                            the relative distribution of transaction counts across different districts within the 
                            chosen state.</span>""", unsafe_allow_html=True)

        if selected_display_name == "Top 10 States with Pincodes of Total Transaction Amount and Count":
            # Create select box options
            years = sorted(df['Year'].unique())
            quarters = sorted(df['Quarter'].unique())

            # Sidebar select box for year and quarter
            selected_year = st.sidebar.selectbox('Select Year', years)
            selected_quarter = st.sidebar.selectbox('Select Quarter', quarters)

            # Filter data based on selected year and quarter
            filtered_df = df[(df['Year'] == selected_year) & (df['Quarter'] == selected_quarter)]

            # Calculate the total transaction amount by state
            state_amounts = filtered_df.groupby('State')['Total Amount'].sum().reset_index()
            state_amounts = state_amounts.sort_values('Total Amount', ascending=False)
            top_states = state_amounts.head(10)['State'].tolist()

            # Sidebar select box for state
            selected_state = st.sidebar.selectbox('Select State', top_states)

            # Filter data based on selected state
            state_filtered_df = filtered_df[filtered_df['State'] == selected_state]

            # Visualize data using charts
            chart_type = st.sidebar.selectbox('Select Chart Type', ['Bar Chart', 'Pie Chart'])
            st.markdown("""<span style="font-size: 24px;">Ranking of States: The top 10 states with the highest total transaction amounts are displayed in 
                        the select box for state selection. This ranking helps identify the states with the most significant transaction volumes 
                        within the selected year and quarter.</span>""", unsafe_allow_html=True)

            if chart_type == 'Bar Chart':
                fig = px.bar(state_filtered_df, x='Pincode', y='Total Amount', color='Pincode', title=f'Total Amount by Pincode in {selected_state}')
                st.plotly_chart(fig, use_container_width=True)
                fig.update_layout(height=750, width=1000,title_font=dict(size=24))
                st.markdown("""<span style="font-size: 24px;"> By selecting "Bar Chart" as the chart type in the sidebar. 
                            The chart represents the total transaction amount by pincode within the selected state.
                            Each pincode is distinguished by a different color, and the bar height represents the transaction amount. 
                            This visualization provides a clear comparison of transaction amounts across different pincodes
                            within the chosen state.</span>""", unsafe_allow_html=True)
            elif chart_type == 'Pie Chart':
                fig = px.pie(state_filtered_df, values='Total Count', names='Pincode', title=f'Total Count by Pincode in {selected_state}')
                st.plotly_chart(fig, use_container_width=True)
                fig.update_layout(height=750, width=1000,title_font=dict(size=24))
                st.markdown("""<span style="font-size: 24px;">By selecting "Pie Chart" as the chart type in the sidebar. 
                            The chart represents the total transaction count by pincode within the selected state as a percentage. 
                            Each pincode is represented as a slice of the pie, and the size of each slice corresponds to the percentage value.
                            This visualization helps you understand the relative distribution of transaction counts across different pincodes within
                            the chosen state.</span>""", unsafe_allow_html=True)

        if selected_display_name == "Top 10 States with Districts of Registered Users":
            
            # Create select box options
            years = sorted(df['Year'].unique())
            quarters = sorted(df['Quarter'].unique())

            # Sidebar select box for year and quarter
            selected_year = st.sidebar.selectbox('Select Year', years)
            selected_quarter = st.sidebar.selectbox('Select Quarter', quarters)

            # Filter data based on selected year and quarter
            filtered_df = df[(df['Year'] == selected_year) & (df['Quarter'] == selected_quarter)]

            # Calculate the total registered users by state
            state_users = filtered_df.groupby('State')['Registered Users'].sum().reset_index()
            state_users = state_users.sort_values('Registered Users', ascending=False)
            top_states = state_users.head(10)['State'].tolist()

            # Sidebar select box for state
            selected_state = st.sidebar.selectbox('Select State', top_states)

            # Filter data based on selected state
            state_filtered_df = filtered_df[filtered_df['State'] == selected_state]

            # Visualize data using charts
            chart_type = st.sidebar.selectbox('Select Chart Type', ['Bar Chart', 'Pie Chart'])
            st.markdown("""<span style="font-size: 24px;">Ranking of States: The top 10 states with the highest number of registered users are
                        displayed in the select box for state selection. This ranking helps identify the states with the largest user bases within
                        the selected year and quarter.</span>""", unsafe_allow_html=True)

            if chart_type == 'Bar Chart':
                fig = px.bar(state_filtered_df, x='District', y='Registered Users', color='District', title=f'Registered Users by District in {selected_state}')
                st.plotly_chart(fig, use_container_width=True)
                fig.update_layout(height=750, width=1000,title_font=dict(size=24))
                st.markdown("""<span style="font-size: 24px;">By selecting "Bar Chart" as the chart type in the sidebar.
                            The chart represents the number of registered users by district within the selected state.
                            Each district is distinguished by a different color, and the bar height represents the number of registered users.
                            This visualization provides a clear comparison of user counts across different
                            districts within the chosen state.</span>""", unsafe_allow_html=True)
            elif chart_type == 'Pie Chart':
                fig = px.pie(state_filtered_df, values='Registered Users', names='District', title=f'Registered Users by District in {selected_state}')
                st.plotly_chart(fig, use_container_width=True)
                fig.update_layout(height=750, width=1000,title_font=dict(size=24))
                st.markdown("""<span style="font-size: 24px;"> By selecting "Pie Chart" as the chart type in the sidebar.
                            The chart represents the distribution of registered users by district within the selected state as a percentage. 
                            Each district is represented as a slice of the pie, and the size of each slice corresponds to the percentage value.
                            This visualization helps you understand the relative distribution of registered users across different districts within
                            the chosen state.</span>""", unsafe_allow_html=True)

        if selected_display_name == "Top 10 States with Pincodes of Registered Users":
            # Create select box options
            years = sorted(df['Year'].unique())
            quarters = sorted(df['Quarter'].unique())

            # Sidebar select box for year and quarter
            selected_year = st.sidebar.selectbox('Select Year', years)
            selected_quarter = st.sidebar.selectbox('Select Quarter', quarters)

            # Filter data based on selected year and quarter
            filtered_df = df[(df['Year'] == selected_year) & (df['Quarter'] == selected_quarter)]

            # Calculate the total registered users by state
            state_users = filtered_df.groupby('State')['Registered Users'].sum().reset_index()
            state_users = state_users.sort_values('Registered Users', ascending=False)
            top_states = state_users.head(10)['State'].tolist()
            
            # Sidebar select box for state
            selected_state = st.sidebar.selectbox('Select State', top_states)

            # Filter data based on selected state
            state_filtered_df = filtered_df[filtered_df['State'] == selected_state]
            
            # Visualize data using charts
            chart_type = st.sidebar.selectbox('Select Chart Type', ['Bar Chart', 'Pie Chart'])
            
            st.markdown("""<span style="font-size: 24px;"> Ranking of States: The top 10 states with the highest number of registered users 
                        are displayed in the select box for state selection. This ranking helps identify the states with the largest user bases
                        within the selected year and quarter.</span>""", unsafe_allow_html=True)
            
            if chart_type == 'Bar Chart':
                fig = px.bar(state_filtered_df, x='Pincode', y='Registered Users', color='Pincode', title=f'Registered Users by Pincode in {selected_state}')
                st.plotly_chart(fig, use_container_width=True)
                fig.update_layout(height=750, width=1000,title_font=dict(size=24))
                st.markdown("""<span style="font-size: 24px;"> By selecting "Bar Chart" as the chart type in the sidebar.
                            The chart represents the number of registered users by pincode within the selected state. 
                            Each pincode is distinguished by a different color, and the bar height represents the number of registered users.
                            This visualization provides a clear comparison of user counts across different 
                            pincodes within the chosen state.</span>""", unsafe_allow_html=True)
                
            elif chart_type == 'Pie Chart':
                fig = px.pie(state_filtered_df, values='Registered Users', names='Pincode', title=f'Registered Users by Pincode in {selected_state}')
                st.plotly_chart(fig, use_container_width=True)
                fig.update_layout(height=750, width=1000,title_font=dict(size=24))
                st.markdown("""<span style="font-size: 24px;">By selecting "Pie Chart" as the chart type in the sidebar. 
                            The chart represents the distribution of registered users by pincode within the selected state as a percentage.
                            Each pincode is represented as a slice of the pie, and the size of each slice corresponds to the percentage value. 
                            This visualization helps you understand the relative distribution of registered users across different pincodes within 
                            the chosen state.</span>""", unsafe_allow_html=True)
                 
    st.markdown("""<span style="font-size: 24px;">These insights provide valuable information about transaction trends,
                user adoption, and regional variations within the provided datasets. They can help businesses and analysts 
                understand market dynamics, user behavior, and opportunities for growth in different states, districts, mobile brands,
                and payment types.</span>""", unsafe_allow_html=True)    
 
if selected_menu_item == "Geo visualization":    
    st.subheader('Statewise Transaction Amount and Count :')
    state_mapping = {'andaman-&-nicobar-islands': 'Andaman & Nicobar','arunachal-pradesh': 'Arunachal Pradesh',
                    'andhra-pradesh':'Andhra Pradesh','assam': 'Assam','bihar': 'Bihar','chandigarh': 'Chandigarh',
                    'chhattisgarh': 'Chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu': 'Dadra and Nagar Haveli and Daman and Diu',
                    'delhi': 'Delhi','goa': 'Goa','gujarat': 'Gujarat','haryana': 'Haryana',
                    'himachal-pradesh': 'Himachal Pradesh','jammu-&-kashmir': 'Jammu & Kashmir','jharkhand': 'Jharkhand',
                    'karnataka': 'Karnataka','kerala': 'Kerala','lakshadweep': 'Lakshadweep','ladakh' : 'Ladakh',
                    'madhya-pradesh': 'Madhya Pradesh','maharashtra': 'Maharashtra','manipur': 'Manipur','meghalaya': 'Meghalaya',
                    'mizoram': 'Mizoram','nagaland': 'Nagaland','odisha': 'Odisha','puducherry': 'Puducherry','punjab': 'Punjab',
                    'rajasthan': 'Rajasthan','sikkim': 'Sikkim','tamil-nadu': 'Tamil Nadu','telangana': 'Telangana',
                    'tripura': 'Tripura','uttar-pradesh': 'Uttar Pradesh','uttarakhand': 'Uttarakhand','west-bengal': 'West Bengal'}


    @st.cache_data
    def fetch_data_from_database(selected_year):
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Ajith568.',
            database='phonepe'
        )

        # Execute the SQL query to retrieve the data for the selected year
        query = f"SELECT `state`, `Year`, `Quarter`, `Transaction Name`, `Total Count`, `Total Amount` FROM ats WHERE `Year` = {selected_year}"
        cursor = connection.cursor()
        cursor.execute(query)

        # Fetch all the rows from the resultset
        rows = cursor.fetchall()

        # Create a DataFrame from the fetched rows
        df = pd.DataFrame(rows, columns=['state', 'Year', 'Quarter', 'Transaction Name', 'Total Count', 'Total Amount'])

        # Perform the aggregation to calculate the sum of count and amount for each state and year
        df_agg = df.groupby(['state', 'Year']).agg({'Total Count': 'sum', 'Total Amount': 'sum'}).reset_index()
        df_agg.rename(columns={'Total Count': 'Transaction count', 'Total Amount': 'Transaction Amount'}, inplace=True)

        # Map the state names and ensure they match the format in the GeoJSON data
        df_agg['state'] = df_agg['state'].map(state_mapping)

        return df_agg


    # Load the GeoJSON data
    geojson_data = "C:\\Users\\vijai\Downloads\\map.geojson"
    gdf = gpd.read_file(geojson_data)

    # Create a selection box for the year
    st.markdown('<h3 style="font-size: 25px;">Select year :</h3>', unsafe_allow_html=True)
    selected_year = st.selectbox("", range(2018, 2023))

    # Fetch the data for the selected year
    df_agg = fetch_data_from_database(selected_year)

    # Merge the GeoJSON data with the aggregated data
    merged_data = gdf.merge(df_agg, left_on='ST_NM', right_on='state', how='left')

    # Extract centroid coordinates
    merged_data['latitude'] = merged_data['geometry'].centroid.y
    merged_data['longitude'] = merged_data['geometry'].centroid.x

    # Create a selection box for the data type
    st.markdown('<h3 style="font-size: 25px;">Select data to visualize :</h3>', unsafe_allow_html=True)
    selection = st.selectbox("", ['Transaction Amount', 'Transaction count'])

    # Create the geovisualization using Plotly
    fig = px.choropleth_mapbox(
        merged_data,
        geojson=merged_data.geometry,
        locations=merged_data.index,
        color=selection,
        mapbox_style="carto-positron",
        center={"lat": merged_data['latitude'].mean(), "lon": merged_data['longitude'].mean()},
        zoom=4,
        opacity=0.5
    )

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, width = 1200, height = 750)

    st.plotly_chart(fig)