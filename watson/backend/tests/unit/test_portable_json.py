from app.db.types import PortableJSON


def test_portable_json_round_trip_keeps_accents():
    column = PortableJSON()
    stored = column.process_bind_param({"motivo": "Não reconheço"}, dialect=None)

    assert stored == '{"motivo": "Não reconheço"}'
    assert column.process_result_value(stored, dialect=None) == {"motivo": "Não reconheço"}
