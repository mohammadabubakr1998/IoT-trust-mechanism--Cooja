#include<iostream>
#include <bits/stdc++.h>
#include<time.h>

using namespace std;

const int N = 4;
double D[N][N] = {{0.3,0.6,0,0.8} , {0.5,0.9,1,0.6} , {0.2,0.4,0.1,0.5} , {0.6,0.5,0.25,1}};


/**********************************************BROKER PART START*************************************/
double calculatePij(int i, int j)
{
    double Pij; //Return Variable

    double Device = D[i][j]; //To save the value from the array D
    double x = 0; //To use for the addition

    //Below calculating ∑ Ddidj(Δt)
    for(int i=0 ; i<N ; i++)
    {
        x = x + D[i][j];
    }

    Pij = Device / x;

    return Pij;
}


double calculatePijlnPij(int j)
{
    double x = 0; //Return variable and to use in the loop for addition
    double Pij;
    double PijlnPij;

    for(int i=0 ; i<N ; i++)
    {
        Pij = calculatePij(i,j);

        if(Pij==0)
            PijlnPij = 0;
        else
            PijlnPij = Pij * log(Pij);


        x = x + PijlnPij;
    }

    return x;
}

double calculateSumE(double E[])
{
    double x = 0; // Return variable and to be used for calculating sum
    for(int i=0 ; i<N ; i++)
    {
        x = x + E[i];
    }

    return x;
}

double broker()
{
    double random = 0; //Only to complete function requirement of RETURN double

    double E[N]; //To store the value of Ei
    double W[N]; // To store the value of Wi;

    double sE; //Sum of Ei;

    double EiTemp;


    // Calculating natural log of N;
    double ln = log(N);
    ln = -(ln);
    ln = 1/ln;


    // Calculating Ei
    for(int i=0 ; i<N ; i++)
    {
        for(int j=0 ; j<N ; j++)
        {
            EiTemp = ln * calculatePijlnPij(j);

            cout << EiTemp << "\t"; // Temporary only for troubleshooting------------------------

            if(i==j)
            {
                E[i] = EiTemp;
            }

        }

        cout << "\n";
    }

    //Below code is only to display value of E[i] (Only for troubleshooting)----------------------
    cout << "\n\nValues of Ei\n";

    for(int i=0 ; i<N ; i++)
    {
        cout << E[i] << "\t";
    }
    cout << "\n";
    // Till this

    // Calculating Wi
    sE = calculateSumE(E);
    for(int i=0 ; i<N  ; i++)
    {
        W[i] = (1-E[i])/(N-sE);
    }

    return random;
}

/*******************************************BROKER PART END*************************************/



int main()
{

    broker();


    return 0;
}
