import pytest
from moto import mock_s3

from .. import api_to_database as atd


def test_get_all_titles():
    atd.api_url = 'http://muppet.wikia.com/api.php'
    titles = atd.get_all_titles()
    assert len(titles) > 0
    title = titles[0]
    assert isinstance(title, dict)
    assert u'ns' in title
    assert u'pageid' in title
    assert u'title' in title


@mock_s3
def test_set_page_key():
    pass
