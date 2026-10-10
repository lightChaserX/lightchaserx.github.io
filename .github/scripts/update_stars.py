"""Write assets/data/stars.json with star counts of the GitHub repos linked as "code" in index.html."""
import json, os, re, urllib.request

html = open('index.html', encoding='utf-8').read()
repos = sorted(set(re.findall(r'href="https://github\.com/([\w.-]+/[\w.-]+)/?">code</a>', html)))
headers = {'Accept': 'application/vnd.github+json'}
if os.environ.get('GITHUB_TOKEN'):
    headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']

stars = {}
for repo in repos:
    req = urllib.request.Request('https://api.github.com/repos/' + repo, headers=headers)
    try:
        with urllib.request.urlopen(req) as r:
            stars[repo] = json.load(r)['stargazers_count']
    except Exception as e:
        print('skip', repo, e)

with open('assets/data/stars.json', 'w') as f:
    json.dump(stars, f, indent=1, sort_keys=True)
    f.write('\n')
print(len(stars), 'repos')
