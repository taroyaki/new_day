import argparse
import requests
import pendulum

from github import Github


GET_UP_ISSUE_NUMBER = 1   
TIMEZONE = "Asia/Tokyo"   #能否改为自动识别？


def login(token):
    return Github(token)

def get_today_get_up_status(issue):
    comments = list(issue.get_comments())
    if not comments:
        return False
    latest_comment = comments[-1]
    now = pendulum.now(TIMEZONE)
    latest_day = pendulum.instance(latest_comment.created_at).in_timezone(
        TIMEZONE
    )
    is_today = (latest_day.day == now.day) and (latest_day.month == now.month)
    return is_today

def main(github_token, repo_name, ios_message, tele_token, tele_chat_id):
    u = login(github_token)
    repo = u.get_repo(repo_name)
    issue = repo.get_issue(GET_UP_ISSUE_NUMBER)
    is_toady = get_today_get_up_status(issue)
    if is_toady:
        print("Today I have recorded the wake up time")
        return
    else:
        ios_message=ios_message[2:]  # 去掉前两个字符，否则会出现冒号加一个空格在最前面
        print(ios_message)
        issue.create_comment(ios_message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("github_token", help="github_token")
    parser.add_argument("repo_name", help="repo_name")
    parser.add_argument(
        "--ios_message", help="ios_message", nargs="?", default="", const=""
    )
    parser.add_argument("--tele_token", help="tele_token", nargs="?", default="", const="")
    parser.add_argument("--tele_chat_id", help="tele_chat_id", nargs="?", default="", const="")
    options = parser.parse_args()
    main(
        options.github_token,
        options.repo_name,
        options.ios_message,
        options.tele_token,
        options.tele_chat_id,
    )
