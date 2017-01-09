## Synopsis

A [slackbot](https://github.com/lins05/slackbot) plugin that queries the JIRA API for information about a ticket when mentioned in a channel.

## Screenshot

![Screenshot](https://i.imgur.com/IxqWuFv.png)

## Installation

1. Setup [slackbot](https://github.com/lins05/slackbot)
2. `pip install slackbotjira`
3. In slackbot_settings.py:
  * Add 'slackbotjira' to PLUGINS list
  * `import os` to use environment variables for JIRA user/pass
  * Configure Python Variables in slackbot_settings.py
    * JIRA_URL = '{JIRA URL}'
    * JIRA_AUTH = (os.environ['JIRA_USER'], os.environ['JIRA_PASS'])
    * JIRA_PROJECTS = ['SPT']  # JIRA Project Keys
4. Configure Environment Variables for Authorization
  * JIRA_USER
  * JIRA_PASS
5. Configure Optional items:
  * Case Sensitivity for Project Names
    * JIRA_PROJECT_CASE_SENSITVE = False  # True is default
  * SSL CA Certificate (or disable verification completely)
    * JIRA_SSL_VERIFY = False  # Disable Verification
    * JIRA_SSL_VERIFY = '/path/to/ca/certificate-chain.pem'  # Custom CA cert (does not like spaces in filename..)
 
## Contributors

[ebob9](https://github.com/ebob9)<br>
[kvarga](https://github.com/kvarga)

## License

The MIT License (see [LICENSE](LICENSE))
