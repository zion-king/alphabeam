# AlphaBeam Conversational Business Intelligence
## 1. About
AlphaBeam CBI is an avant-garde Conversational Business Intelligence solution, the first of its kind, that redefines data interaction by seamlessly helping business users to explore their data without having to rely on their tech teams every time. While traditional BI tools have empowered data exploration through dashboards and reports, they often cater to a specialized audience, requiring technical expertise and leaving out crucial stakeholders. This results in missed insights, delayed decisions, and a limited understanding of their data's true potential.

To address this shortcoming in fostering a truly interactive and user-centric experience for non-technical users, AlphaBeam seamlessly blends conversational capabilities with advanced analytics, creating a symbiotic relationship between business users and their data.

## 2. AlphaBeam Capabilities
At a glance, AlphaBeam offers businesses and organisations, in particular non-technical stakeholders, a data-agnostic solution to ingest data from different sources, a semantic layer which translates raw data into business vocabularies and user queries into precise metrics and visualisations, a conversational interface for ad-hoc analysis and AI-powered insights through Gemini LLM, and a visualisation layer transforms the retrieved data into compelling dashboards. 

These capabilities empower users to carry out the following:
- **Conversational Inquiries:** Business users can ask questions about already existing dashboards in natural language, just as they would converse with a colleague. They could dig deeper into the data behind the visualisations, gaining a comprehensive understanding of trends and patterns.

- **Comprehensive Metric Exploration:** Engage in a conversational dialogue to uncover insights about any metric or data point, regardless of whether it's currently displayed on the dashboard. AlphaBeam breaks users free from the constraints of pre-defined dashboards and enables them to delve into any aspect of their data that piques their curiosity, regardless of their technical background.

- **Visualisation on Demand:** AlphaBeam enables stakeholders to explore data interactively, receive accurate and insightful interpretations of visuals and data trends, and generate dynamic visualisations with specific data points for deeper understanding.

- **Decision Making at the Speed of Data:** By uncovering hidden trends and patterns through conversational querying, AlphaBeam empowers users to make informed decisions very quickly based on readily available and easily digestible insights.

## 3. System Design - Proof of Concept
AlphaBeam's architecture orchestrates a seamless dialogue between users and their data, unlocking interactive insights through a robust system design. Here's a breakdown of its key components:

### i. Data Source Integrations
AlphaBeam embraces a wide range of data sources, including batch data, streaming platforms, SQL databases, data warehouses, and external APIs. For this PoC, we have used Google BigQuery to store our data, and integrated it to AlphaBeam to enable us to create the semantic layer using dbt and to fetch data based on user's queries using MetricFlow.

### ii. Semantic Layer
The Semantic Layer acts as a translator, bridging the gap between raw data and business context. Different semantic models can be built, each tailored to specific data sources. The Semantic Layer also integrates to the Retrieval Layer to provide semantic search capabilities, enabling users to discover and explore available data using natural language queries.

### iii. Metric Layer
The Metric Layer is an SQL implementation of the Semantic Layer. It houses the metrics and queries that are needed to fetch data from the source, tailored to the users' unique analytics needs. 

### iv. Assistants Layer
The Assistants Layer leverages Gemini to automate the creation of metric queries. When a user asks a question for which the semantic layer shows that there is available data, but the metric required to fetch that data is not available, the Assistant Layers augments the Metric Layer through metric definition and query formulation, and the generated metric is stored in the Metric Layer for subsequent use. Further, the Assistats Layer houses custom functions that are needed to assist in the data retrieval process.

### v. Retrieval Layer
The Retrieval Layer orchestrates Retrieval Augmented Generation (RAG) pipelines, through Llama-Index, to augment Gemini with contextual data. It is first used to transform the Semantic Layer into vector embeddings which are stored in a vector database. When a user asks a question, the Retrieval layer implements semantic search on these embeddings to determine if the question can be answered based on the business ontologies. Further, the Retrieval Layer is used to orchestrate data retrieval by implementing the queries that fetch relevant data from the source and augmenting Gemini with this retrieved data to generate a contextual response.

### vi. Visualisation / Reporting Layer
The Visualisation Layer transforms retrieved data into compelling visual narratives. It automates the creation of interactive dashboards and dynamic charts from users' requests. The Visualisation Layer also enables tech teams to configure readily-available dashboards for specific metrics, which users can view at a glance on the interface.

### vii. Chat Layer
The Chat Layer brings the contextual, conversational capabilities of AlphaBeam to the frontend, facilitating a natural language dialogue with the data source. The Chat Layer orchestrates AlphaBeam's conversational flow logic, from interpreting the user's query to determine whether there's an answer, to synthesising responses based on the retrieved data, leveraging the natural language capabilities of Gemini Pro.

## 4. User Flow
![AlphaBeam_User_Flow](https://github.com/zion-king/alphabeam/blob/main/frontend/assets/alphabeam_user_flow.png)

## 5. Our Tech Stack
The following technologies have been used to build the AlphaBeam MVP:
- **Data store:** Google BigQuery
- **Semantic and metric layers:** dbt, MetricFlow
- **Retrieval layer:** Llama-Index, ChromaDB, Cohere, Gemini Pro, TrueLens
- **Visualisation layer:** Pandas, Plotly, Streamlit
- **Chat layer:** Llama-Index, Gemini Pro
- **Deployment:** Streamlit, GCP

![AlphaBeam_Tech_Stack](https://github.com/zion-king/alphabeam/blob/main/frontend/assets/alphabeam_tech_stack.png)

## 6. About the Data

### i. Data Description
The data used in this PoC to demonstrate AlphaBeam's capabilities was obtained from the Adventure Works database. We chose this database because it is a typical example of how business data should appear. Because this database contains a huge number of datasets, we chose only three datasets in this database. The chosen data were: 
- **Customers:** This contains the descriptions of each customer where each row describes each customer.
- **Products:** This had descriptions of each product where each row describes each product.
- **Sales:** Each entry described details of each order.
These datasets were uploaded on BigQuery before dbt was connected to BigQuery to build the semantic layer and metric layer.

### ii. Building the Semantic Layer and Metric Layer
Before building the semantic layer with dbt-metricflow, the raw data were modelled using dbt. These modelled datasets acted as the bedrock to the semantic layer where the necessary connections between these datasets were established using the necessary foreign and primary keys. In each semantic model where these relationships were established, we also defined the metrics that would manifest in our data warehouse. It is important to note that we didn't exhaust the metrics that could be defined from the data because we understood that we were building a proof of concept data warehouse. 

Listed below are the metrics currently available:
- `discount_amount_average`
- `discount_amount_total`
- `price_average`
- `price_total`
- `product_cost_average`
- `product_cost_total`
- `quantity_average`
- `quantity_total`
- `revenue_average`
- `revenue_total`

### iii. Displaying The Metrics on the Streamlit Dashboard
Among the available metrics in our metric layer, the following metrics were plotted and displayed on the dashboard:
- `product_cost_total` displayed as **Total Cost**
- `quantity_total` displayed as **Total Product Sold**
- `revenue_total` displayed as **Total Revenue**
- Difference between `revenue_total` and `product_cost_total` displayed as **Profit Margin**

## 7. Running AlphaBeam Locally
