#include <windows.h>
#include <shellapi.h>
#include <string>

// ȫ�ֱ���
HINSTANCE hInst;
const wchar_t* WINDOW_CLASS = L"LuckyUnluckyWindowClass";

// ��������
LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);
void OpenHtmlWindows(const wchar_t* htmlFile);
void PositionWindows(HWND* windows, int count);
std::wstring GetExeDirectory();

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, PSTR szCmdLine, int iCmdShow) {
    hInst = hInstance;

    // ע�ᴰ����
    WNDCLASS wc = {};
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = WINDOW_CLASS;
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wc.hCursor = LoadCursor(nullptr, IDC_ARROW);

    if (!RegisterClass(&wc)) {
        MessageBox(nullptr, L"����ע��ʧ��!", L"����", MB_ICONERROR);
        return 0;
    }

    // ��������
    HWND hWnd = CreateWindow(
        WINDOW_CLASS,
        L"ѡ�� Lucky �� UnLucky",
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, 300, 150,
        nullptr, nullptr, hInstance, nullptr
    );

    if (!hWnd) {
        MessageBox(nullptr, L"���ڴ���ʧ��!", L"����", MB_ICONERROR);
        return 0;
    }

    // ������ť
    CreateWindow(
        L"BUTTON", L"Lucky",
        WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON,
        50, 30, 80, 30,
        hWnd, (HMENU)1, hInstance, nullptr
    );

    CreateWindow(
        L"BUTTON", L"UnLucky",
        WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON,
        150, 30, 80, 30,
        hWnd, (HMENU)2, hInstance, nullptr
    );

    ShowWindow(hWnd, iCmdShow);
    UpdateWindow(hWnd);

    // ��Ϣѭ��
    MSG msg;
    while (GetMessage(&msg, nullptr, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return (int)msg.wParam;
}

LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam) {
    switch (message) {
    case WM_COMMAND:
        switch (LOWORD(wParam)) {
        case 1: // Lucky��ť
            OpenHtmlWindows(L"Lucky.HTML");
            break;
        case 2: // UnLucky��ť
            OpenHtmlWindows(L"UnLucky.HTML");
            break;
        }
        break;
    case WM_DESTROY:
        PostQuitMessage(0);
        break;
    default:
        return DefWindowProc(hWnd, message, wParam, lParam);
    }
    return 0;
}

void OpenHtmlWindows(const wchar_t* htmlFile) {
    // ��ȡEXE����Ŀ¼
    std::wstring exeDir = GetExeDirectory();
    std::wstring fullPath = exeDir + L"\\" + htmlFile;

    // ��3������
    HWND windows[3];
    for (int i = 0; i < 3; i++) {
        SHELLEXECUTEINFO sei = { sizeof(sei) };
        sei.lpFile = fullPath.c_str();
        sei.nShow = SW_SHOWNORMAL;
        sei.fMask = SEE_MASK_NOCLOSEPROCESS;

        if (ShellExecuteEx(&sei)) {
            // �ȴ����ڴ���
            Sleep(500); // �ȴ����ڼ���
            windows[i] = FindWindow(nullptr, htmlFile);
            if (!windows[i]) {
                // ���ͨ�������Ҳ�����������������
                windows[i] = GetShellWindow();
            }
        }
        else {
            // ��ʾ������Ϣ
            DWORD err = GetLastError();
            wchar_t errMsg[256];
            wsprintf(errMsg, L"�޷����ļ�: %s\n�������: %d", fullPath.c_str(), err);
            MessageBox(nullptr, errMsg, L"����", MB_ICONERROR);
            return;
        }
    }

    // ���д���
    PositionWindows(windows, 3);
}

void PositionWindows(HWND* windows, int count) {
    if (count == 0) return;

    // ��ȡ��Ļ�ߴ�
    int screenWidth = GetSystemMetrics(SM_CXSCREEN);
    int screenHeight = GetSystemMetrics(SM_CYSCREEN);

    // ����ÿ�����ڵĿ�Ⱥ�λ��
    int windowWidth = screenWidth / count;
    int windowHeight = screenHeight;

    for (int i = 0; i < count; i++) {
        if (windows[i] && IsWindow(windows[i])) {
            // ���ô���λ�úʹ�С
            SetWindowPos(
                windows[i],
                HWND_TOP,
                i * windowWidth,
                0,
                windowWidth,
                windowHeight,
                SWP_SHOWWINDOW
            );
        }
    }
}

// ��ȡEXE�ļ�����Ŀ¼
std::wstring GetExeDirectory() {
    wchar_t path[MAX_PATH];
    GetModuleFileName(nullptr, path, MAX_PATH);
    std::wstring exePath(path);
    size_t pos = exePath.find_last_of(L"\\/");
    return exePath.substr(0, pos);
}