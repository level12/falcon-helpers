import pathlib
import tempfile
import falcon_helpers.contrib.storage as storage


class TestLocalFileStore:
    def test_save_does_not_require_path(self):
        with tempfile.TemporaryDirectory() as d:
            store = storage.LocalFileStore(d, uidgen=lambda: 'unique-name')

            with tempfile.NamedTemporaryFile() as f:
                doc = store.save(f.name, f)
                assert doc.uid == 'unique-name'
                assert doc.name == f.name
                assert doc.path == str(pathlib.Path(d).joinpath(doc.uid))

            with tempfile.NamedTemporaryFile() as f:
                doc = store.save(f.name, f, path='other')
                assert doc.uid == 'unique-name'
                assert doc.name == f.name
                assert doc.path == str(pathlib.Path(d).joinpath('other', doc.uid))

