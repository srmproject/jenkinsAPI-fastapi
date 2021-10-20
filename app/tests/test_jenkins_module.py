# import jenkinsapi
from jenkinsapi.jenkins import Jenkins
import pytest

@pytest.mark.skip
def test_connect():
    host = ""
    usernmae = ""
    password = ""

    jenkins_client = Jenkins(host,
                             username=usernmae,
                             password=password)

    for item in jenkins_client.items():
        print(item)


@pytest.mark.skip
def test_get_alljobs():
    host = ""
    usernmae = ""
    password = ""

    jenkins_client = Jenkins(host,
                             username=usernmae,
                             password=password)

    for item in jenkins_client.items():
        print(item)
