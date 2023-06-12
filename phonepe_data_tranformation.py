#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import json
import pandas as pd
import mysql.connector
import csv


# In[2]:


def read_ats(path):
    state_list = os.listdir(path)
    columns = {'State': [], 'Year': [], 'Quarter': [], 'Transaction Name': [], 'Total Count': [], 'Total Amount': []}
    
    for i in state_list:
        path1 = os.path.join(path, i)
        path_year = os.listdir(path1)
        
        for j in path_year:
            path2 = os.path.join(path1, j)
            path_json = os.listdir(path2)
            
            for k in path_json:
                path_final = os.path.join(path2, k)
                with open(path_final, 'r') as f:
                    d = json.loads(f.read())
                    
                for data in d['data']['transactionData']:
                    columns['State'].append(i)
                    columns['Year'].append(j)
                    columns['Quarter'].append(int(k.strip('.json')))
                    name = data['name']
                    columns['Transaction Name'].append(name)
                    count = data['paymentInstruments'][0]['count']
                    columns['Total Count'].append(count)
                    amount = data['paymentInstruments'][0]['amount']
                    columns['Total Amount'].append(amount)
                
    df = pd.DataFrame(columns)
    return df


path = "H:\\Guvi\\Project\\DS_Phonepe Pulse Data Visualization and Exploration A User-Friendly Tool Using Streamlit and Plotly\\pulse\\data\\aggregated\\transaction\\country\\india\\state\\"
df = read_ats(path)
df.to_csv(r"H:\Guvi\Project\DS_Phonepe Pulse Data Visualization and Exploration A User-Friendly Tool Using Streamlit and Plotly\data_csv\ATS_18-22.csv")


# In[3]:


def ats_mysql(csv_path):
    # Connect to MySQL database
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Ajith568.',
        auth_plugin='mysql_native_password',
        database='phonepe'
    )
    mycursor = mydb.cursor()

    # Create table if it doesn't exist
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS ATS (
            State VARCHAR(255) NOT NULL,
            Year INT NOT NULL,
            Quarter INT NOT NULL,
            `Transaction Name` VARCHAR(255) NOT NULL,
            `Total Count` INT NOT NULL,
            `Total Amount` FLOAT NOT NULL
        );
    """)

    # Open CSV file and read the data
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # Iterate over each row and insert into MySQL table
        for row in csv_reader:
            mycursor.execute("""
                INSERT INTO ATS (State, Year, Quarter, `Transaction Name`, `Total Count`, `Total Amount`)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (row['State'], row['Year'], row['Quarter'], row['Transaction Name'], row['Total Count'], row['Total Amount']))

    # Commit the changes to the database and close the connection
    mydb.commit()
    mydb.close()

# Call the function and provide the CSV file path
csv_path = "H:\\Guvi\\Project\\DS_Phonepe Pulse Data Visualization and Exploration A User-Friendly Tool Using Streamlit and Plotly\\data_csv\\ATS_18-22.csv"
ats_mysql(csv_path)


# In[ ]:





# In[4]:


def read_aus(path):
    state_list = os.listdir(path)
    columns = {'State': [], 'Year': [], 'Quarter': [], 'Mobile Brand': [], 'User Count': [], 'Percentage': []}
    
    for i in state_list:
        path1 = os.path.join(path, i)
        path_year = os.listdir(path1)
        
        for j in path_year:
            path2 = os.path.join(path1, j)
            path_json = os.listdir(path2)
            
            for k in path_json:
                path_final = os.path.join(path2, k)
                
                with open(path_final, 'r') as f:
                    d = json.load(f)
                    
                if d['data']['usersByDevice'] is not None:
                    for data in d['data']['usersByDevice']:               
                        columns['State'].append(i)
                        columns['Year'].append(j)
                        columns['Quarter'].append(int(k.strip('.json')))
                        columns['Mobile Brand'].append(data['brand'])
                        columns['User Count'].append(data['count'])
                        columns['Percentage'].append(data['percentage'])
                else:
                    pass
                
    df = pd.DataFrame(columns)
    return df

# Usage:
path = "H:\\Guvi\\Project\\DS_Phonepe Pulse Data Visualization and Exploration A User-Friendly Tool Using Streamlit and Plotly\\pulse\\data\\aggregated\\user\\country\\india\\state\\"
df = read_aus(path)
df.to_csv(r"H:\Guvi\Project\DS_Phonepe Pulse Data Visualization and Exploration A User-Friendly Tool Using Streamlit and Plotly\data_csv\AUS_18-22.csv")


