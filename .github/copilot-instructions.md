* Always ask clarifying questions if things are not clear
* When rendering front-end pages - assume that they will be accessed from both a mobile and desktop device - try to 
  ensure the UI has a responsive design for easy use on mobile devices.

* Dependency version safety rules (requirements.txt / pyproject.toml):
  - Never guess package versions.
  - Only pin versions that are confirmed to exist on PyPI at edit time.
  - Before changing dependency versions, verify each package/version with a real check (PyPI or pip index).
  - If verification cannot be performed, do NOT pin; ask me to run a check or leave the package unpinned with a comment.

* Python compatibility rules:
  - Ensure each pinned package supports Python 3.14.3.
  - If Python 3.14.3 support is uncertain, do not pin that version; choose a confirmed compatible one or ask.

* Required response format for dependency changes:
  - After editing dependency files, include a "Dependency Verification" section listing each changed package as:
    - package==version — VERIFIED / NOT VERIFIED
  - If any are NOT VERIFIED, explicitly state that and stop before finalizing pins.

* Installation sanity check (required):
  - After updating dependencies, run:
    - pip install -r requirements.txt
  - If install fails, fix versions and re-run until successful.

* Conflict rule:
  - If these rules conflict with speed, prioritize correctness and verification over speed.

