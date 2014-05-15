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


def test_get_all_revisions():
    atd.api_url = 'http://muppet.wikia.com/api.php'
    titles = atd.get_all_titles()
    title = titles[0]
    all_revisions = atd.get_all_revisions(title)
    assert isinstance(all_revisions, list)
    title_string, revisions = all_revisions
    assert isinstance(title_string, unicode)
    assert isinstance(revisions, list)
    revision = revisions[0]
    assert isinstance(revision, dict)
    assert u'user' in revision
    assert u'userid' in revision
    assert u'revid' in revision
    assert u'parentid' in revision


@mock_s3
def test_set_page_key():
    pass
