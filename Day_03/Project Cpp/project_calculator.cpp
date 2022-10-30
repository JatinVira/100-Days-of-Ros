#include<iostream>

using namespace std;

class Calculator
{
private:

    double var1 = 0.0;
    double var2 = 0.0;
    int choice = 0;

public:

    void userNumInput()
    {
        cout << "Enter your first number:  " << endl;
        cin >> var1;
        cout << "Enter your second number: " << endl;
        cin >> var2;
    }

    void userCaseInput()
    {
        cout << "Enter 1 for Addition       \n" << "Enter 2 for Subtraction \n"
             << "Enter 3 for Multiplication \n" << "Enter 4 for Division    \n";
        cin >> choice;
    }

    double add()
    {
        return var1 + var2 ;
    }

    double sub()
    {
        return var1 - var2 ;
    }

    double mul()
    {
        return var1 * var2 ;
    }

    double div()
    {
        return var1 / var2 ;
    }

    int getChoice()
    {
        return choice;
    }

    double getVar1()
    {
        return var1;
    }

    double getVar2()
    {
        return var2;
    }
    
}; 


int main()
{
    Calculator cal;
    cal.userNumInput();
    cal.userCaseInput();
    switch(cal.getChoice())
    {
        case(0):
        cout << "Operation not assigned \n";
        break;

        case(1):
        cout << "Addition of " << cal.getVar1() << " and " << cal.getVar2() << " = " << cal.add();
        break;

        case(2):
        cout << "Subtraction of " << cal.getVar1() << " and " << cal.getVar2() << " = " << cal.sub();
        break;

        case(3):
        cout << "Multiplication of " << cal.getVar1() << " and " << cal.getVar2() << " = " << cal.mul();
        break;

        case(4):
        cout << "Division of " << cal.getVar1() << " and " << cal.getVar2() << " = " << cal.div();
        break;

        default:
        cout << "Invalid Operator assigned \n";
        break;

    }
    
    return 0;
}