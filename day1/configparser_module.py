import configparser

config = configparser.ConfigParser()

config['DEFAULT'] = {
    'ServerName': 'Name',
    'Compression': 'yes'
}

config['bitbucket.org'] = {}
config['bitbucket.org']['user'] = 'hg'
config['topsecret.server.com'] = {}
topsecret = config['topsecret.server.com']
topsecret['Host port'] = '9501'
topsecret['Power module'] = 'safe'

with open('example.ini', 'w') as f:
    config.write(f)

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('example.ini')
    print(config.sections())
    print('-' * 50)

    print(config['DEFAULT']['ServerName'])

    print('-'*50)

    for key in config['topsecret.server.com']:
        print(key)

    print(config.options('bitbucket.org'))
    print(config.items('bitbucket.org'))

    print('-'*50)
    print(config.get('bitbucket.org', 'user'))

    config.add_section('money')
    config.set('money', 'diction', 'doc')

    with open('example.ini', 'w') as f:
        config.write(f)

