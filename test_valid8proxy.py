import builtins
import os
import Valid8Proxy as vp


def test_save_proxies_to_file(tmp_path):
    proxies = ['1.1.1.1:80', '2.2.2.2:8080']
    file_path = tmp_path / 'out.txt'
    vp.save_proxies_to_file(proxies, filename=str(file_path))
    assert file_path.read_text() == '1.1.1.1:80\n2.2.2.2:8080\n'


def test_validate_and_print_proxies_respects_limit(monkeypatch):
    proxies = [f'192.168.0.{i}:80' for i in range(5)]
    call_count = {'count': 0}

    def fake_is_proxy_working(proxy):
        call_count['count'] += 1
        return True

    monkeypatch.setattr(vp, 'is_proxy_working', fake_is_proxy_working)
    vp.stop_code = False
    working = vp.validate_and_print_proxies(proxies, print_limit=3)
    assert len(working) == 3
    assert set(proxies[:3]) == working
    assert call_count['count'] == 3
