import pytest
from software_design_patterns.behavioral.interpreter_pattern import *


def test_interpreter_rust_to_python():
    RUST_CODE = """fn add(x: i32, y: i32) -> i32 {
    let result = x + y;
    return result;
}"""
    EXPECTED_PYTHON_CODE = """def add(x: int, y: int) -> int:
    result = x + y
    return result
"""
    rs_to_py_interpreter = RustToPythonInterpreter()
    python_code = rs_to_py_interpreter.interpret(RUST_CODE)
    assert python_code == EXPECTED_PYTHON_CODE

    local_scope = {}
    exec(python_code, {}, local_scope)
    assert local_scope["add"](2, 3) == 5

    py_to_rs_interpreter = PythonToRustInterpreter()
    rust_code_converted_back = py_to_rs_interpreter.interpret(python_code)
    assert rust_code_converted_back == RUST_CODE
