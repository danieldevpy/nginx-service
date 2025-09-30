from core.domain.helpers.ssl_helper import SSLHelper

helper = SSLHelper()

def test_check_has_ssl(block_server):
    assert helper.check_has_ssl(block_server) == True

def test_remove_ssl(block_server):
    removed_ssl, _ = helper.edit_server_block(block_server, remove=True)
    assert not 'listen 443 ssl' in removed_ssl
    assert not 'ssl_certificate' in removed_ssl
    assert not 'ssl_certificate_key' in removed_ssl
    assert not 'include /etc/letsencrypt' in removed_ssl
    assert not 'ssl_dhparam' in removed_ssl

def test_copy_ssl(block_server):
    _, copy = helper.edit_server_block(block_server)
    rules_ssl = "".join(copy)
    assert 'listen 443 ssl' in rules_ssl
    assert 'ssl_certificate' in rules_ssl
    assert 'ssl_certificate_key' in rules_ssl
    assert 'include /etc/letsencrypt' in rules_ssl
    assert 'ssl_dhparam' in rules_ssl

def test_insert_rules_ssl(block_server):
    
    removed_ssl, copy = helper.edit_server_block(block_server, remove=True)
    assert not 'listen 443 ssl' in removed_ssl
    assert not 'ssl_certificate' in removed_ssl
    assert not 'ssl_certificate_key' in removed_ssl
    assert not 'include /etc/letsencrypt' in removed_ssl
    assert not 'ssl_dhparam' in removed_ssl

    rules_ssl = helper.insert_rules_ssl(removed_ssl, copy)

    assert 'listen 443 ssl' in rules_ssl
    assert 'ssl_certificate' in rules_ssl
    assert 'ssl_certificate_key' in rules_ssl
    assert 'include /etc/letsencrypt' in rules_ssl
    assert 'ssl_dhparam' in rules_ssl
