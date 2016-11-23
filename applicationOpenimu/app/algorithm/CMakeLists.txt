add_subdirectory(podometer)

SET(srcs
    ${srcs}
    
    ${CMAKE_CURRENT_SOURCE_DIR}/AlgorithmInfo.cpp
	${CMAKE_CURRENT_SOURCE_DIR}/AlgorithmInfoSerializer.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/AlgorithmOutputInfo.cpp
	${CMAKE_CURRENT_SOURCE_DIR}/AlgorithmOutputInfoSerializer.cpp
    PARENT_SCOPE
)

SET(headers
    ${headers}
    ${CMAKE_CURRENT_SOURCE_DIR}/AlgorithmInfo.h
	${CMAKE_CURRENT_SOURCE_DIR}/AlgorithmInfoSerializer.h
    ${CMAKE_CURRENT_SOURCE_DIR}/AlgorithmOutputInfo.h
    ${CMAKE_CURRENT_SOURCE_DIR}/AlgorithmOutputInfoSerializer.h
    PARENT_SCOPE
)
