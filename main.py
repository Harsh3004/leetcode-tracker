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
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scope
    )

    client = gspread.authorize(creds)
    sheet = client.open("LeetCode Tracker").sheet1

    # Fetch existing problems
    existing_titles = set(sheet.col_values(2))  # Column B = Problem Name

    # Fetch LeetCode data
    data = get_leetcode_data()

    new_count = 0

    for item in data:
        title = item["title"]
        if title not in existing_titles:
            sheet.append_row([
                datetime.fromtimestamp(int(item["timestamp"])).strftime("%Y-%m-%d"),
                title,
                item["lang"],
                f"https://leetcode.com/problems/{item['titleSlug']}/"
            ])
            new_count += 1

    print(f"Added {new_count} new problems.")

if __name__ == "__main__":
    update_sheet()
