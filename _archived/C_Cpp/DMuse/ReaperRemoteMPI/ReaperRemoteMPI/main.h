#ifndef _DLL_H_
#define _DLL_H_

#define DLLEXPORT __declspec(dllexport)

DLLEXPORT void PushMsg(char *, int);
DLLEXPORT int GetMsg(char *);
DLLEXPORT void Listen(char *, char *, int);

#endif