# In[5]:


def aus_mysql(csv_path):
    # Connect to MySQL database
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Ajith568.',
        auth_plugin='mysql_native_password',
        database='phonepe'
    )
    mycursor = mydb.cursor()

    # Create table if it doesn't exist
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS AUS (
            State VARCHAR(255) NOT NULL,
            Year INT NOT NULL,
            Quarter INT NOT NULL,
            `Mobile Brand` VARCHAR(255) NOT NULL,
            `User Count` INT NOT NULL,
            `Percentage` FLOAT NOT NULL
        );
    """)

    # Open CSV file and read the data
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # Iterate over each row and insert into MySQL table
        for row in csv_reader:
            mycursor.execute("""
                INSERT INTO AUS (State, Year, Quarter, `Mobile Brand`, `User Count`, `Percentage`)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (row['State'], row['Year'], row['Quarter'], row['Mobile Brand'], row['User Count'], row['Percentage']))

    # Commit the changes to the database and close the connection
    mydb.commit()
    mydb.close()

# Call the function and provide the CSV file path
csv_path = "H:\\Guvi\\Project\\DS_Phonepe Pulse Data Visualization and Exploration A User-Friendly Tool Using Streamlit and Plotly\\data_csv\\AUS_18-22.csv"
aus_mysql(csv_path)


# In[ ]:





# In[6]:


def read_mts(path):
    state_list = os.listdir(path)
    columns = {'State': [], 'District': [], 'Year': [], 'Quarter': [], 'Total Count': [], 'Total Amount': []}
    
    for i in state_list:
        path1 = os.path.join(path, i)
        path_year = os.listdir(path1)
        
        for j in path_year:
            path2 = os.path.join(path1, j)
            path_json = os.listdir(path2)
            
            for k in path_json:
                path_final = os.path.join(path2, k)
                with open(path_final, 'r') as f:
                    d = json.load(f)
                    
                for data in d['data']['hoverDataList']:
                    columns['State'].append(i)
                    columns['District'].append(data['name'])
                    columns['Year'].append(j)
                    columns['Quarter'].append(int(k.strip('.json')))
                    count = data['metric'][0]['count']
                    columns['Total Count'].append(count)
                    amount = data['metric'][0]['amount']
                    columns['Total Amount'].append(amount)

    df = pd.DataFrame(columns)
    return df

# Usage:
path = "H:\\Guvi\\Project\\DS_Phonepe Pulse Data Visualization and Exploration A User-Friendly Tool Using Streamlit and Plotly\\pulse\\data\\map\\transaction\\hover\\country\\india\\state\\"
df = read_mts(path)
df.to_csv(r"H:\Guvi\Project\DS_Phonepe Pulse Data Visualization and Exploration A User-Friendly Tool Using Streamlit and Plotly\data_csv\MTS_18-22.csv")


# In[7]:


def mts_mysql(csv_path):
    # Connect to MySQL database
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Ajith568.',
        auth_plugin='mysql_native_password',
        database='phonepe'
    )
    mycursor = mydb.cursor()

    # Create table if it doesn't exist
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS MTS (
            State VARCHAR(255) NOT NULL,
            District VARCHAR(255) NOT NULL,
            Year INT NOT NULL,
            Quarter INT NOT NULL,
            `Total Count` INT NOT NULL,
            `Total Amount` FLOAT NOT NULL
        );
    """)

    # Open CSV file and read the data
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # Iterate over each row and insert into MySQL table
        for row in csv_reader:
            mycursor.execute("""
                INSERT INTO MTS (State, District, Year, Quarter, `Total Count`, `Total Amount`)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (row['State'], row['District'], row['Year'], row['Quarter'], row['Total Count'], row['Total Amount']))

    # Commit the changes to the database and close the connection
    mydb.commit()
    mydb.close()

# Call the function and provide the CSV file path
csv_path = r"H:\Guvi\Project\DS_Phonepe Pulse Data Visualization and Exploration A User-Friendly Tool Using Streamlit and Plotly\data_csv\MTS_18-22.csv"
mts_mysql(csv_path)


# In[ ]:





# In[8]:


