ipython_slack_client
======================
> IPython frontend that runs in Slack

##### [Implementation to support my talk proposal (not confirmed) in PyCon India 2018](https://in.pycon.org/cfp/2018/proposals/jupyter-notebooks-internals-and-extension~dyz6e/)

![IPython Slack Client](https://i.imgur.com/SvyDlmE.gif)

## Usage
> Valid only for the development version

* Add [SLACK_API_TOKEN](https://api.slack.com/custom-integrations/legacy-tokens) (legacy token) as an environmental variable.
```
$ export SLACK_API_TOKEN="xoxp-xxxx"
```

* Execute the client module.
```
$ python3 slack_client.py
```

* Start writing the code in a Slack channel.