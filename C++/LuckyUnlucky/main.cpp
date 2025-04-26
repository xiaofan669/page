#include <windows.h>
#include <shellapi.h>
#include <string>

// 全局变量
HINSTANCE hInst;
const wchar_t* WINDOW_CLASS = L"LuckyUnluckyWindowClass";

// 函数声明
LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);
void OpenHtmlWindows(const wchar_t* htmlFile);
void PositionWindows(HWND* windows, int count);
std::wstring GetExeDirectory();

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, PSTR szCmdLine, int iCmdShow) {
    hInst = hInstance;

    // 注册窗口类
    WNDCLASS wc = {};
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = WINDOW_CLASS;
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wc.hCursor = LoadCursor(nullptr, IDC_ARROW);

    if (!RegisterClass(&wc)) {
        MessageBox(nullptr, L"窗口注册失败!", L"错误", MB_ICONERROR);
        return 0;
    }

    // 创建窗口
    HWND hWnd = CreateWindow(
        WINDOW_CLASS,
        L"选择 Lucky 或 UnLucky",
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, 300, 150,
        nullptr, nullptr, hInstance, nullptr
    );

    if (!hWnd) {
        MessageBox(nullptr, L"窗口创建失败!", L"错误", MB_ICONERROR);
        return 0;
    }

    // 创建按钮
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

    // 消息循环
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
        case 1: // Lucky按钮
            OpenHtmlWindows(L"Lucky.HTML");
            break;
        case 2: // UnLucky按钮
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
    // 获取EXE所在目录
    std::wstring exeDir = GetExeDirectory();
    std::wstring fullPath = exeDir + L"\\" + htmlFile;

    // 打开3个窗口
    HWND windows[3];
    for (int i = 0; i < 3; i++) {
        SHELLEXECUTEINFO sei = { sizeof(sei) };
        sei.lpFile = fullPath.c_str();
        sei.nShow = SW_SHOWNORMAL;
        sei.fMask = SEE_MASK_NOCLOSEPROCESS;

        if (ShellExecuteEx(&sei)) {
            // 等待窗口创建
            Sleep(500); // 等待窗口加载
            windows[i] = FindWindow(nullptr, htmlFile);
            if (!windows[i]) {
                // 如果通过标题找不到，尝试其他方法
                windows[i] = GetShellWindow();
            }
        }
        else {
            // 显示错误信息
            DWORD err = GetLastError();
            wchar_t errMsg[256];
            wsprintf(errMsg, L"无法打开文件: %s\n错误代码: %d", fullPath.c_str(), err);
            MessageBox(nullptr, errMsg, L"错误", MB_ICONERROR);
            return;
        }
    }

    // 排列窗口
    PositionWindows(windows, 3);
}

void PositionWindows(HWND* windows, int count) {
    if (count == 0) return;

    // 获取屏幕尺寸
    int screenWidth = GetSystemMetrics(SM_CXSCREEN);
    int screenHeight = GetSystemMetrics(SM_CYSCREEN);

    // 计算每个窗口的宽度和位置
    int windowWidth = screenWidth / count;
    int windowHeight = screenHeight;

    for (int i = 0; i < count; i++) {
        if (windows[i] && IsWindow(windows[i])) {
            // 设置窗口位置和大小
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

// 获取EXE文件所在目录
std::wstring GetExeDirectory() {
    wchar_t path[MAX_PATH];
    GetModuleFileName(nullptr, path, MAX_PATH);
    std::wstring exePath(path);
    size_t pos = exePath.find_last_of(L"\\/");
    return exePath.substr(0, pos);
}