def read_mus(path):
    state_list = os.listdir(path)
    columns = {'State': [], 'District': [], 'Year': [], 'Quarter': [], 'Registered Users': [], 'App Opened': []}

    for i in state_list:
        path1 = os.path.join(path, i)
        path_year = os.listdir(path1)

        for j in path_year:
            path2 = os.path.join(path1, j)
            path_json = os.listdir(path2)

            for k in path_json:
                path_final = os.path.join(path2, k)
                with open(path_final, 'r') as f:
                    d = json.load(f)

                hover_data = d['data']['hoverData']
                for district, values in hover_data.items():
                    columns['State'].append(i)
                    columns['District'].append(district.title())
                    columns['Year'].append(j)
                    columns['Quarter'].append(int(k.strip('.json')))
                    columns['Registered Users'].append(values['registeredUsers'])
                    columns['App Opened'].append(values['appOpens'])

    df = pd.DataFrame(columns)
    return df

# Usage:
path = "H:\\Guvi\\Project\\DS_Phonepe Pulse Data Visualization and Exploration A User-Friendly Tool Using Streamlit and Plotly\\pulse\\data\\map\\user\\hover\\country\\india\\state\\"
df = read_mus(path)
df.to_csv(r"H:\Guvi\Project\DS_Phonepe Pulse Data Visualization and Exploration A User-Friendly Tool Using Streamlit and Plotly\data_csv\MUS_18-22.csv")


# In[9]:


def mus_mysql(csv_path):
    # Connect to MySQL database
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Ajith568.',
        auth_plugin='mysql_native_password',
        database='phonepe'
    )
    mycursor = mydb.cursor()

    # Create table if it doesn't exist
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS MUS (
            State VARCHAR(255) NOT NULL,
            District VARCHAR(255) NOT NULL,
            Year INT NOT NULL,
            Quarter INT NOT NULL,
            `Registered Users` INT NOT NULL,
            `App Opened` INT NOT NULL
        );
    """)

    # Open CSV file and read the data
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # Iterate over each row and insert into MySQL table
        for row in csv_reader:
            mycursor.execute("""
                INSERT INTO MUS (State, District, Year, Quarter, `Registered Users`, `App Opened`)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (row['State'], row['District'], row['Year'], row['Quarter'], row['Registered Users'], row['App Opened']))

    # Commit the changes to the database and close the connection
    mydb.commit()
    mydb.close()

# Call the function and provide the CSV file path
csv_path = r"H:\Guvi\Project\DS_Phonepe Pulse Data Visualization and Exploration A User-Friendly Tool Using Streamlit and Plotly\data_csv\MUS_18-22.csv"
mus_mysql(csv_path)


# In[ ]:





# In[11]:


def read_ttsd(path):
    state_list = os.listdir(path)
    columns = {'State': [], 'District': [], 'Year': [], 'Quarter': [], 'Total Count': [], 'Total Amount': []}

    for i in state_list:
        path1 = os.path.join(path, i)
        path_year = os.listdir(path1)

        for j in path_year:
            path2 = os.path.join(path1, j)
            path_json = os.listdir(path2)

            for k in path_json:
                path_final = os.path.join(path2, k)
                with open(path_final, 'r') as f:
                    d = json.load(f)

                for data in d['data']['districts']:
                    columns['State'].append(i)
                    columns['District'].append(data['entityName'])
                    columns['Year'].append(j)
                    columns['Quarter'].append(int(k.strip('.json')))
                    count = data['metric']['count']
                    columns['Total Count'].append(count)
                    amount = data['metric']['amount']
                    columns['Total Amount'].append(amount)

    df = pd.DataFrame(columns)
    return df

# Usage:
path = "H:\\Guvi\\Project\\DS_Phonepe Pulse Data Visualization and Exploration A User-Friendly Tool Using Streamlit and Plotly\\pulse\\data\\top\\transaction\\country\\india\\state\\"
df = read_ttsd(path)
df.to_csv(r"H:\Guvi\Project\DS_Phonepe Pulse Data Visualization and Exploration A User-Friendly Tool Using Streamlit and Plotly\data_csv\TTSD_18-22.csv")


# In[12]:


