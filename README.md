# Real time clickstream data pipeline using Aiven 


## Usecase :

The goal of this project is to provide an immediate, live view of website activity to key stakeholders. Instead of waiting for daily reports, the business can monitor current traffic levels , customer patterns and site health as events occur.

### Key Values:

#### Live Traffic Tracking: 
See exactly how many users are active on the site at any given second.

#### Performance Monitoring: 
Track the response_time_ms for every click. If the site slows down, the Gauge Visualization turns red, alerting the team before users abandon the site.

#### Geographic Visibility: 
 Automatically categorizes every interaction by country (e.g., IN, US, UK), allowing stakeholders to visualize market penetration and global user distribution in sub-seconds.

#### Behavioral Tracking: 
Live monitoring of specific user actions (view_page, add_to_cart, purchase) to identify high-traffic areas of the platform instantly

## Technical Architecture :

<img width="2816" height="1536" alt="Gemini_Generated_Image_22u5od22u5od22u5" src="https://github.com/user-attachments/assets/07520805-e447-4be1-862d-ea6a7cc4796c" />

## Pre-requisites : 

#### Managed Infrastructure ([Aiven Console](https://console.aiven.io/)): 

1. **Aiven for Apache Kafka**: A inkless kafka running cluster with SASL/SSL enabled.

2. **Aiven Kafka Connect**: An active connector service integrated with the Kafka cluster.

3. **Aiven Karapace**: The Schema Registry service enabled to host the Avro data contracts.

4. **Aiven for OpenSearch**: A running instance with Dashboards enabled.

#### Local Development Environment: 

1. **Python 3.8+**: Installed with the below libraries

2. **confluent-kafka**: For high-performance Kafka communication.

3. **fastavro**: To handle binary Avro serialization.

##  Deployment & Setup Guide

#### 1. Kafka & Schema Registry Configuration
* **Create Topic:** In the Aiven Kafka console, create a topic named `clickstream`. Set the **Cleanup Policy** to `delete` (Diskless).
* **Enable Schema Registry:** Create a schema subject named `clickstream-data` and upload the [clickstream-data.avsc](https://github.com/Nidhiks2000/realtime-clickstream-pipeline/blob/main/clickstream-data.avsc) definition.

#### 2. Producer Initialization
* **Update Credentials:** Update the `service_uri`, `user`, and `password` in [clickstream-producer.py](https://github.com/Nidhiks2000/realtime-clickstream-pipeline/blob/main/clickstream-producer.py).
* **Execute Script:** Run the producer to start streaming validated events:
  ```bash
  python3 clickstream-producer.py

 #### 3. OpenSearch Integration (Kafka Connect)
* **Sink Configuration:** Activate the **OpenSearch Sink Connector** within the Kafka Connect service. Use the configuration parameters provided in [opensearch_connector_config.json](https://github.com/Nidhiks2000/realtime-clickstream-pipeline/blob/main/opensearch_connector_config.json).
* **Verification:** Navigate to **OpenSearch Service > Indexes** in the Aiven Console. Once the connector is active, you will see the `clickstream` index appearing with live storage updates, confirming data is being successfully ingested.

#### 4. Dashboards & Visualization
* **Access UI:** Launch the **OpenSearch Dashboards** URL found in your Aiven OpenSearch service overview.
  
* **Create Index Pattern:**
    1. Navigate to **Dashboards Management > Index Patterns**.
  
    2. Create a new pattern named `clickstream`.
  
    3. Select `@timestamp` as the primary time field to enable time-series analysis.
       
* **Build Insights:** Navigate to the **Visualize** tab to create real-time **Gauges** for performance monitoring and **Maps** for geographic traffic distribution.

<img width="1512" height="745" alt="Screenshot 2026-03-31 at 11 00 46 PM" src="https://github.com/user-attachments/assets/bea140e6-c7df-4d17-a5e6-6339bfa11d9b" />
  

   




