import json
from confluent_kafka import Producer


bootstrap_servers = 'pkc-619z3.us-east1.gcp.confluent.cloud:9092'
security_protocol = 'SASL_SSL'
sasl_mechanisms = 'PLAIN'
sasl_username = 'api_key'
sasl_password = 'api_secret'

#configurtion
conf = {'bootstrap.servers': bootstrap_servers,
        'security.protocol': security_protocol,
        'sasl.mechanisms': sasl_mechanisms,
        'sasl.username': sasl_username,
        'sasl.password': sasl_password,
        'client.id': 'kushagra_macbook'}

#producer object
producer = Producer(conf)

#function which will be called after the callback request.
def acked(error, msg):
    if error is not None:
        print(f"Failed with error {error}")
    else:
        print(f'following message is written on kafka topic with key {msg.key()}')
        print(f"Following message is written on Kafka topic {msg.value()}")

#opening a json file and then producing the data to kafka topic
with open('/Users/kushagra/Documents/spark_structured_streaming/spark_structured_streaming/kafka/data/data.json','r') as file:
    for line in file:
        data = json.loads(line)
        customer_key = str(data['customer_id'])
        customer_details = line
        producer.produce('retail_data', key=customer_key, value=customer_details, callback=acked)
        producer.poll(1)
        producer.flush()
