#ifndef _DLL_H_
#define _DLL_H_

#define DLLEXPORT __declspec(dllexport)

DLLEXPORT void push_message(char *msg, int n);
DLLEXPORT int get_message(char *msg);
DLLEXPORT void start_listening(char *send_tagname, char *recv_tagname, int mapping_size);
DLLEXPORT void HelloWorld();

#endif
