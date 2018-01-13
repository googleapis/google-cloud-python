from datetime import date
from datetime import timedelta
from collections import namedtuple
import requests
from bs4 import BeautifulSoup

today = date.today()
language = 'python'
google_cloud = 'https://www.github.com/GoogleCloudPlatform/google-cloud-{}/'
github_url = google_cloud.format(language)

no = '-'
Types = namedtuple('Label',
                   ['bug', 'feature', 'question', 'cleanup', 'process'])
types = Types('label:"type: bug" ',
              'label:"type: feature request" ',
              'label:"type: question" ',
              'label:"type: cleanup" ',
              'label:"type: process" ')

Priority = namedtuple('Priority', ['p0', 'p1', 'p2'])
priority = Priority('label:"priority: p0" ',
                    'label:"priority: p1" ',
                    'label:"priority: p2" ')


def updated(days):
    return 'updated:<={}'.format(today-timedelta(days))


def created(days):
    return 'created:<={}'.format(today-timedelta(days))


def query(url, params, name):
    r = requests.get(url, params=params)
    soup = BeautifulSoup(r.text, 'html.parser')
    number = int(soup
                 .find('a', class_='btn-link selected')
                 .contents[2]
                 .strip()[:-5])
    items = soup.find_all('span', class_='opened-by')
    print(r.url)
    print(name, number)
    print([int(item.contents[0].strip().split('\n')[0][1:]) for item in items])


issues = {'issues_with_no_type': (no+types.bug
                                  + no+types.feature
                                  + no+types.question
                                  + no+types.cleanup
                                  + no+types.process),
          'questions_with_no_assignee': 'no:assignee ',
          'bugs_with_no_assignee': types.bug + 'no:assignee',
          'bugs_with_no_priority': (types.bug
                                    + no+priority.p0
                                    + no+priority.p1
                                    + no+priority.p2),
          'bugs_with_priority_p0': types.bug + priority.p0,
          'bugs_with_priority_p1': types.bug + priority.p1,
          'bugs_with_priority_p2': types.bug + priority.p2,
          'questions_outside_response_slo': (types.question
                                             + updated(120)),
          'p0_bugs_outside_response_slo': (types.bug
                                           + priority.p0
                                           + updated(1)),
          'p0_bugs_outside_closure_slo': (types.bug
                                          + priority.p0
                                          + created(5)),
          'p1_bugs_outside_response_slo': (types.bug
                                           + priority.p1
                                           + updated(5)),
          'p1_bugs_outside_closure_slo': (types.bug
                                          + priority.p1
                                          + created(42)),
          'p2_bugs_outside_response_slo': (types.bug
                                           + priority.p2
                                           + updated(120)),
          'p2_bugs_outside_closure_slo': (types.bug
                                          + priority.p2
                                          + created(120)),
          'feature_requests_outside_response_slo': (types.feature
                                                    + updated(120)),
          'feature_requests_outside_closure_slo': (types.feature
                                                   + created(120)),
          'cleanup_outside_response_slo': (types.cleanup
                                           + updated(120)),
          'cleanup_outside_closure_slo': (types.cleanup
                                          + created(120))}

pull_requests = {'pull_requests_with_no_type': (no+types.bug
                                                + no+types.feature
                                                + no+types.question
                                                + no+types.cleanup
                                                + no+types.process),
                 'pull_requests_outside_response_slo': updated(42),
                 'pull_requests_outside_closure_slo': created(120)}


for issue in issues:
    if not issues[issue]:
        continue
    params = {'q': 'is:open is:issue ' + issues[issue]}
    url = github_url + 'issues?'
    query(url, params, issue)

for pull_request in pull_requests:
    if not pull_requests[pull_request]:
        continue
    params = {'q': 'is:open is:pr ' + pull_requests[pull_request]}
    url = github_url + 'pulls?'
    query(url, params, pull_request)
