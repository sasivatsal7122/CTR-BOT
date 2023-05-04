import random

def get_proxy():
    proxies = [
        '169.197.83.74:6046',
        '169.197.83.74:6170',
        '169.197.83.74:6171',
        '169.197.83.74:8160',
        '169.197.83.74:8162'
    ]
    chosen_proxy = random.choice(proxies)
    proxy_options = {
        'proxy': {
            'http': f'http://ou45v:xfl4quy0@{chosen_proxy}',
            'https': f'http://ou45v:xfl4quy0@{chosen_proxy}',
            'no_proxy': 'localhost,127.0.0.1'
        }
    }
    
    return proxy_options

