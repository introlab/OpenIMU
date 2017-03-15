find_package(Qt5Core    REQUIRED)
find_package(Qt5Gui     REQUIRED)
find_package(Qt5Widgets REQUIRED)
find_package(Qt5Quick   REQUIRED)
find_package(Qt5Charts	REQUIRED)
find_package(Qt5LinguistTools	REQUIRED)
find_package(Qt5QuickControls2	REQUIRED)
find_package(Qt5Multimedia	REQUIRED)

add_subdirectory(acquisition)
add_subdirectory(algorithm)
add_subdirectory(core)
add_subdirectory(dialogs)
add_subdirectory(logger)
add_subdirectory(graph)
add_subdirectory(widgets)
add_subdirectory(utilities)

SET(srcs
    ${srcs}
    AccdataDisplay.cpp
    MainWindow.cpp
)

SET(headers
    ${headers}
    AccDataDisplay.h
    MainWindow.h
)

SET(uis
    ${uis}
    widget.ui
    help.ui
    about.ui
    FullGraphDialog.ui
    AccDataDisplay.ui
)

SET(qrc
    qml.qrc
    images.qrc
    audio.qrc
)

SET(qml

)

#Binary dir Required for ui_ files includes
include_directories(
    ${CMAKE_CURRENT_BINARY_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/core/json
    ${CMAKE_CURRENT_SOURCE_DIR}/views
    ${CMAKE_CURRENT_SOURCE_DIR}/widgets
    ${CMAKE_CURRENT_SOURCE_DIR}/widgets/MRichTextEditor
    )

# Generate and update translation files
SET(FILES_TO_TRANSLATE ${FILES_TO_TRANSLATE} ${headers} ${srcs} ${uis})

QT5_CREATE_TRANSLATION(qm_files ${FILES_TO_TRANSLATE} ../translations/openImu_fr.ts ../translations/openImu_en.ts)
#QT5_ADD_TRANSLATION(qm_files ../translations/openImu_fr.ts ../translations/openImu_en.ts)

# generate rules for building source files from the resources
QT5_ADD_RESOURCES(srcs_qrc ${qrc})

#Generate .h files from the .ui files
QT5_WRAP_UI(moc_uis ${uis})

#This will generate moc_* for Qt
QT5_WRAP_CPP(moc_srcs ${headers})

IF(APPLE)
    # use, i.e. don't skip the full RPATH for the build tree
    SET(CMAKE_SKIP_BUILD_RPATH  FALSE)

    # when building, don't use the install RPATH already
    # (but later on when installing)
    SET(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)

    #Rpath needs to be modified to include frameworks
    set (CMAKE_INSTALL_RPATH "@executable_path/../Frameworks")

    #Application
    add_executable(applicationOpenimu MACOSX_BUNDLE Main.cpp ${srcs} ${headers} ${moc_srcs} ${moc_uis} ${srcs_qrc} ${qml} ${qm_files})
    qt5_use_modules(applicationOpenimu Sql Core Network Xml XmlPatterns Gui Widgets Quick Charts QuickControls2 LinguistTools Multimedia)


    #Make framework directory
    set(FRAMEWORK_PATH "${EXECUTABLE_OUTPUT_PATH}/applicationOpenimu.app/Contents/Frameworks")
    file(MAKE_DIRECTORY ${FRAMEWORK_PATH})

    #Copy all frameworks from QT_INSTALL_LIBS directory!
    #Use Qt executable to query path
    EXEC_PROGRAM(${QT_QMAKE_EXECUTABLE} ARGS "-query QT_INSTALL_LIBS" OUTPUT_VARIABLE QTLIBS)

    file(GLOB QT_FRAMEWORKS "${QTLIBS}/*.Framework")

    foreach(framework ${QT_FRAMEWORKS})
        message(STATUS "Copying ${framework}")
        file(COPY ${framework} DESTINATION ${FRAMEWORK_PATH})
    endforeach(framework)

ELSE(APPLE)

    #Application
    add_executable(applicationOpenimu Main.cpp ${srcs} ${headers} ${moc_srcs} ${moc_uis} ${srcs_qrc} ${qml} ${qm_files})
    qt5_use_modules(applicationOpenimu Sql Core Network Xml XmlPatterns Gui Widgets Quick Charts QuickControls2 LinguistTools Multimedia)
    TARGET_LINK_LIBRARIES(applicationOpenimu)

ENDIF(APPLE)







