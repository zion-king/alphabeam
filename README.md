# AlphaBeam Conversational Business Intelligence
## About
AlphaBeam CBI is an avant-garde Conversational Business Intelligence solution, the first of its kind, that redefines data interaction by seamlessly helping business users to explore their data without having to rely on their tech teams every time. While traditional BI tools have empowered data exploration through dashboards and reports, they often cater to a specialized audience, requiring technical expertise and leaving out crucial stakeholders. This results in missed insights, delayed decisions, and a limited understanding of their data's true potential. 

To address this shortcoming in fostering a truly interactive and user-centric experience for non-technical users, AlphaBeam seamlessly blends conversational capabilities with advanced analytics, creating a symbiotic relationship between business users and their data.

## AlphaBeam Capabilities
At a glance, AlphaBeam offers businesses and organisations, in particular non-technical stakeholders, a data-agnostic solution to ingest data from different sources, a semantic layer which translates raw data into business vocabularies and user queries into precise metrics and visualizations, a conversational interface for ad-hoc analysis and AI-powered insights through Gemini LLM, and a visualisation layer transforms the retrieved data into compelling dashboards. 

These capabilities empower users to carry out the following:
- **Conversational Inquiries:** Business users can ask questions about already existing dashboards in natural language, just as they would converse with a colleague. They could dig deeper into the data behind the visualizations, gaining a comprehensive understanding of trends and patterns.

- **Comprehensive Metric Exploration:** Engage in a conversational dialogue to uncover insights about any metric or data point, regardless of whether it's currently displayed on the dashboard. AlphaBeam breaks users free from the constraints of pre-defined dashboards and enable them delve into any aspect of their data that piques their curiosity, regardless of their technical background.

- **Visualization on Demand:** AlphaBeam enables stakeholders to explore data interactively, receive accurate and insightful interpretations of visuals and data trends, and generate dynamic visualizations with specific data points for deeper understanding.

- **Decision Making at the Speed of Data:** By uncovering hidden trends and patterns through conversational querying, AlphaBeam empowers users to make informed decisions very quickly based on readily available and easily digestible insights.

## Proof of Concept
AlphaBeam's architecture orchestrates a seamless dialogue between users and their data, unlocking interactive insights through a robust system design. Here's a breakdown of its key components:

### 1. Data Source Integrations
AlphaBeam embraces a wide range of data sources, including batch data, streaming platforms, SQL databases, data warehouses, and external APIs. For this PoC, we have used Google BigQuery to store our data, and integrated it to AlphaBeam to enable us to create the semantic layer using dbt and to fetch data based on user's queries using MetricFlow.

### 1. Semantic Layer
The Semantic Layer acts as a translator, bridging the gap between raw data and business context. Different semantic models can be employed, each tailored to specific data sources. The Semantic Layer also integrates to the Retrieval Layer to provide semantic search capabilities, enabling users to discover and explore available data based on natural language queries.

### 2. Metric Layer
The Metric Layer is an SQL implementation of the Semantic Layer. It houses the metrics and queries that are needed to fetch data from the source, tailored to the users' unique analytics needs. 

### 3. Assistants Layer
The Assistants Layer leverages Gemini to automate the creation of metric queries. When a user asks a question for which the semantic layer shows that there is available data, but the metric required to fetch that data is not available, the Assistant Layers augments the Metric Layer through metric definition and query formulation, and the generated metric is stored in the Metric Layer for subsequent use. Further, the Assistats Layer houses custom functions that are needed to assist in the data retrieval process.

### 4. Retrieval Layer
The Retrieval Layer orchestrates Retrieval Augmented Generation (RAG) pipelines, through Llama-Index, to augment Gemini with contextual data. It is first used to transform the Semantic Layer into vector embeddings which are stored in a vector database. When a user asks a question, the Retrieval layer implements semantic search on these embeddings to determine if the question can be answered based on the business ontologies. Further, the Retrieval Layer is used to orchestrate data retrieval by implementing the queries that fetch relevant data from the source and augmenting Gemini with this retrieved data to generate a contextual response.

### 5. Visualisation / Reporting Layer
The Visualisation Layer transforms retrieved data into compelling visual narratives. It automates the creation of interactive dashboards and dynamic charts from users' requests. The Visualisation Layer also enables tech teams to configure readily-available dashboards for specific metrics, which users can view at a glance on the interface.

### 6. Chat Layer
The Chat Layer brings the contextual, conversational capabilities of AlphaBeam to the frontend, facilitating a natural language dialogue with the data source. The Chat Layer orchestrates AlphaBeam's conversational flow logic, from interpreting the user's query to determine whether there's an answer, to synthesising responses based on the retrieved data, leveraging the natural language capabilities of Gemini Pro.

## User Flow
![AlphaBeam_User_Flow](https://github.com/zion-king/alphabeam/frontend/assets/alphabeam_user_flow.png)

## Tech Stack
![AlphaBeam_Tech_Stack](https://github.com/zion-king/alphabeam/frontend/assets/alphabeam_tech_stack.png)


