from datetime import datetime
from github import Github, GithubException
import pytz

from credentials import ACCESS_TOKEN


PRINT_COMMIT_DATES = True
PRINT_COMMIT_MESSAGES = True


def transform_date_into_correct_timezone(date: datetime) -> datetime:
    gmt_timezone = pytz.timezone("GMT")
    current_timezone = pytz.timezone("Europe/Warsaw")
    gmt_date = gmt_timezone.localize(date)
    correct_date = gmt_date.astimezone(current_timezone)
    return correct_date
    

def get_commits() -> None:
    connection = Github(ACCESS_TOKEN)
    current_date = datetime.today()
    beggining_of_the_month = datetime(
        year=current_date.year,
        month=current_date.month,
        day=1,
        hour=1,
        minute=1,
        second=1,
    )

    for repo in connection.get_user().get_repos():
        commits = repo.get_commits(
            since=beggining_of_the_month,
            until=current_date,
            author=connection.get_user(),
        )
        try:
            total_count = commits.totalCount
        except GithubException:
            total_count = 0
        
        if total_count:
            commit_str = "commit" if total_count == 1 else "commits"
            print("\n", repo.name, "-", total_count, commit_str)
            print(repo.html_url)
            for commit in commits:
                print(commit.sha, end="")
                if PRINT_COMMIT_DATES:
                    date = repo.get_git_commit(commit.sha).author.date
                    correct_date = transform_date_into_correct_timezone(date)
                    print_date = correct_date.strftime("%Y-%m-%d %H:%M")
                    print("\t", print_date, end="")
                if PRINT_COMMIT_MESSAGES:
                    print("\t", repo.get_git_commit(commit.sha).message)
                else:
                    print("")


if __name__ == '__main__':
    get_commits()
