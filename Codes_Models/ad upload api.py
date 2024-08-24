import boto3
import requests
import datetime
import json
from requests.auth import HTTPBasicAuth

# SP-API credentials
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
refresh_token = "YOUR_REFRESH_TOKEN"

# AWS credentials
access_key = "YOUR_ACCESS_KEY"
secret_key = "YOUR_SECRET_KEY"
region = "eu-west-1"  # The region for India is eu-west-1

# SP-API endpoint
endpoint = "https://sellingpartnerapi-eu.amazon.com"

# Set up boto3 client for SP-API
client = boto3.client(
    "sts",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region
)

# Generate access token using refresh token
def get_access_token():
    url = f"{endpoint}/auth/o2/token"
    payload = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, data=payload, headers=headers)
    return response.json()["access_token"]

# Create a feed document to upload product data
def create_feed_document():
    url = f"{endpoint}/feeds/2021-06-30/documents"
    headers = {
        "x-amz-access-token": get_access_token(),
        "x-amz-date": datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ"),
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers)
    return response.json()

# Upload product data to the feed document
def upload_product_data(feed_document_id, product_data):
    upload_url = feed_document_id["url"]
    headers = {
        "Content-Type": "application/xml"
    }
    response = requests.put(upload_url, data=product_data, headers=headers)
    return response.status_code

# Submit the feed for processing
def submit_feed(feed_document_id):
    url = f"{endpoint}/feeds/2021-06-30/feeds"
    headers = {
        "x-amz-access-token": get_access_token(),
        "x-amz-date": datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ"),
        "Content-Type": "application/json"
    }
    payload = {
        "feedType": "POST_PRODUCT_DATA",
        "marketplaceIds": ["A21TJRUUN4KGV"],  # Replace with your Indian marketplace ID
        "inputFeedDocumentId": feed_document_id
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response.json()

# Example product data in XML format
product_data = """<?xml version="1.0" encoding="utf-8"?>
<AmazonEnvelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="amzn-envelope.xsd">
    <Header>
        <DocumentVersion>1.02</DocumentVersion>
        <MerchantIdentifier>A1XEXAMPLE</MerchantIdentifier>
    </Header>
    <MessageType>Product</MessageType>
    <Message>
        <MessageID>1</MessageID>
        <OperationType>Update</OperationType>
        <Product>
            <SKU>YOUR_SKU</SKU>
            <StandardProductID>
                <Type>ASIN</Type>
                <Value>B000123456</Value>
            </StandardProductID>
            <ProductTaxCode>A_GEN_NOTAX</ProductTaxCode>
            <DescriptionData>
                <Title>Example Product Title</Title>
                <Brand>Example Brand</Brand>
                <Description>Example product description.</Description>
                <BulletPoint>First bullet point</BulletPoint>
                <BulletPoint>Second bullet point</BulletPoint>
                <Manufacturer>Example Manufacturer</Manufacturer>
                <ItemType>example-item-type</ItemType>
            </DescriptionData>
        </Product>
    </Message>
</AmazonEnvelope>"""

# Step-by-step execution
feed_document_id = create_feed_document()
upload_status = upload_product_data(feed_document_id, product_data)
submit_response = submit_feed(feed_document_id)

print("Feed document created:", feed_document_id)
print("Upload status:", upload_status)
print("Feed submission response:", submit_response)
