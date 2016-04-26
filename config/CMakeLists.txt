
#We will copy files here in the QML directory
#For installation and for "in QtCreator/dev" use
FILE(GLOB JSON_FILE "${CMAKE_CURRENT_SOURCE_DIR}/*")

MESSAGE(STATUS "COPYING JSON file : ${JSON_FILE}")

#For IN-SOURCE debug
file(COPY ${JSON_FILE} DESTINATION ${EXECUTABLE_OUTPUT_PATH}/config/)


