FROM python:3.8

COPY . .

ADD Piv_packages Piv_packages
ADD Reporting/assets Reporting/assets

RUN pip install --no-cache-dir -r requirements.txt -e ./Piv_packages/api_interactions ./Piv_packages/data_constants

WORKDIR /Pytest

CMD ["pytest", "-v"]
# "--html=Reporting/report.html", "--css=Reporting/assets/report.css"

CMD tail -f /dev/nul