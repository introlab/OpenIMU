add_subdirectory(podometer)

SET(srcs
    ${srcs}
    ${CMAKE_CURRENT_SOURCE_DIR}/AlgorithmList.cpp
    PARENT_SCOPE
)

SET(headers
    ${headers}
    ${CMAKE_CURRENT_SOURCE_DIR}/AlgorithmList.h
    PARENT_SCOPE
)
