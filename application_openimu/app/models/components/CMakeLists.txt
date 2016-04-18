add_subdirectory(blockType)

SET(srcs
    ${srcs}
    ${CMAKE_CURRENT_SOURCE_DIR}/abstractinputnode.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/abstractoutputnode.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/block.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/blockgenerator.cpp
    PARENT_SCOPE
)

SET(headers
    ${headers}
    ${CMAKE_CURRENT_SOURCE_DIR}/abstractinputnode.h
    ${CMAKE_CURRENT_SOURCE_DIR}/abstractoutputnode.h
    ${CMAKE_CURRENT_SOURCE_DIR}/block.h
    ${CMAKE_CURRENT_SOURCE_DIR}/blockgenerator.h
    ${CMAKE_CURRENT_SOURCE_DIR}/blockplugin.h
    ${CMAKE_CURRENT_SOURCE_DIR}/inputnode.h
    ${CMAKE_CURRENT_SOURCE_DIR}/observer.h
    ${CMAKE_CURRENT_SOURCE_DIR}/outputnode.h
    ${CMAKE_CURRENT_SOURCE_DIR}/quickiteminputnodes.h
    ${CMAKE_CURRENT_SOURCE_DIR}/quickiteminputnodeshandles.h
    ${CMAKE_CURRENT_SOURCE_DIR}/quickitemoutputnodes.h
    ${CMAKE_CURRENT_SOURCE_DIR}/workerthreads.h
    PARENT_SCOPE
)


