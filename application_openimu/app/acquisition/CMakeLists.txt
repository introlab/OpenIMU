
SET(srcs
    ${srcs}
    ${CMAKE_CURRENT_SOURCE_DIR}/SensorDataPerDay.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/SensorDataPerHour.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/SensorDataPerSecond.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/SensorReader.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/AccelerometerReader.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/GyroscopeReader.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/MagnetometerReader.cpp
    PARENT_SCOPE
)

SET(headers
    ${headers}
    ${CMAKE_CURRENT_SOURCE_DIR}/SensorDataPerDay.h
    ${CMAKE_CURRENT_SOURCE_DIR}/SensorDataPerHour.h
    ${CMAKE_CURRENT_SOURCE_DIR}/SensorDataPerSecond.h
    ${CMAKE_CURRENT_SOURCE_DIR}/SensorReader.h
    ${CMAKE_CURRENT_SOURCE_DIR}/AccelerometerReader.h
    ${CMAKE_CURRENT_SOURCE_DIR}/GyroscopeReader.h
    ${CMAKE_CURRENT_SOURCE_DIR}/MagnetometerReader.h
    PARENT_SCOPE
)



