# pytest automation
Back End API testing

The Framework dependecies: 
  - Python 3.8
  - PyCharm Community Edition
  - python virtual environment with required libraries

Network:
VPN access required. If vpn connection isn't possible whitelist your 
ip address in django admin /admin/main/ipwhitelist/

Setup Python Virtual Environment:
Make sure python 3 is your base interpreter. Use PyEnv and Homebrew to configure your global python version
https://opensource.com/article/19/5/python-3-default-mac

1) cd into the directory where you want to create you python virtual environment
2) python -m venv [name_of_virtual_env]         # Create virtual environment
3) source [name_of_virtual_env]/bin/activate    # This activates the virtual environment
4) pip install -r [path to]/requirements.txt -e ./Piv_packages/api_interactions ./Piv_packages/data_constants
   # This installs all of the project requirements and the local packages api_interactions and data_constants


Once you have this done you can either run your tests directly from the terminal by going into the directory
where the pytests are held or you can go into your pycharm preferences and attach the python executable of your created
virtual environment to the interpreter. This can be done under PyCharm-->Preferences-->Project Interpreter. Click the
wheel to add existing environment and navigate to the python executable of your virtual environment.

# Run these commands in the directory containing the Pytests
pytest -v --env=dev  # run all tests

pytest -v --env=qa  -m "smoke"          # run smoke tests in QA

pytest -v --env=dev  -m "not smoke"     # run all tests except smoke test

pytest -v --env=dev -m "smoke" --html=Reporting/report.html --css=Reporting/assets/report.css # run test with reporting

pytest --setup-show             # this will show the setup and teardown of fixtures

#If you don't want or have a need to create a virtualenv and just want to run the tests
install docker on your machine and then just run. "docker build ./" in the Pytest directory










