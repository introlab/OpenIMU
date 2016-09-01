add_subdirectory(blockType)

SET(srcs
    ${srcs}
    ${CMAKE_CURRENT_SOURCE_DIR}/AbstractInputNode.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/AbstractOutputNode.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/Block.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/BlockGenerator.cpp
    PARENT_SCOPE
)

SET(headers
    ${headers}
    ${CMAKE_CURRENT_SOURCE_DIR}/AbstractInputNode.h
    ${CMAKE_CURRENT_SOURCE_DIR}/AbstractOutputNode.h
    ${CMAKE_CURRENT_SOURCE_DIR}/Block.h
    ${CMAKE_CURRENT_SOURCE_DIR}/BlockGenerator.h
    ${CMAKE_CURRENT_SOURCE_DIR}/BlockPlugin.h
    ${CMAKE_CURRENT_SOURCE_DIR}/InputNode.h
    ${CMAKE_CURRENT_SOURCE_DIR}/Observer.h
    ${CMAKE_CURRENT_SOURCE_DIR}/Outputnode.h
    ${CMAKE_CURRENT_SOURCE_DIR}/QuickItemInputNodes.h
    ${CMAKE_CURRENT_SOURCE_DIR}/QuickItemInputNodesHandles.h
    ${CMAKE_CURRENT_SOURCE_DIR}/QuickItemOutputNodes.h
    ${CMAKE_CURRENT_SOURCE_DIR}/WorkerThreads.h
    PARENT_SCOPE
)


