#define PY_SSIZE_T_CLEAN
#include <stdio.h>
#include "Python.h"
#include <pthread.h>

void *thrd_func(void *arg) { 
    Py_Initialize();
    PyRun_SimpleString("import sys");
	PyRun_SimpleString("sys.path.append('C:\\REAPER\\Plugins')");
	PyObject *pModule = NULL;
	PyObject *pFunc = NULL;
	PyObject *arglist;
	pModule = PyImport_ImportModule("reaper_python");
	printf("11111 %x\n", pModule);
	pFunc = PyObject_GetAttrString(pModule, "RPR_ShowConsoleMsg");
	arglist = PyString_FromString("great_module");
	PyEval_CallObject(pFunc, arglist);
	Py_Finalize();
    pthread_exit(NULL);
}

void HelloWorld() {
	pthread_t thread;
    int no = 0, res;
    void * thrd_ret;
    srand(time(NULL));
    res = pthread_create(&thread, NULL, thrd_func, (void*)no);
    if (res != 0) {
        exit(res);
    }
    res = pthread_join(thread, &thrd_ret);
}

int main() {
	HelloWorld();
	getchar();
	return 0;
}