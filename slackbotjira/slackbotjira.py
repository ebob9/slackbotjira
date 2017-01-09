from jira import JIRA, JIRAError
from slackbot import settings
from slackbot.bot import respond_to, listen_to
import re

# Clean JIRA Url to not have trailing / if exists
CLEAN_JIRA_URL = settings.JIRA_URL if not settings.JIRA_URL[-1:] == '/' else settings.JIRA_URL[:-1]

# check for case sensitivity of projects
try:
    project_case_sensitive = settings.JIRA_PROJECTS_CASE_SENSITIVE
except AttributeError:
    # Value was not in slackbot_settings, use default
    project_case_sensitive = True

# Check for Custom CA cert
try:
    jira_ssl_verify = settings.JIRA_SSL_VERIFY
except AttributeError:
    # Value was not in slackbot_settings, use default
    jira_ssl_verify = True


# Login to jira
jira = JIRA( basic_auth=settings.JIRA_AUTH, options={
    'server': CLEAN_JIRA_URL,
    'verify': jira_ssl_verify
})


# Listen for messages that look like JIRA URLs
@listen_to('(.*)')
def jira_listener(message, text):
    for ticketproject, ticketnum in re.findall('([A-Za-z]+)-([0-9]+)', text):
        # Only attempt to find tickets in projects defined in slackbot_settings
        if project_case_sensitive:
            # case sensitive searching
            if ticketproject not in settings.JIRA_PROJECTS:
                return
        else:
            # case insensitive.
            if ticketproject.upper() not in [item.upper() for item in settings.JIRA_PROJECTS]:
                return

        # Parse ticket and search JIRA
        ticket = '%s-%s' % (ticketproject, ticketnum)
        process_ticket(message, ticket)


def process_ticket(message, ticket):
    try:
        issue = jira.issue(ticket)
    except JIRAError:
        message.send('%s not found' % ticket)
        return

    # Create variables to display to user
    summary = issue.fields.summary
    reporter = issue.fields.reporter.displayName if issue.fields.reporter else 'Anonymous'
    assignee = issue.fields.assignee.displayName if issue.fields.assignee else 'Unassigned'
    status = issue.fields.status
    priority = issue.fields.priority
    ticket_url = CLEAN_JIRA_URL + '/browse/%s' % ticket

    attachment = {
        "title": ticket_url,
        "pretext": "Ticket *%s*" % (ticket),
        "text": summary,
        "mrkdwn_in": ["text", "pretext"],
        "fields": [
            {
                "title": "Priority",
                "value": priority.name,
                "short": True
            },
            {
                "title": "Status",
                "value": status.name,
                "short": True
            },
            {
                "title": "Reporter",
                "value": reporter,
                "short": True
            },
            {
                "title": "Assignee",
                "value": assignee,
                "short": True
            }
        ]
    }

    # Send message to Slack
    message.send_webapi('', attachments=[attachment])
