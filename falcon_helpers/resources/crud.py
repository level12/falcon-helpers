import sqlalchemy as sa
import falcon


class ListBase:
    """A base class for returning list of objects.

    This base class assumes you are using the marshmallow middleware for object
    serialization and sqlalchemy for database access.

    Attributes:
        db_cls: Set this to a SQLAlchemy entity
        schema: Set this a Marshmallow schema
    """
    db_cls = None
    schema = None

    def on_get(self, req, resp):
        result = self.get_objects(req)
        schema = self.schema(many=True)

        resp.status = falcon.HTTP_200
        resp.body = schema.dump(result)

    def get_objects(self, req):
        return self.session.query(self.db_cls).all()


class CrudBase:
    """A very simple CRUD resource.

    This base class assumes you are using the marshmallow middleware for object
    serialization and sqlalchemy for database access.

    Attributes:
        db_cls: Set this to a SQLAlchemy entity
        schema: Set this a Marshmallow schema
    """
    db_cls = None
    schema = None

    def on_get(self, req, resp, obj_id):
        result = self.session.query(self.db_cls).get(obj_id)

        if not result:
            raise falcon.HTTP_404

        schema = self.schema()
        resp.status = falcon.HTTP_200
        resp.body = schema.dump(result)


    def on_put(self, req, resp, obj_id):
        self.session.add(req.context['dto'].data)
        self.session.flush()

        resp.status = falcon.HTTP_200
        resp.body = self.schema().dump(req.context['dto'].data)


    def on_post(self, req, resp, obj_id):
        self.session.add(req.context['dto'].data)
        self.session.flush()

        resp.status = falcon.HTTP_201
        resp.body = self.schema().dump(req.context['dto'].data)


    def on_delete(self, req, resp, obj_id):
        try:
            result = (self.session
                     .query(self.db_cls)
                     .filter_by(id=obj_id)
                     .delete(synchronize_session=False))
        except sa.exc.IntegrityError:
            self.session.rollback()
            resp.status = falcon.HTTP_400
            resp.json = {'errors': [('Unable to delete because the object is '
                                    'connected to other objects')]}
        else:
            resp.status = falcon.HTTP_204
