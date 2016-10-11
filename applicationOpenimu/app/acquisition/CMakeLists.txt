
SET(srcs
    ${srcs}
    ${CMAKE_CURRENT_SOURCE_DIR}/WimuAcquisition.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/CJsonSerializer.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/WimuRecord.cpp
    PARENT_SCOPE
)

SET(headers
    ${headers}
    ${CMAKE_CURRENT_SOURCE_DIR}/WimuAcquisition.h
    ${CMAKE_CURRENT_SOURCE_DIR}/WimuRecord.h
    ${CMAKE_CURRENT_SOURCE_DIR}/CJsonSerializer.h
    ${CMAKE_CURRENT_SOURCE_DIR}/IJsonSerializable.h
    PARENT_SCOPE
)



