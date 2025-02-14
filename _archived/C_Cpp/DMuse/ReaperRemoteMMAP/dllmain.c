#include "dll.h"
#include <windows.h>
#include <string.h>

int ch0_size = 256, ch1_size = 10240;
HANDLE *hMap_ch0 = NULL, *hMap_ch1 = NULL;
char *addr_ch0 = NULL, *addr_ch1 = NULL;

DLLEXPORT void PushMsg(char *msg, int msg_channel, int n) {
    char *addr = msg_channel == 0 ? addr_ch0 : addr_ch1;
	int i, n2, j = 0;
	n2 = n + 4;
	for (i = -4; i < n2; i++) {
		if (i < 0) {
			*(addr + j++) = '\x02';
		} else if (i >= n) {
			*(addr + j++) = '\x03';
		} else {
			*(addr + j++) = *(msg + i);
		}
	}
}

DLLEXPORT int GetMsg(char *msg, int msg_channel) {
    char *addr = msg_channel == 0 ? addr_ch0 : addr_ch1;
    int size = msg_channel == 0 ? ch0_size : ch1_size;
    int i, x0 = 0, x1 = 0, get = 0, n = 0;
	char c;
	for (i = 0; i < size; i++) {
		c = *(addr + i);
		if (c == 0x02) {
			x0++;
			if (x0 == 4) {
				get = 1;
			}
			continue;
		} else {
			x0 = 0;
		}
		if (c == 0x03) {
			x1++;
			if (x1 == 4) {
				get = 0;
			}
			continue;
		} else {
			x1 = 0;
		}
		if (get) {
			*(msg + n++) = c;
		}
	}
	*(msg + n) = '\0';
	return n;
}

DLLEXPORT void Clear(int channel) {
    if(channel == 0){
        memset(addr_ch0, 0, ch0_size);
    }else{
        memset(addr_ch1, 0, ch1_size);
    }
}

DLLEXPORT void Listen(char *ch0_tagname, char *ch1_tagname, int c_size, int d_size) {
		if (hMap_ch0 != NULL && hMap_ch1 != NULL) {
			return;
		}
		if (addr_ch0 != NULL && addr_ch1 != NULL) {
			return;
		}
		ch0_size = c_size;
		ch1_size = d_size;
		hMap_ch0 = CreateFileMapping(INVALID_HANDLE_VALUE, NULL, PAGE_READWRITE, 0, ch0_size, ch0_tagname);
		hMap_ch1 = CreateFileMapping(INVALID_HANDLE_VALUE, NULL, PAGE_READWRITE, 0, ch1_size, ch1_tagname);
		if (hMap_ch0 == NULL || hMap_ch1 == NULL) {
			CloseHandle(hMap_ch0);
			CloseHandle(hMap_ch1);
			hMap_ch0 = NULL;
			hMap_ch1 = NULL;
			return;
		}
		addr_ch0 = (char *) MapViewOfFile(hMap_ch0, FILE_MAP_ALL_ACCESS, 0, 0, ch0_size);
		addr_ch1 = (char *) MapViewOfFile(hMap_ch1, FILE_MAP_ALL_ACCESS, 0, 0, ch1_size);
		if (addr_ch0 == NULL || addr_ch1 == NULL) {
			CloseHandle(hMap_ch0);
			CloseHandle(hMap_ch1);
			return;
		}

}

/*char * sentence(char *begin, char *end){
    for(char *c=begin; c < end; c++){

    }
}

DLLEXPORT char * GetInterpret(char *msg, int n){
    char *begin, *end, **sents[64];
    begin = msg, end = msg + n;
    while((end = strchr(msg, ';')) != NULL){
        for(char *c=begin; c < end; c++){

        }

    }
}*/

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved) {
	switch (fdwReason) {
		case DLL_PROCESS_ATTACH:
			break;
		case DLL_PROCESS_DETACH:
			break;
		case DLL_THREAD_ATTACH:
			break;
		case DLL_THREAD_DETACH:
			break;
	}

	return TRUE;
}
