add_subdirectory(podometer)

SET(srcs
    ${srcs}
        ${CMAKE_CURRENT_SOURCE_DIR}/AlgorithmInfoSerializer.cpp
	${CMAKE_CURRENT_SOURCE_DIR}/AlgorithmOutputInfoSerializer.cpp
	${CMAKE_CURRENT_SOURCE_DIR}/FilteredData.cpp
    PARENT_SCOPE
)

SET(headers
    ${headers}
    ${CMAKE_CURRENT_SOURCE_DIR}/AlgorithmInfo.h
    ${CMAKE_CURRENT_SOURCE_DIR}/AlgorithmInfoSerializer.h
    ${CMAKE_CURRENT_SOURCE_DIR}/AlgorithmOutputInfo.h
    ${CMAKE_CURRENT_SOURCE_DIR}/AlgorithmOutputInfoSerializer.h
    ${CMAKE_CURRENT_SOURCE_DIR}/FilteredData.h
    PARENT_SCOPE
)
