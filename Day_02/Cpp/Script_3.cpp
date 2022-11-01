#include<iostream>

using namespace std;

int sum(int num)
{
    if (num > 0)
    {
        return num + sum(num-1);
    }
    else
    {
        return 0;
    }
}

int main(){

    int x = sum(10);
    cout << x;
    return 0;
}