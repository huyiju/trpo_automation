QT += testlib
QT -= gui
QT += network
QT += xml
LIBS += -lgcov

QMAKE_CXXFLAGS += -g -fprofile-arcs -ftest-coverage -O0
QMAKE_LFLAGS += -g -fprofile-arcs -ftest-coverage  -O0

SOURCES += \
    ../src/functional.cpp \
    ../src/gateway.cpp \
    ../src/strategylab.cpp \
    ../src/tcpserver.cpp \
    TestTcp.cpp\
    faketcp.cpp

HEADERS += \
    ../src/functional.h \
    ../src/gateway.h \
    ../src/strategylab.h \
    ../src/tcpserver.h \
    TestTcp.h \
    faketcp.h

SUBDIRS += \
    ../src/src.pro

RESOURCES += \
    ../src/resources.qrc

DISTFILES += \
    ../src/config/answerStructure.xml \
    ../src/config/jsonSpecificationForClientRequest.xml


