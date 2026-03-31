# Real-Time Clickstream Monitoring

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
Live monitoring of specific user actions (view_page, add_to_cart, purchase) to identify high-traffic areas of the platform instantly.

## Technical Architecture :

<img width="2816" height="1536" alt="Gemini_Generated_Image_22u5od22u5od22u5" src="https://github.com/user-attachments/assets/07520805-e447-4be1-862d-ea6a7cc4796c" />

## Pre-requisites : 

#### Managed Infrastructure [Aiven Console](https://console.aiven.io/): 

1. Aiven for Apache Kafka: A inkless kafka running cluster with SASL/SSL enabled.

2. Aiven Kafka Connect: An active connector service integrated with the Kafka cluster.

3. Aiven Karapace: The Schema Registry service enabled to host the Avro data contracts.

4. Aiven for OpenSearch: A running instance with Dashboards enabled.

#### Local Development Environment: 

1. Python 3.8+: Installed with the following libraries:

2. confluent-kafka: For high-performance Kafka communication.

3. fastavro: To handle binary Avro serialization.

   




