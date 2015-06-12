#include <stdlib.h>
#include <iostream>
#include <string.h>
#include <time.h>
#include <windows.h>
#include <ostream>

using namespace std;

string ExePath() {
	TCHAR buffer[MAX_PATH];
	GetModuleFileName(NULL, buffer, MAX_PATH);
	return string(buffer);
}

int main()
{
	string s = ExePath();
	string web_bot = s + "cosmetic_webbot\\main.py";
	a = system(web_bot);
	Sleep(3000);
	
	string s = ExePath();
	//printf("%s\n", s.c_str());
	Sleep(30000);

}