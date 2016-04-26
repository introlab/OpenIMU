add_subdirectory(json)
add_subdirectory(components)

SET(srcs
    ${srcs}
    ${CMAKE_CURRENT_SOURCE_DIR}/caneva.cpp
    PARENT_SCOPE
)

SET(headers
    ${headers}
    ${CMAKE_CURRENT_SOURCE_DIR}/caneva.h
    PARENT_SCOPE
)


