* Going to keep a file just to keep track of where I am in the setup/development.

3/20/26
* Prompted github copilot to generate the project. Also setup cloudsql instance to use and the github repo, as well 
  as the cloud run project.
* Should read over the setup guide next - I think I need to configure oauth. I want to get it working locally and 
  make changes via AI. In general I want to force myself to use AI so I can make sure I create a good agent file for 
  common things I want the AI to always think about whenever I interact with it. I'm using this as an exercise to 
  see where there is friction in my usage in AI 

3/21/26
* Setup oauth credentials, and got the django migrations to run. AI seems pretty bad at setting up the 
  infrastructure and such - it does its best guess, but doesn't do any verification that what it says to do is 
  actually correct. 
* Should try to figure out how to make sure I can configure copilot to always follow a base set of instructions. I 
  can't manually specify the agent anymore. 
* Some of the framework specific stuff was also not taken care of - once I started up the application I encountered 
  runtime errors, and had to prompt the AI with the error to understand how to fix it. I had to configure auth via 
  django admin before I was able to actually use the site. 

3/31/26
* Finally picked this back up. 
* First step in debugging AI setup code, make sure logging for the errors is properly enabled. That ended up 
  shedding light on the issues I was having, namely misconfigured/missing ENV variables.
* Need to get into a better pattern of managing secrets/env variables and such with the prod environment. I'm doing 
  everything manually now, which is fine, but was a part of the process that was a little annoying.
* Also needed to manually setup a cloud sql connection for cloud run. I didn't use the generated cloudrun config 
  file AI generated, did most of the infra setup manually.
* Running into a number of other bugs - basically feeding the error back into AI. It's really the base-setup of the 
  application that has been problematic. I think things will go more smoothly when I'm just using it for pure 
  application code.