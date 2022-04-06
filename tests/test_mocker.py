from unittest.mock import _Call, MagicMock, call, patch
from pytest_recipes import mocked_module
import re


"""
https://myadventuresincoding.wordpress.com/2011/02/26/python-python-mock-cheat-sheet/ 
is an excellent guide on patching classes and class methods

https://benoitgoujon.com/post/six-advanced-pytest-tricks/ contains
- Using caplog fixture instead of mocking log calls
- Using pytest.mark.freeze_time Test time-dependent functions
"""

@patch('pytest_recipes.mocked_module._logger.warn')
def test_patch_one_call_check_args(warn: MagicMock):
    """
    Show use of patch decorator with partial argument matching
    """

    mocked_module.call_warn("shit happens")

    arg0: str = warn.call_args_list[0].args[0]

    assert arg0.startswith("shit hap")
    assert len(warn.call_args_list[0].kwargs) == 0


@patch('pytest_recipes.mocked_module._logger.warn')
@patch('pytest_recipes.mocked_module._logger.fatal')
def test_patching_two_calls(fatal: MagicMock, warn: MagicMock):
    """
    Same as above, but two calls patched, notice reverse order of parameters and @patch definitions
    """

    mocked_module.call_warn("shit happens")
    mocked_module.call_fatal("shit really happens")

    warn.assert_called_once()
    fatal.assert_has_calls([call("shit really happens")])


def assert_matches(regex, string):
    assert re.match(regex, string), f"'{string}' did not match regex '{regex}'"

@patch('pytest_recipes.mocked_module._logger.warn')
def test_matching_with_regex(warn: MagicMock):
    """
    Match args using Regular expression
    """

    mocked_module.call_warn("shit happens")

    assert_matches("shit.+ens$", warn.call_args_list[0].args[0])


"""
Below is tests showing use of mocker fixture and explicit patching instead of using @patch decorator
"""

def test_mocker_one_call_check_args(mocker: MagicMock):
    mocker.patch('pytest_recipes.mocked_module._logger.warn', return_value=None)

    mocked_module.call_warn("shit happens")

    assert mocked_module._logger.warn.call_args_list[0].args[0] == "shit happens"
    assert len(mocked_module._logger.warn.call_args_list[0].kwargs) == 0


def test_mocker_two_calls_check_second_args(mocker: MagicMock):
    mocker.patch('pytest_recipes.mocked_module._logger.warn', return_value=None)

    mocked_module.call_warn("shit happens")
    mocked_module.call_warn("shit happens 2", "twice 2", kw="sometimes")

    assert mocked_module._logger.warn.call_args_list[1].args[0] == "shit happens 2"
    assert mocked_module._logger.warn.call_args_list[1].args[1] == "twice 2"
    assert mocked_module._logger.warn.call_args_list[1].kwargs["kw"] == "sometimes"


def test_mocker_one_call_check_args_via_types(mocker: MagicMock):
    mocker.patch('pytest_recipes.mocked_module._logger.warn', return_value=None)

    mocked_module.call_warn("shit happens")
    mocked_module.call_warn("shit happens 2", "twice 2", kw="sometimes")

    assert len(mocked_module._logger.warn.call_args_list) == 2
    call = mocked_module._logger.warn.call_args_list[0]
    assert type(call) == _Call
    args = call.args
    kwargs = call.kwargs
    assert type(call.args) == tuple
    assert call.args == ("shit happens",)
    assert type(kwargs) == dict
    assert args[0] == "shit happens"
