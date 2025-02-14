#include "main.h"
#include <windows.h>
#include <pthread.h>

int mem_size = 10240;
HANDLE hMap_send = NULL, hMap_recv = NULL;
pthread_t tid;
char *addr_send = NULL, *addr_recv = NULL;

DLLEXPORT void PushMsg(char *msg, int n) {
	int i, n2, j = 0;
	n2 = n + 4;
	for (i = -4; i < n2; i++) {
		if (i < 0) {
			*(addr_send + j++) = '\x02';
		} else if (i >= n) {
			*(addr_send + j++) = '\x03';
		} else {
			*(addr_send + j++) = *(msg + i);
		}
	}
}

DLLEXPORT int GetMsg(char *msg) {
	int i, x0 = 0, x1 = 0, get = 0, n = 0;
	char c;
	for (i = 0; i < mem_size; i++) {
		c = *(addr_recv + i);
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

DLLEXPORT void Listen(char *send_tagname, char *recv_tagname, int m_size) {
	if (hMap_send != NULL && hMap_recv != NULL) {
		return;
	}
	if (addr_send != NULL && addr_recv != NULL) {
		return;
	}
	mem_size = m_size;
	hMap_send = CreateFileMapping(INVALID_HANDLE_VALUE, NULL, PAGE_READWRITE, 0, m_size, send_tagname);
	hMap_recv = CreateFileMapping(INVALID_HANDLE_VALUE, NULL, PAGE_READWRITE, 0, m_size, recv_tagname);
	if (hMap_send == NULL || hMap_recv == NULL) {
		CloseHandle(hMap_send);
		CloseHandle(hMap_recv);
		hMap_send = NULL;
		hMap_recv = NULL;
		return;
	}
	addr_send = (char *) MapViewOfFile(hMap_send, FILE_MAP_ALL_ACCESS, 0, 0, mem_size);
	addr_recv = (char *) MapViewOfFile(hMap_recv, FILE_MAP_ALL_ACCESS, 0, 0, mem_size);
	if (addr_send == NULL || addr_recv == NULL) {
		CloseHandle(hMap_send);
		CloseHandle(hMap_recv);
		return;
	}
}

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
