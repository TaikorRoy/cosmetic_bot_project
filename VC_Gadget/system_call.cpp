#include <stdlib.h>
#include <iostream>
#include <string.h>
#include <time.h>
#include <windows.h>
#include <ostream>
#include <string>

using namespace std;

string ExePath() {
	TCHAR buffer[MAX_PATH];
	GetModuleFileName(NULL, buffer, MAX_PATH);
	return string(buffer);
}

/*
HINSTANCE launch_webbot(char* project_base_path)
{
	const char* command = "C:\\Anaconda2\\python.exe";
	string webbot_path = project_base_path + "cosmetic_webbot\\main.py";
	const char* file = webbot_path.c_str();
	cout << command;
	cout << "\n";
	cout << file;
	HINSTANCE a = ShellExecute(NULL, command, file, NULL, NULL, 5);
	return a;
}

HINSTANCE launch_webserver(char* project_base_path)
{
	const char* command = "C:\\Anaconda2\\python.exe";
	string webbot_path = project_base_path + "web_server\\ws_app.py";
	const char* file = webbot_path.c_str();
	cout << command;
	cout << "\n";
	cout << file;
	HINSTANCE a = ShellExecute(NULL, command, file, NULL, NULL, 5);
	return a;
}
*/

int main()
{
	string manager_path = ExePath();
	int manager_path_strlen = manager_path.length();
	string project_base_path = manager_path.replace(manager_path_strlen - 13, manager_path_strlen, "");

	const char* command = "C:\\Anaconda2\\python.exe";
	string webbot_path = project_base_path + "cosmetic_webbot\\main.py";
	const char* file = webbot_path.c_str();
	cout << command;
	cout << "\n";
	cout << file;
	HINSTANCE a = ShellExecute(NULL, command, file, NULL, NULL, 5);

	const char* command1 = "C:\\Anaconda2\\python.exe";
	string webbot_path1 = project_base_path + "web_server\\ws_app.py";
	const char* file1 = webbot_path.c_str();
	cout << command1;
	cout << "\n";
	cout << file1;
	HINSTANCE b = ShellExecute(NULL, command1, file1, NULL, NULL, 5);

	Sleep(500000);

	
}