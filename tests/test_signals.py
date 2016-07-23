def test_signal_registration(basicApp):
    plugin = basicApp.plugins.get("BasicPlugin")
    signals = plugin.signals.get()
    assert len(signals.keys()) == 1
    assert "test" in signals.keys()


def test_signal_send(basicApp):
    answers = basicApp.signals.send("test", basicApp)
    assert len(answers) == 1
    assert isinstance(answers, list)
    assert len(answers[0]) == 2
    assert isinstance(answers[0], tuple)
    assert answers[0][1] == {'text': 'test'}


def test_signal_connect(basicApp):

    def _test_command(plugin, **kwargs):
        return "12345"

    plugin = basicApp.plugins.get("BasicPlugin")
    plugin.signals.connect("12345 receiver", "test", _test_command, "receiver 12345 for test")
    answers = plugin.signals.send("test")
    assert len(answers) == 2
    for answer in answers:
        if answer[0] == _test_command:
            assert answer[1] == "12345"


def test_signal_disconnect(basicApp):
    def _test_command(plugin, **kwargs):
        return "12345"

    plugin = basicApp.plugins.get("BasicPlugin")
    plugin.signals.connect("12345 receiver", "test", _test_command, "receiver 12345 for test")
    answers = plugin.signals.send("test")
    assert len(answers) == 2
    for answer in answers:
        if answer[0] == _test_command:
            assert answer[1] == "12345"

    plugin.signals.disconnect("12345 receiver")
    answers = plugin.signals.send("test")
    assert len(answers) == 1


def test_receiver_get(basicApp):
    def _test_command(plugin, **kwargs):
        return "12345"

    plugin = basicApp.plugins.get("BasicPlugin")
    receivers = plugin.signals.get_receiver()
    assert len(receivers) == 1  # test receiver
    plugin.signals.connect("12345 receiver", "test", _test_command, "receiver 12345 for test")
    receivers = plugin.signals.get_receiver()
    assert len(receivers) == 2
    plugin.deactivate()
    receivers = plugin.signals.get_receiver()
    assert len(receivers) == 0



