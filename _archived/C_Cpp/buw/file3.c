#define PY_SSIZE_T_CLEAN
#include "Python.h"
#include "dll.h"
#include <pthread.h>

void *thrd_func(void *arg) {
	/*Py_Initialize();*/
	//PyRun_SimpleString("import sys");
	//PyRun_SimpleString("sys.path.append('C:/REAPER/Plugins')");
	PyObject *pModule = NULL;
	PyObject *pFunc = NULL;
	PyObject *arglist;
	pModule = PyImport_ImportModule("__main__");
	pFunc = PyObject_GetAttrString(pModule, "RPR_ShowMessageBox");
	arglist = PyString_FromString("great_module");
	PyEval_CallObject(pFunc, arglist);
	//Py_Finalize();
	pthread_exit(NULL);
}

DLLEXPORT void HelloWorld() {
	pthread_t thread;
	int res;
	void *thrd_ret;
	srand(time(NULL));
	res = pthread_create(&thread, NULL, thrd_func, NULL);
	if (res != 0) {
		exit(res);
	}
	res = pthread_join(thread, &thrd_ret);
}