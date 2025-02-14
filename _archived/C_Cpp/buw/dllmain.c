/* Replace "dll.h" with the name of your header */
#include <Python.h>
#include "dll.h"
#include <windows.h>
#include <pthread.h>

int mem_size = 10240;
HANDLE hMap_send = NULL, hMap_recv = NULL;
pthread_t tid;
char *addr_send = NULL, *addr_recv = NULL;//, *addr_recv_temp = NULL;

DLLEXPORT void push_message(char *msg, int n) {
	int i;
	for (i = 0; i < n; i++) {
		*(addr_send + i) = msg[i];
	}
	//MessageBox(0, msg, "Message has been sent.", MB_ICONINFORMATION);
}

DLLEXPORT int get_message(char *msg) {
	int i, etx_count = 0, i2 = 0;
	for (i = 0; i < mem_size; i++) {
		if (*(addr_recv + i) == 0x03) {
			etx_count++;
			if (etx_count >= 4) {
				*(msg + i) = *(addr_recv + i);
				break;
			}
		}

		*(msg + i) = *(addr_recv + i);
	}
	return i;
}

void *listening_loop(void *params) {
	/*while(1)
	{
		
	}*/
}

DLLEXPORT void start_listening(char *send_tagname, char *recv_tagname, int mapping_size) {
	//MessageBox(0, "Listening...", "Prompt", MB_ICONINFORMATION);
	if (hMap_send != NULL && hMap_recv != NULL) {
		//MessageBox(0, "Both mappings exist.", "Error", MB_ICONINFORMATION);
		return;
	}
	if (addr_send != NULL && addr_recv != NULL) {
		//MessageBox(0, "Both addresses exist.", "Error", MB_ICONINFORMATION);
		return;
	}
	mem_size = mapping_size;
	hMap_send = CreateFileMapping(INVALID_HANDLE_VALUE, NULL, PAGE_READWRITE, 0, mem_size, send_tagname);
	hMap_recv = CreateFileMapping(INVALID_HANDLE_VALUE, NULL, PAGE_READWRITE, 0, mem_size, recv_tagname);
	if (hMap_send == NULL || hMap_recv == NULL) {
		if (hMap_send == NULL) {
			MessageBox(0, "Failed to create mapping for send.", "Error", MB_ICONINFORMATION);
		}
		if (hMap_recv == NULL) {
			MessageBox(0, "Failed to create mapping for recv.", "Error", MB_ICONINFORMATION);
		}
		CloseHandle(hMap_send);
		CloseHandle(hMap_recv);
		hMap_send = NULL;
		hMap_recv = NULL;
		return;
	}
	addr_send = (char *) MapViewOfFile(hMap_send, FILE_MAP_ALL_ACCESS, 0, 0, mem_size);
	addr_recv = (char *) MapViewOfFile(hMap_recv, FILE_MAP_ALL_ACCESS, 0, 0, mem_size);
	if (addr_send == NULL || addr_recv == NULL) {
		MessageBox(0, "Error occured while mapping view.", "Error", MB_ICONINFORMATION);
		CloseHandle(hMap_send);
		CloseHandle(hMap_recv);
		return;
	}
	int ret;
	ret = pthread_create(&tid, NULL, listening_loop, NULL);
	if (ret != 0) {
		MessageBox(0, "Error occurred while creating thread.", "Error", MB_ICONINFORMATION);
		UnmapViewOfFile(addr_send);
		UnmapViewOfFile(addr_recv);
		CloseHandle(hMap_send);
		CloseHandle(hMap_recv);
	}

	//pthread_exit(NULL);
}

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved) {
	switch (fdwReason) {
		case DLL_PROCESS_ATTACH: {
			break;
		}
		case DLL_PROCESS_DETACH: {
			break;
		}
		case DLL_THREAD_ATTACH: {
			break;
		}
		case DLL_THREAD_DETACH: {
			break;
		}
	}
	/* Return TRUE on success, FALSE on failure */
	return TRUE;
}
