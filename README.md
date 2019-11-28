# assignment-hb
An assignment with 3 approaches

Setup: Install Virtual Environment
- `python3 -m pip install --user virtualenv`
- `python3 -m venv venv`
- `source venv/bin/activate`

Install libraries:
- `python -m pip install --upgrade pip`
- `python -m pip install -r requirements.txt`

Install webdrivers:
- `webdrivermanager firefox chrome opera --linkpath ./drivers`

Test Execution with `pytest`:
* `python -m pytest ./pytest/test_adding_product_to_basket.py --html=Report_pytest.html --self-contained-html` or
* `pytest ./pytest/test_adding_product_to_basket.py --html=Report_pytest.html --self-contained-html`

Test Execution with `pytest-bdd`:
* `python -m pytest ./pytest-bdd/test_steps.py --html=Report_pytest-bdd.html --self-contained-html` or
* `pytest ./pytest-bdd/test_steps.py --html=Report_pytest-bdd.html --self-contained-html`

Test Execution with `Robot Framework`:
* `robot -d Results ./robot/adding_product_to_basket.robot`

Deactivate Virtual Environment:
* `deactivate`
