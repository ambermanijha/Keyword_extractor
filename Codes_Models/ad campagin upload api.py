import requests
import json
import datetime

# API credentials
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
refresh_token = "YOUR_REFRESH_TOKEN"
profile_id = "YOUR_PROFILE_ID"  # Get this from the Amazon Advertising API after querying profiles

# API endpoints
auth_endpoint = "https://api.amazon.com/auth/o2/token"
advertising_endpoint = "https://advertising-api.amazon.com/v2"


# Function to get access token using the refresh token
def get_access_token():
    payload = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
    }
    response = requests.post(auth_endpoint, data=payload, headers=headers)
    return response.json()["access_token"]


# Function to create a Sponsored Products campaign
def create_campaign(access_token):
    url = f"{advertising_endpoint}/sp/campaigns"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Amazon-Advertising-API-ClientId": client_id,
        "Amazon-Advertising-API-Scope": profile_id
    }

    # Example campaign data
    campaign_data = {
        "name": "Example Campaign",
        "campaignType": "sponsoredProducts",
        "targetingType": "manual",
        "state": "enabled",
        "dailyBudget": 5.0,  # Daily budget in INR
        "startDate": datetime.datetime.now().strftime("%Y%m%d"),
        "endDate": None,  # No end date
        "portfolioId": None,  # Use None if not using portfolios
        "premiumBidAdjustment": False,
    }

    response = requests.post(url, headers=headers, data=json.dumps(campaign_data))
    return response.json()


# Function to create an ad group within the campaign
def create_ad_group(campaign_id, access_token):
    url = f"{advertising_endpoint}/sp/adGroups"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Amazon-Advertising-API-ClientId": client_id,
        "Amazon-Advertising-API-Scope": profile_id
    }

    ad_group_data = {
        "name": "Example Ad Group",
        "campaignId": campaign_id,
        "defaultBid": 1.0,  # Default bid in INR
        "state": "enabled"
    }

    response = requests.post(url, headers=headers, data=json.dumps(ad_group_data))
    return response.json()


# Function to create a keyword targeting for the ad group
def create_keyword_targeting(ad_group_id, access_token):
    url = f"{advertising_endpoint}/sp/keywords"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Amazon-Advertising-API-ClientId": client_id,
        "Amazon-Advertising-API-Scope": profile_id
    }

    keyword_data = [
        {
            "adGroupId": ad_group_id,
            "state": "enabled",
            "keywordText": "example keyword",
            "matchType": "exact",
            "bid": 1.0  # Bid amount in INR
        }
    ]

    response = requests.post(url, headers=headers, data=json.dumps(keyword_data))
    return response.json()


# Step-by-step execution
access_token = get_access_token()
campaign_response = create_campaign(access_token)
campaign_id = campaign_response.get("campaignId")
print("Campaign created:", campaign_response)

if campaign_id:
    ad_group_response = create_ad_group(campaign_id, access_token)
    ad_group_id = ad_group_response.get("adGroupId")
    print("Ad group created:", ad_group_response)

    if ad_group_id:
        keyword_response = create_keyword_targeting(ad_group_id, access_token)
        print("Keyword targeting created:", keyword_response)
