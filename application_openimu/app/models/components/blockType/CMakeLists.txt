
SET(srcs
    ${srcs}
    ${CMAKE_CURRENT_SOURCE_DIR}/activitytrackerblock.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/addblock.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/blockFactory.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/dbwriteblock.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/divBlock.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/podometerblock.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/subBlock.cpp
    PARENT_SCOPE
)

SET(headers
    ${headers}
    ${CMAKE_CURRENT_SOURCE_DIR}/activitytrackerblock.h
    ${CMAKE_CURRENT_SOURCE_DIR}/addblock.h
    ${CMAKE_CURRENT_SOURCE_DIR}/blockFactory.h
    ${CMAKE_CURRENT_SOURCE_DIR}/blockType.h
    ${CMAKE_CURRENT_SOURCE_DIR}/dbwriteblock.h
    ${CMAKE_CURRENT_SOURCE_DIR}/divBlock.h
    ${CMAKE_CURRENT_SOURCE_DIR}/podometerblock.h
    ${CMAKE_CURRENT_SOURCE_DIR}/subBlock.h
    PARENT_SCOPE
)


