import datetime
import sqlite3
import random
import re
import requests

import config

dbname = config.dbname
contest_sets = config.contest_sets

conn = sqlite3.connect(dbname)
c = conn.cursor()

contest_names = [contest_set['name'] for contest_set in contest_sets]
if len(contest_names) == 0:
    print('contest_setsが空です')
    exit(0)
contest = contest_sets[0]
if len(contest_names) > 1:
    print('バチャを作成したいコンテストセットを選んでください')
    for i, contest_name in enumerate(contest_names):
        print(f'{i}: {contest_name}')
    contest_index = int(input('番号を入力してください: '))
    while contest_index < 0 or contest_index >= len(contest_names):
        print('番号が不正です')
        contest_index = int(input('番号を入力してください: '))
    contest = contest_sets[contest_index]

c.execute('CREATE TABLE IF NOT EXISTS contest_info (name TEXT PRIMARY KEY, next_start_date DATE)')
c.execute('CREATE TABLE IF NOT EXISTS past_problems (contest_name TEXT, date DATE, problem_id TEXT)')

c.execute('SELECT * FROM contest_info WHERE name = ?', (contest['name'],))
contest_info = c.fetchone()
if contest_info is None:
    date = input('作成するコンテストの開催日を入力してください（YYYY-MM-DD）: ')
    while re.match(r'\d{4}-\d{2}-\d{2}', date) is None:
        print('日付フォーマットが不正です')
        date = input('作成するコンテストの開催日を入力してください（YYYY-MM-DD）: ')
    c.execute('INSERT INTO contest_info VALUES (?, date(?, \'+1 day\'))', (contest['name'], date))
else:
    date = contest_info[1]
    print('次回のコンテストは%sに設定されています' % date)
    if input('変更しますか？（y/n）: ').lower() == 'y':
        date = input('新しい開催日を入力してください（YYYY-MM-DD）: ')
        while re.match(r'\d{4}-\d{2}-\d{2}', date) is None:
            print('日付フォーマットが不正です')
            date = input('新しい開催日を入力してください（YYYY-MM-DD）: ')
        c.execute('UPDATE contest_info SET next_start_date = NEXT_DAY(?, 1) WHERE name = ?', (date, contest['name']))

problem_infos = contest['problem_infos']
problem_json = requests.get('https://kenkoooo.com/atcoder/resources/problem-models.json').json()
problems = []
for i, problem_info in enumerate(problem_infos):
    candidate_problem_ids = []
    difficulty_range = problem_info['difficulty_range']
    include_experimental = problem_info['include_experimental']
    for problem_id in problem_json:
        if not 'difficulty' in problem_json[problem_id]:
            continue
        difficulty = max(0, problem_json[problem_id]['difficulty'])
        if difficulty < difficulty_range[0] or difficulty > difficulty_range[1]:
            continue
        is_experimental = problem_json[problem_id]['is_experimental']
        if not include_experimental and is_experimental:
            continue
        c.execute('SELECT * FROM past_problems WHERE contest_name = ? AND date >= date(?, ?) AND problem_id = ?', (contest['name'], date, '-%d days' % problem_info['duplicate_remove_days'], problem_id))
        if c.fetchone() is not None:
            continue
        candidate_problem_ids.append(problem_id)
    if len(candidate_problem_ids) == 0:
        print('候補問題がありません')
        exit(0)
    problem_id = candidate_problem_ids[random.randint(0, len(candidate_problem_ids) - 1)]
    problems.append({
        'id': problem_id,
        'point': problem_info['point'],
        'order': i
    })

start_dt = datetime.datetime.strptime(date + ' ' + contest['everyday_start_time'], '%Y-%m-%d %H:%M')

token = input('AtCoder Problemsのトークンを入力してください: ')

headers = {
    'Content-Type': 'application/json',
    'Cookie': 'token=' + token
}
r = requests.post('https://kenkoooo.com/atcoder/internal-api/contest/create', headers=headers, json={
    'title': start_dt.strftime(contest['title']),
    'memo': contest['memo'],
    'start_epoch_second': int(start_dt.timestamp()),
    'duration_second': contest['duration_second'],
    'mode': None,
    'is_public': True,
    'penalty_second': contest['penalty_second'],
})
if r.status_code != 200:
    print('コンテストの作成に失敗しました')
    exit(0)
contest_id = r.json()['contest_id']
print('コンテストを作成しました: https://kenkoooo.com/atcoder/#/contest/show/' + contest_id)

r = requests.post('https://kenkoooo.com/atcoder/internal-api/contest/item/update', headers=headers, json={
    'contest_id': contest_id,
    'problems': problems
})
if r.status_code != 200:
    print('コンテストの問題を設定できませんでした')
    exit(0)
print('コンテストの問題を設定しました')

for problem in problems:
    c.execute('INSERT INTO past_problems VALUES (?, ?, ?)', (contest['name'], date, problem['id']))

print('完了しました')
conn.commit()
conn.close()
