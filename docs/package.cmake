if(TARGET PythonCalc::Documentation)
    return()
endif()

set(PYTHON_CALC_DOCUMENTATION_PATH "${CMAKE_CURRENT_LIST_DIR}")
set(PYTHON_CALC_DOCUMENTATION_DIRECTORY "SyntaxFolder")

add_executable(PythonCalc::Documentation IMPORTED)

set_target_properties(
    PythonCalc::Documentation
    PROPERTIES
        IMPORTED_LOCATION
            "${PYTHON_CALC_DOCUMENTATION_PATH}/${PYTHON_CALC_DOCUMENTATION_DIRECTORY}"
)
