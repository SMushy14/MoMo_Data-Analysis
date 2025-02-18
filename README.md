Overview:
In this summative assignment, you will demonstrate your ability to design and develop an enterprise-level fullstack application. Your task is to process SMS data in XML format, clean and categorize the data, store it in a relational database, and build a frontend interface to analyze and visualize the data. This assignment tests your skills in backend data processing, database management, and frontend development.

You will be provided with an XML file containing approximately 1600 SMS messages of various types from the famous Mobile Payment Service Provider in Rwanda, MTN MoMoLinks to an external site.. Your goal is to process the data, load it into a database, and create an interactive dashboard to analyze and display insights derived from the SMS data. Who knows, MTN might be interested in what you have to show.

Learning Objectives:
By completing this assignment, you will:

Apply data cleaning and categorization techniques to extract meaningful insights from raw data.
Design and implement relational database schemas to store structured data.
Develop a backend to handle database operations and integrate it with a frontend application.
Build an interactive and user-friendly dashboard using HTML, CSS, and JavaScript.
Demonstrate end-to-end problem-solving skills in fullstack application development.
Deliverables:
Python/JS Scripts: For data cleaning, processing, and populating the database.
Database Schema: Design and implement a relational database to store SMS data.
Frontend Interface: A dashboard built with HTML, CSS, and JavaScript to visualize and interact with the data.
Documentation: A brief report explaining your approach, design decisions, and the functionality of your application.
Assignment Tasks:
1. Data Cleaning and Processing (Backend)
Data Extraction:

Parse the provided XML file using JavaScript or Python  libraries (e.g., xml.etree.ElementTree, lxml, or BeautifulSoup).
Extract and categorize SMS messages into types such as:
Incoming Money
Payments to Code Holders
Transfers to Mobile Numbers
Bank Deposits
Airtime Bill Payments
Cash Power Bill Payments
Transactions Initiated by Third Parties
Withdrawals from Agents
Bank Transfers
Internet and Voice Bundle Purchases
Data Cleaning:

Handle missing fields or erroneous data.
Normalize text data (e.g., converting amounts to integers, formatting dates).
Logging:

Log unprocessed or ignored messages into a separate file.
2. Database Design and Implementation
Relational Database:

Design a schema that captures all relevant fields for each transaction type.
Use SQLite, MySQL, or PostgreSQL to implement the database.
Data Insertion:

Write a script to insert the cleaned and categorized data into the database.
Ensure data integrity and handle duplicates or conflicting entries.
3. Frontend Dashboard Development
Dashboard Requirements:

Build an interactive dashboard using HTML, CSS, and JavaScript.
Include the following features:
Search and Filter: Allow users to search and filter transactions by type, date, or amount.
Visualizations: Use charts (e.g., bar charts, pie charts) to display, such as:
Total transaction volume by type.
Monthly summaries of transactions.
Distribution of payments and deposits.
Any  visualization/report you deem relevant for deeper insights
Details View: Display detailed information for a selected transaction.
API Integration (Optional for Bonus Marks):

Develop a simple backend API using Python (e.g., Flask or FastAPI) or NodeJS to fetch data from the database for the frontend.
