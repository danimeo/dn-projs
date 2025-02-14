#ifndef _DLL_H_
#define _DLL_H_

#define DLLEXPORT __declspec(dllexport)

DLLEXPORT void PushMsg(char *, int, int);
DLLEXPORT int GetMsg(char *, int);
DLLEXPORT void Clear(int);
DLLEXPORT void Listen(char *, char *, int, int);

#endif
