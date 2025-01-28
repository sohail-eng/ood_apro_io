import pandas as pd
import requests
from tqdm import tqdm


with open("token.txt", "r") as file:
    token = str(file.read()).strip()


headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'channel': 'APP',
    'origin': 'https://ghl-isv-app-prod.leadconnectorhq.com',
    'priority': 'u=1, i',
    'referer': 'https://ghl-isv-app-prod.leadconnectorhq.com/',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'source': 'WEB_USER',
    'version': '2021-07-28',
    'token-id': token,
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
}

email_url = 'https://backend.leadconnectorhq.com/conversations-reporting/emails'
name_url = 'https://backend.leadconnectorhq.com/contacts/search/ids/es'


def get_email_page_data(status, start_date, end_date):
    params = {
        'locationId': 'uJmm8JybOgefefFQveQy',
        'status': status,
        'limit': 1,
        'skip': 0,
        'provider': 'leadconnector',
        'startDate': f'{start_date}T19:00:00.000Z',
        'endDate': f'{end_date}T18:59:59.999Z',
    }
    response_data = requests.get(email_url, headers=headers, params=params).json()
    if response_data.get("statusCode") == 401:
        print("Please replace token")
        exit()
    total = response_data.get("total")
    final_data = []
    for _ in tqdm(range(int(total / 1000) + (1 if total % 1000 != 0 else 0)), desc="Processing", unit="_"):
        params = {
            'locationId': 'uJmm8JybOgefefFQveQy',
            'status': status,
            'limit': 1000,
            'skip': len(final_data),
            'provider': 'leadconnector',
            'startDate': f'{start_date}T19:00:00.000Z',
            'endDate': f'{end_date}T18:59:59.999Z',
        }
        response_data = requests.get(email_url, headers=headers, params=params).json()
        if response_data.get("statusCode") == 401:
            print("Please replace token")
            exit()

        total = response_data.get("total")
        response_data = response_data.get("results")
        response_list = [
            {
                "contactId": item.get("contactId"),
                "contactName": "",
                "email": ", ".join(item.get("email")),
                "status": status.capitalize(),
                "updatedAt": item.get("updatedAt")
            }
            for item in response_data
        ]
        final_data.extend(response_list)

    return final_data


def get_name_data(ids):
    json_data = {
        'locationId': 'uJmm8JybOgefefFQveQy',
        "ids": ids
    }
    response_data = requests.post(name_url, headers=headers,
                                  json=json_data).json()
    return response_data.get("contacts")


def scrape_name_data(data_set):
    data_set = [
        item.get("contactId")
        for item in data_set
    ]
    chunk_size = 250
    chunks = [data_set[i:i + chunk_size] for i in range(0, len(data_set), chunk_size)]
    names_final_data = {}

    # Adding tqdm progress bar here
    for chunk in tqdm(chunks, desc="Processing", unit="_"):
        names_data = get_name_data(chunk)
        names_final_data.update({
            item.get("id"): item.get("contactName")
            for item in names_data
        })

    return names_final_data


def scrape_email_data(status):
    json_data = get_email_page_data(
        status=status,
        start_date="2025-01-16",
        end_date="2025-01-23"
    )

    names_data = scrape_name_data(
        json_data
    )
    for item in json_data:
        item.update({
            "contactName": names_data.get(item.pop("contactId"), item["email"])
        })

    df = pd.DataFrame(json_data)
    df.to_csv(f"emails_{status}.csv", index=False)


scrape_email_data(status="opened")
scrape_email_data(status="clicked")