def ttsd_mysql(csv_path):
    # Connect to MySQL database
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Ajith568.',
        auth_plugin='mysql_native_password',
        database='phonepe'
    )
    mycursor = mydb.cursor()

    # Create table if it doesn't exist
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS TTSD (
            State VARCHAR(255) NOT NULL,
            District VARCHAR(255) NOT NULL,
            Year INT NOT NULL,
            Quarter INT NOT NULL,
            `Total Count` INT NOT NULL,
            `Total Amount` FLOAT NOT NULL
        );
    """)

    # Open CSV file and read the data
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # Iterate over each row and insert into MySQL table
        for row in csv_reader:
            mycursor.execute("""
                INSERT INTO TTSD (State, District, Year, Quarter, `Total Count`, `Total Amount`)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (row['State'], row['District'], row['Year'], row['Quarter'], row['Total Count'], row['Total Amount']))

    # Commit the changes to the database and close the connection
    mydb.commit()
    mydb.close()

# Call the function and provide the CSV file path
csv_path = r"H:\Guvi\Project\DS_Phonepe Pulse Data Visualization and Exploration A User-Friendly Tool Using Streamlit and Plotly\data_csv\TTSD_18-22.csv"
ttsd_mysql(csv_path)


# In[ ]:





# In[13]:


def read_ttsp(path):
    state_list = os.listdir(path)
    columns = {'State': [], 'Pincode': [], 'Year': [], 'Quarter': [], 'Total Count': [], 'Total Amount': []}

    for i in state_list:
        path1 = os.path.join(path, i)
        path_year = os.listdir(path1)

        for j in path_year:
            path2 = os.path.join(path1, j)
            path_json = os.listdir(path2)

            for k in path_json:
                path_final = os.path.join(path2, k)
                with open(path_final, 'r') as f:
                    d = json.load(f)

                for data in d['data']['pincodes']:
                    columns['State'].append(i)
                    columns['Pincode'].append(data['entityName'])
                    columns['Year'].append(j)
                    columns['Quarter'].append(int(k.strip('.json')))
                    count = data['metric']['count']
                    columns['Total Count'].append(count)
                    amount = data['metric']['amount']
                    columns['Total Amount'].append(amount)

    df = pd.DataFrame(columns)
    return df

# Usage:
path = "H:\\Guvi\\Project\\DS_Phonepe Pulse Data Visualization and Exploration A User-Friendly Tool Using Streamlit and Plotly\\pulse\\data\\top\\transaction\\country\\india\\state\\"
df = read_ttsp(path)
df.to_csv(r"H:\Guvi\Project\DS_Phonepe Pulse Data Visualization and Exploration A User-Friendly Tool Using Streamlit and Plotly\data_csv\TTSP_18-22.csv")


# In[14]:


def ttsp_mysql(csv_path):
    # Connect to MySQL database
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Ajith568.',
        auth_plugin='mysql_native_password',
        database='phonepe'
    )
    mycursor = mydb.cursor()

    # Create table if it doesn't exist
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS TTSP (
            State VARCHAR(255) NOT NULL,
            Pincode VARCHAR(255) NOT NULL,
            Year INT NOT NULL,
            Quarter INT NOT NULL,
            `Total Count` INT NOT NULL,
            `Total Amount` FLOAT NOT NULL
        );
    """)

    # Open CSV file and read the data
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # Iterate over each row and insert into MySQL table
        for row in csv_reader:
            mycursor.execute("""
                INSERT INTO TTSP (State, Pincode, Year, Quarter, `Total Count`, `Total Amount`)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (row['State'], row['Pincode'], row['Year'], row['Quarter'], row['Total Count'], row['Total Amount']))

    # Commit the changes to the database and close the connection
    mydb.commit()
    mydb.close()

# Call the function and provide the CSV file path
csv_path = r"H:\Guvi\Project\DS_Phonepe Pulse Data Visualization and Exploration A User-Friendly Tool Using Streamlit and Plotly\data_csv\TTSP_18-22.csv"
ttsp_mysql(csv_path)


# In[ ]:





# In[15]:


def read_tusd(path):
    state_list = os.listdir(path)
    columns = {'State': [], 'District': [], 'Year': [], 'Quarter': [], 'Registered Users': []}

    for i in state_list:
        path1 = os.path.join(path, i)
        path_year = os.listdir(path1)

        for j in path_year:
            path2 = os.path.join(path1, j)
            path_json = os.listdir(path2)

            for k in path_json:
                path_final = os.path.join(path2, k)
                with open(path_final, 'r') as f:
                    d = json.load(f)

                for data in d['data']['districts']:
                    columns['State'].append(i)
                    columns['District'].append(data['name'])
                    columns['Year'].append(j)
                    columns['Quarter'].append(int(k.strip('.json')))
                    columns['Registered Users'].append(data['registeredUsers'])

    df = pd.DataFrame(columns)
    return df

