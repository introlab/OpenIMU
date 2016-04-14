find_package(Qt5Core    REQUIRED)
find_package(Qt5Gui     REQUIRED)
find_package(Qt5Widgets REQUIRED)


SET(srcs
    vblabel_plugin.cpp
    vblabel.cpp
)

SET(headers
    vblabel_plugin.h
    vblabel.h
)

SET(uis

)

SET(qrc

)

SET(qml
    vbLabel.qml
)

#Required for ui_ files includes
include_directories(
    ${CMAKE_CURRENT_BINARY_DIR}
    )

# generate rules for building source files from the resources
QT5_ADD_RESOURCES(srcs_qrc ${qrc})

#Generate .h files from the .ui files
QT5_WRAP_UI(moc_uis ${uis})

#This will generate moc_* for Qt
QT5_WRAP_CPP(moc_srcs ${headers})


add_library(vbLabel SHARED ${srcs} ${headers} ${moc_srcs} ${moc_uis} ${srcs_qrc} ${qml})
qt5_use_modules(vbLabel Sql Core Network Xml XmlPatterns Gui Widgets Qml Quick)



#Test applications with dependencies
#add_executable(test_BLED112-Foracare test_BLED112-ForaCare.cpp ${srcs} ${headers} ${moc_srcs} ${moc_uis} ${srcs_qrc})
#qt5_use_modules(test_BLED112-Foracare Sql Core Network Xml XmlPatterns Gui Widgets)
#TARGET_LINK_LIBRARIES(test_BLED112-Foracare BLED112-ForaCare ${QWT6_LIBS})





