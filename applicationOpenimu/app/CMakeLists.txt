find_package(Qt5Core    REQUIRED)
find_package(Qt5Gui     REQUIRED)
find_package(Qt5Widgets REQUIRED)
find_package(Qt5Quick   REQUIRED)
find_package(Qt5Charts	REQUIRED)
find_package(Qt5LinguistTools	REQUIRED)
find_package(Qt5QuickControls2	REQUIRED)

add_subdirectory(acquisition)
add_subdirectory(algorithm)
add_subdirectory(core)
add_subdirectory(dialogs)
add_subdirectory(logger)
add_subdirectory(graph)
add_subdirectory(widgets)
add_subdirectory(utils)

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
)

SET(qml

)

#Binary dir Required for ui_ files includes
include_directories(
    ${CMAKE_CURRENT_BINARY_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/core/json
    ${CMAKE_CURRENT_SOURCE_DIR}/views
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


#Application
add_executable(applicationOpenimu Main.cpp ${srcs} ${headers} ${moc_srcs} ${moc_uis} ${srcs_qrc} ${qml} ${qm_files})
qt5_use_modules(applicationOpenimu Sql Core Network Xml XmlPatterns Gui Widgets Quick Charts QuickControls2)
TARGET_LINK_LIBRARIES(applicationOpenimu)






