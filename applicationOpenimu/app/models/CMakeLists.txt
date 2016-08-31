add_subdirectory(json)
add_subdirectory(components)

SET(srcs
    ${srcs}
    ${CMAKE_CURRENT_SOURCE_DIR}/Caneva.cpp
    PARENT_SCOPE
)

SET(headers
    ${headers}
    ${CMAKE_CURRENT_SOURCE_DIR}/Caneva.h
    PARENT_SCOPE
)


