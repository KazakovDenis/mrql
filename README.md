# mrql

`library in progress`

MongoDB Readable Query Language library.

It helps to convert ugly pipelines like this one:
```python
pipeline = [
    {'$match': {'users.u': user_id}},
    {'$limit': limit},
    {
        '$set': {
            'base_user': {
                '$arrayElemAt': [
                    {
                        '$filter': {
                            'input': '$users',
                            'as': 'user',
                            'cond': {'$eq': ['$$user.u', user_id]},
                        }
                    },
                    0,
                ]
            }
        }
    },
    {
        '$project': {
            '_id': 1,
            'users': {
                '$map': {
                    'input': {
                        '$slice': [
                            {
                                '$sortArray': {
                                    'input': {
                                        '$filter': {
                                            'input': '$users',
                                            'as': 'user',
                                            'cond': {
                                                '$and': [
                                                    {'$ne': ['$$user.p', '$base_user.p']},
                                                    {'$gte': ['$$user.t', since_dt]}
                                                    if since_dt
                                                    else {},
                                                ]
                                            },
                                        }
                                    },
                                    'sortBy': {'t': -1},
                                }
                            },
                            limit,
                        ]
                    },
                    'as': 'user',
                    'in': '$$user.u',
                }
            },
        }
    },
]
```

to a human-readable one:
```python
from mrql import get_default_compiler

query = """
MATCH users.u = @user_id;

LIMIT @limit;

SET base_user = ARRAYELEMAT(
    FILTER($users, user, EQ(user.u, @user_id)),
    0
);

PROJECT _id, 
    users = MAP(
        SLICE(
            SORTARRAY(
                FILTER($users, user, AND(
                    NE(user.p, base_user.p),
                    GTE(user.t, @since_dt)
                )),
                {t: -1}
            ),
            @limit
        ),
        user,
        user.u
    )
"""
params = { ... }
compiler = get_default_compiler()
pipeline = compiler(query, user_id=user_id, since_dt=since_dt, limit=limit)  # the same pipeline
```
