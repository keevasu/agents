For Strands SDK and to connect to Bedrock 

*  export AWS_ACCESS_KEY_ID=xxxxx
*  export AWS_SECRET_ACCESS_KEY=yyyy
 Optionally, set the region
* export AWS_DEFAULT_REGION=

For Strands SDK and to connect to anthropic claude
* Get the API-Key from claude console 

***********************************************

Setting up your python env

* python3 -m venv .myenv

* source myenv/bin/activate

* pip3 install -r requirements.txt

* deactivate (To deactivate your virtual environment)

***********************************************
For setting up your claude Agent SDK

* export ANTHROPIC_API_KEY="fffffff"
* curl -fsSL https://claude.ai/install.sh | bash - This is to install Claude CLI for ClaudeSDKClient - This is useful when you are using streaming and query options

