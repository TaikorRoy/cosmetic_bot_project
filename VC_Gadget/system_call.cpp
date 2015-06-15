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


int LaunchWebServer(string project_base_path) {
	const char* command = "start /b C:\\Anaconda2\\python.exe";
	string webserver_path = project_base_path + "web_server\\ws_app.py";
	const char* file = webserver_path.c_str();
	char full_command[1000];  // declare a container to carry the full command that need to be execuated
	strcpy(full_command, command);
	strcat(full_command, " ");
	strcat(full_command, file);
	int result = system(full_command);
	return result;
}

int LaunchWebBot(string project_base_path) {
	const char* command = "start /b C:\\Anaconda2\\python.exe";
	string webbot_path = project_base_path + "cosmetic_webbot\\main.py";
	const char* file = webbot_path.c_str();
	char full_command[1000];  // declare a container to carry the full command that need to be execuated
	strcpy(full_command, command);
	strcat(full_command, " ");
	strcat(full_command, file);
	int result = system(full_command);
	return result;
}

int main()
{
	string manager_path = ExePath();
	int manager_path_strlen = manager_path.length();
	string project_base_path = manager_path.replace(manager_path_strlen - 24, manager_path_strlen, "");
	
	LaunchWebBot(project_base_path);
	LaunchWebServer(project_base_path);

}




