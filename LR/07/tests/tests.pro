QT += testlib network xml
QT -= gui

CONFIG += c++11

SOURCES += \
    testgateway.cpp
    ../src/utils/gateway.cpp


HEADERS += \
    testgateway.h
    ../src/utils/gateway.cpp
