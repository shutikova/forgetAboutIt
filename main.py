from jira import JIRA, exceptions, resources
from sys import exit
from typing import List, Optional

token = ""

quarters = {"CY22Q1": ["2022/01/01", "2022/03/30"], "CY22Q2": ["2022/01/04", "2022/06/30"],
            "CY22Q3": ["2022/07/01", "2022/09/30"], "CY22Q4": ["2022/10/01", "2022/12/31"]}
teams = ['RHEL', 'RHELBLD', 'RHELCMP', 'RHLEWF', 'RHELDST']
exd_work_types = ['Release Operation', 'Maintenance']
custom_fields = {'Story Points': 'customfield_12310243'}

invalid_token = "You have entered invalid token. Try again"
invalid_quarter = "You have entered invalid quarter. Try one from the following list: " + str(quarters.keys())
invalid_team = "You have entered invalid team name. Try one from the following list: " + str(teams)


def main(quarter: str, team: str) -> int:
    # Correctness of parameters
    if quarter not in quarters.keys():
        print(invalid_quarter)
        exit(-1)
    if team not in teams:
        print(invalid_team)
        exit(-1)

    # Authorisation
    try:
        jira = JIRA(server="https://issues.redhat.com/", token_auth=token)
        jira.myself()
    except exceptions.JIRAError:
        print(invalid_token)
        exit(-1)

    get_story_points(jira, [])
    get_issues_by_exd_work_type(jira, 'Maintenance', quarter, team)
    return 0


def get_issues_by_exd_work_type(jira: JIRA, exd_work_type: str, quarter: str, team: str)\
        -> Optional[List[resources.Issue]]:
    jql_request = f"project={team} and resolved >= '{quarters.get(quarter)[0]}'" \
                  f"and resolved <= '{quarters.get(quarter)[1]}' and EXD-WorkType = '{exd_work_type}'"\
                  f"and 'Epic Link' is EMPTY"
    return jira.search_issues(jql_request)


def get_tasks_from_epics(jira: JIRA, quarter: str, team: str) -> Optional[List[resources.Issue]]:
    jql_request = f"project={team} and resolved >= '{quarters.get(quarter)[0]}'" \
                  f"and resolved <= '{quarters.get(quarter)[1]}' and 'Epic Link' is not EMPTY"
    return jira.search_issues(jql_request)


def get_tickets(jira: JIRA, quarter: str, team: str) -> Optional[List[resources.Issue]]:
    jql_request = f"project={team} and resolved >= '{quarters.get(quarter)[0]}'" \
                  f"and resolved <= '{quarters.get(quarter)[1]}' and issuetype = Ticket and 'Epic Link' is EMPTY"
    return jira.search_issues(jql_request)


def get_story_points(jira: JIRA, issues: List[resources.Issue]) -> List[int]:
    story_points = []
    for issue in issues:
        pass
    print(type(jira.issue('RHELCMP-10001')))
    print(type(jira.issue('RHELCMP-10001').get_field(custom_fields.get('Story Points'))))
    return story_points


def create_csv():
    pass


def put_data_to_csv():
    pass


def create_pie_chart():
    pass


main('CY22Q3', "RHELCMP")
