# データベースのファイル名
dbname = 'problems.sqlite3'
# コンテストセット一覧
contest_sets = [
    {
        'name': 'asakatsu_extra',
        'title': 'あさかつ%-m/%-d EXTRA',
        'memo': 'あさかつ公認のおまけ黄Diff2問（含：試験管）です。 感想戦も同じサーバーでやっています。',
        'everyday_start_time': '07:30',
        'duration_second': 3600,
        'penalty_second': 300,
        'problem_infos': [
            {
                'difficulty_range': (2000, 2199),
                'point': 1,
                'include_experimental': True,
                'duplicate_remove_days': 60
            }
            {
                'difficulty_range': (2200, 2399),
                'point': 1,
                'include_experimental': True,
                'duplicate_remove_days': 60
            }
        ]
    }
]
