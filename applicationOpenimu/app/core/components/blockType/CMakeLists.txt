
SET(srcs
    ${srcs}
    ${CMAKE_CURRENT_SOURCE_DIR}/ActivityTrackerBlock.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/AddBlock.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/BlockFactory.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/DbWriteBlock.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/DivBlock.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/DbBlock.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/PodometerBlock.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/SubBlock.cpp
    PARENT_SCOPE
)

SET(headers
    ${headers}
    ${CMAKE_CURRENT_SOURCE_DIR}/ActivityTrackerBlock.h
    ${CMAKE_CURRENT_SOURCE_DIR}/Addblock.h
    ${CMAKE_CURRENT_SOURCE_DIR}/BlockFactory.h
    ${CMAKE_CURRENT_SOURCE_DIR}/BlockType.h
    ${CMAKE_CURRENT_SOURCE_DIR}/DbWriteBlock.h
    ${CMAKE_CURRENT_SOURCE_DIR}/DivBlock.h
    ${CMAKE_CURRENT_SOURCE_DIR}/DbBlock.h
    ${CMAKE_CURRENT_SOURCE_DIR}/PodometerBlock.h
    ${CMAKE_CURRENT_SOURCE_DIR}/SubBlock.h
    PARENT_SCOPE
)


