
#We will copy files here in the QML directory
#For installation and for "in QtCreator/dev" use
FILE(GLOB QML_CHARTS "${CMAKE_CURRENT_SOURCE_DIR}/Charts/*")

MESSAGE(STATUS "COPYING QML Charts : ${QML_CHARTS}")

#For IN-SOURCE debug
file(COPY ${QML_CHARTS} DESTINATION ${EXECUTABLE_OUTPUT_PATH}/jbQuick/Charts)


