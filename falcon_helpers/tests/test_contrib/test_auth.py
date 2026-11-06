import jwt
import pytest
import sqlalchemy as sa
import falcon_helpers.contrib.auth as auth


def test_generate_auth_token():
    # we don't need to hit the db for this test so don't commit it
    u1 = auth.User.testing_create(_commit=False)

    token = u1.generate_auth_token('aud', 'secret')
    result = jwt.decode(token, 'secret', algorithms=['HS512'], audience='aud')
    assert result['sub'] == u1.ident

    token = u1.generate_auth_token('aud', 'secret', additional_data={
        'other': 'true'
    })
    result = jwt.decode(token, 'secret', algorithms=['HS512'], audience='aud')
    assert result['sub'] == u1.ident
    assert result['other'] == 'true'


def test_group_permission_pair_is_unique():
    engine = sa.create_engine('sqlite://')
    with engine.begin() as connection:
        auth.metadata.create_all(connection, tables=[
            auth.Group.__table__,
            auth.Permission.__table__,
            auth.group_permissions,
        ])
        connection.execute(sa.insert(auth.Group).values(id=1, ident='admins'))
        connection.execute(sa.insert(auth.Permission).values(id=1, ident='view'))
        grant = sa.insert(auth.group_permissions).values(group_id=1, permissions_id=1)
        connection.execute(grant)

        with pytest.raises(sa.exc.IntegrityError):
            connection.execute(grant)

        assert connection.scalar(sa.select(sa.func.count()).select_from(
            auth.group_permissions,
        )) == 1
