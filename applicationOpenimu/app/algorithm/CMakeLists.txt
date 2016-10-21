add_subdirectory(podometer)

SET(srcs
    ${srcs}
    ${CMAKE_CURRENT_SOURCE_DIR}/AlgorithmList.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/AlgorithmOutput.cpp
    PARENT_SCOPE
)

SET(headers
    ${headers}
    ${CMAKE_CURRENT_SOURCE_DIR}/AlgorithmList.h
    ${CMAKE_CURRENT_SOURCE_DIR}/AlgorithmOutput.h
    PARENT_SCOPE
)
