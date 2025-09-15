import textwrap

from mrql import get_default_compiler

done = textwrap.dedent("""
    MATCH foo="bar"; 
    LIMIT 1;
""")  # noqa: W291

todo = textwrap.dedent("""
MATCH users.u = @user_id;

LIMIT @limit;

SET base_user = ARRAYELEMAT(
    FILTER($users, user, EQ(user.u, @user_id)),
    0
);

PROJECT 
    _id, 
    users = MAP(
        SLICE(
            SORTARRAY(
                FILTER($users, user, AND( NE(user.p, base_user.p), GTE(user.t, @since_dt) )),
                {t: -1}
            ),
            @limit
        ),
        user,
        user.u
    )
""")  # noqa: W291


if __name__ == '__main__':
    compiler = get_default_compiler()
    print(compiler(done))  # noqa: T201
