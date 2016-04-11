
# This script shows how to create a smart envelope for messages in SeeMQ - a message broker integrated with JIRA for tracking.
# Description for SeeMQ at : http://1drv.ms/1SqbdSl

from jira import JIRA

# By default, the client will connect to a JIRA instance started from the Atlassian Plugin SDK.
# (see https://developer.atlassian.com/display/DOCS/Installing+the+Atlassian+Plugin+SDK for details).

jira = JIRA(basic_auth=('admin', 'admin'))    # a username/password tuple
# can be AD or RHDS as long as the JIRA is setup to authenticate with the appropriate membership provider

# Get all projects viewable by anonymous users.
projects = jira.projects()

# Create a trackable issue.
issue_dict = {
    'project': {'id': 123},
    'summary': 'New Queue from SeeMQ',
    'description': 'Yay I have a Queue',
    'issuetype': {'name': 'Task'},
}
issue = jira.create_issue(fields=issue_dict)

# Find all comments made by Atlassians on this issue.
import re
atl_comments = [comment for comment in issue.fields.comment.comments
                if re.search(r'seemq-admin@xyz.com$', comment.author.emailAddress)]

###
###   Message Broker processing
###

import pika

parameters = pika.URLParameters('amqp://guest:guest@localhost:5672/%2F')

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

channel.basic_publish('seemq_exchange',
                      'seemq_routing_key',
                      'JIRA ID: 123 - message body value',   ############           Integration
                      pika.BasicProperties(content_type='text/plain',
                                           delivery_mode=1))

connection.close()

# Add a comment to the issue.
jira.add_comment(issue, 'Message Queue activity mentioned here')

# Update the labels field like this
issue.update(labels=['AAA', 'BBB'])

# Resolve the issue and assign it to 'pm_user' in one step
jira.transition_issue(issue, '5', fields: {'assignee':{'name': 'pm_user'}, 'resolution':{'id': '3'}})

# For more involved access to JIRA issues, use JIRA native REST API like so
# curl request to http://jira-server/rest/api/latest/issue/ABC-123


