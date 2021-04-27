FROM python:3.8

COPY . .

ADD Piv_packages Piv_packages

RUN pip install --no-cache-dir -r requirements.txt -e ./Piv_packages/api_interactions ./Piv_packages/data_constants

WORKDIR /be_tests

RUN ["pytest", "-v"]
# "--html=Reporting/report.html", "--css=Reporting/assets/report.css"

CMD tail -f /dev/null