# Usage:
path = "H:\\Guvi\\Project\\DS_Phonepe Pulse Data Visualization and Exploration A User-Friendly Tool Using Streamlit and Plotly\\pulse\\data\\top\\user\\country\\india\\state\\"
df = read_tusd(path)
df.to_csv(r"H:\Guvi\Project\DS_Phonepe Pulse Data Visualization and Exploration A User-Friendly Tool Using Streamlit and Plotly\data_csv\TUSD_18-22.csv")


# In[16]:


def tusd_mysql(csv_path):
    # Connect to MySQL database
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Ajith568.',
        auth_plugin='mysql_native_password',
        database='phonepe'
    )
    mycursor = mydb.cursor()

    # Create table if it doesn't exist
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS TUSD (
            State VARCHAR(255) NOT NULL,
            District VARCHAR(255) NOT NULL,
            Year INT NOT NULL,
            Quarter INT NOT NULL,
            `Registered Users` INT NOT NULL
        );
    """)

    # Open CSV file and read the data
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # Iterate over each row and insert into MySQL table
        for row in csv_reader:
            mycursor.execute("""
                INSERT INTO TUSD (State, District, Year, Quarter, `Registered Users`)
                VALUES (%s, %s, %s, %s, %s)
            """, (row['State'], row['District'], row['Year'], row['Quarter'], row['Registered Users']))

    # Commit the changes to the database and close the connection
    mydb.commit()
    mydb.close()

# Call the function and provide the CSV file path
csv_path = r"H:\Guvi\Project\DS_Phonepe Pulse Data Visualization and Exploration A User-Friendly Tool Using Streamlit and Plotly\data_csv\TUSD_18-22.csv"
tusd_mysql(csv_path)


# In[ ]:





# In[17]:


def read_tusp(path):
    state_list = os.listdir(path)
    columns = {'State': [], 'Pincode': [], 'Year': [], 'Quarter': [], 'Registered Users': []}

    for i in state_list:
        path1 = os.path.join(path, i)
        path_year = os.listdir(path1)

        for j in path_year:
            path2 = os.path.join(path1, j)
            path_json = os.listdir(path2)

            for k in path_json:
                path_final = os.path.join(path2, k)
                with open(path_final, 'r') as f:
                    d = json.load(f)

                for data in d['data']['pincodes']:
                    columns['State'].append(i)
                    columns['Pincode'].append(data['name'])
                    columns['Year'].append(j)
                    columns['Quarter'].append(int(k.strip('.json')))
                    columns['Registered Users'].append(data['registeredUsers'])

    df = pd.DataFrame(columns)
    return df

# Usage:
path = "H:\\Guvi\\Project\\DS_Phonepe Pulse Data Visualization and Exploration A User-Friendly Tool Using Streamlit and Plotly\\pulse\\data\\top\\user\\country\\india\\state\\"
df = read_tusp(path)
df.to_csv(r"H:\Guvi\Project\DS_Phonepe Pulse Data Visualization and Exploration A User-Friendly Tool Using Streamlit and Plotly\data_csv\TUSP_18-22.csv")


# In[18]:


def tusp_mysql(csv_path):
    # Connect to MySQL database
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Ajith568.',
        auth_plugin='mysql_native_password',
        database='phonepe'
    )
    mycursor = mydb.cursor()

    # Create table if it doesn't exist
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS TUSP (
            State VARCHAR(255) NOT NULL,
            Pincode INT NOT NULL,
            Year INT NOT NULL,
            Quarter INT NOT NULL,
            `Registered Users` INT NOT NULL
        );
    """)

    # Open CSV file and read the data
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # Iterate over each row and insert into MySQL table
        for row in csv_reader:
            mycursor.execute("""
                INSERT INTO TUSP (State, Pincode, Year, Quarter, `Registered Users`)
                VALUES (%s, %s, %s, %s, %s)
            """, (row['State'], row['Pincode'], row['Year'], row['Quarter'], row['Registered Users']))

    # Commit the changes to the database and close the connection
    mydb.commit()
    mydb.close()

# Call the function and provide the CSV file path
csv_path = r"H:\Guvi\Project\DS_Phonepe Pulse Data Visualization and Exploration A User-Friendly Tool Using Streamlit and Plotly\data_csv\TUSP_18-22.csv"
tusp_mysql(csv_path)


# In[ ]:




