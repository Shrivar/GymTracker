* Always ask clarifying questions if things are not clear
* When rendering front-end pages - assume that they will be accessed from both a mobile and desktop device - try to 
  ensure the UI has a responsive design for easy use on mobile devices.
* When updating dependencies in requirements.txt:
  - ONLY use package versions that are published on PyPI and actually exist
  - Verify that each pinned version is compatible with Python 3.14.3
  - When in doubt, use real, stable versions rather than guessing
  - Example: oauthlib==3.8.0 does NOT exist, use oauthlib==3.9.0 instead
  - Do NOT add versions that cannot be verified as real PyPI releases 
