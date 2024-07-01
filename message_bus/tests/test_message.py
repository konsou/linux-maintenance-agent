import unittest

from message_bus.message import Message, MessageType


class TestMessage(unittest.TestCase):
    def test_as_dict(self):
        m = Message(
            message_type=MessageType.TEST,
            key="test_key",
            source="test_source",
            value="test_value",
        )
        self.assertEqual(
            {
                "message_type": MessageType.TEST,
                "key": "test_key",
                "source": "test_source",
                "value": "test_value",
            },
            m.as_dict(),
        )

    def test_as_json(self):
        m = Message(
            message_type=MessageType.TEST,
            key="test_key",
            source="test_source",
            value="test_value",
        )
        self.assertEqual(
            """{"message_type": "TEST", "key": "test_key", "source": "test_source", "value": "test_value"}""",
            m.as_json(indent=None),
        )

    def test_from_dict(self):
        dict_vals = {
            "message_type": MessageType.TEST,
            "key": "test_key",
            "source": "test_source",
            "value": "test_value",
        }
        m = Message.from_dict(dict_vals)
        self.assertEqual(dict_vals["key"], m.key)
        self.assertEqual(dict_vals["source"], m.source)
        self.assertEqual(dict_vals["value"], m.value)

    def test_from_json(self):
        json_string = """{"message_type": "TEST", "key": "test_key", "source": "test_source", "value": "test_value"}"""
        m = Message.from_json(json_string)
        self.assertEqual("test_key", m.key)
        self.assertEqual("test_source", m.source)
        self.assertEqual("test_value", m.value)

    def test_from_to_dict(self):
        dict_vals = {
            "message_type": MessageType.TEST,
            "key": "test_key",
            "source": "test_source",
            "value": "test_value",
        }
        m = Message.from_dict(dict_vals)
        self.assertEqual(dict_vals, m.as_dict())

    def test_from_to_json(self):
        json_string = """{"message_type": "TEST", "key": "test_key", "source": "test_source", "value": "test_value"}"""
        m = Message.from_json(json_string)
        self.assertEqual(json_string, m.as_json(indent=None))

    def test_input_data_types_validated(self):
        with self.assertRaises(TypeError, msg="Should validate key"):
            Message(
                message_type=MessageType.TEST,
                key=123,
                source="test_source",
                value="test_value",
            )

        with self.assertRaises(TypeError, msg="Should validate source"):
            Message(
                message_type=MessageType.TEST,
                key="test_key",
                source=set(),
                value="test_value",
            )

        with self.assertRaises(TypeError, msg="Should validate value"):
            Message(
                message_type=MessageType.TEST,
                key="test_key",
                source="test_source",
                value=object(),
            )
