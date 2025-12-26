import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

LEETCODE_USERNAME = "Harsh_Joshi_"

def get_leetcode_data():
    url = "https://leetcode.com/graphql"
    query = {
        "query": """
        query recentAcSubmissionList($username: String!) {
          # recentAcSubmissionList(username: $username, limit: 10) {
          recentAcSubmissionList(username: $username) {
            title
            titleSlug
            timestamp
            lang
          }
        }
        """,
        "variables": {"username": LEETCODE_USERNAME}
    }
    return requests.post(url, json=query).json()["data"]["recentAcSubmissionList"]

def update_sheet():
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json",
        ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]
    )

    client = gspread.authorize(creds)
    sheet = client.open_by_key("1tLHch40aitSHCv3mBelhE9TG-n2rFI-WGst3jNu5tws").sheet1

    data = get_leetcode_data()
    for item in data:
        sheet.append_row([
            datetime.fromtimestamp(int(item["timestamp"])).strftime("%Y-%m-%d"),
            item["title"],
            item["lang"],
            f"https://leetcode.com/problems/{item['titleSlug']}/"
        ])

if __name__ == "__main__":
    update_sheet()
