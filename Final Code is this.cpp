#include<iostream>
#include <bits/stdc++.h>
#include<time.h>

using namespace std;

const int N = 4; //Total number of devices
const int targetDevice = 4; //The target DEVICE
const int requesting = 1; //The requesting deivce
int negativerating[N][N];  // Only for the calculation of Omega negative rating is to be saved;
double dj[N];
double D[N][N];

// double D[N][N] = {{0.3,0.6,0,0.8} , {0.5,0.9,1,0.6} , {0.2,0.4,0.1,0.5} , {0.6,0.5,0.25,1}};

/*******************************************DEVICE PART START***********************************/

void device()
{

	// const int n = 4;
	int i = 2;
	int deltaT = 4;


	double   x, y;
	// double dj[N];

	int positiveRating;
	// int negativerating;
    int negativerating;



	if (deltaT > 0)
	{
		for (int j=0; j < N; j++)
		{
			positiveRating = 0;
			// negativerating[N][N] = 0;
            negativerating = 0;

			double rnd;

			rnd = rand() % 20;





			for (int m=0; m < rnd; m++)
			{


				double tau =  static_cast <float> (rand()) / static_cast <float> (RAND_MAX);


				//cout << "tau:" << tau << "\n";

				if (tau >= 0.5)
				{
					positiveRating++;
					//cout << "postive:" << positiveRating << "\n";


				}
				else if (tau < 0.5)
				{
					negativerating++;
					//cout << "negative:" << negativerating << "\n";

				}
                // negativerating = negativerating[j][m];
			}
			x = positiveRating + 1;
			y = positiveRating + negativerating;
			if (y == 0)
			{
				dj[j] = 0;
			}
			else if (positiveRating != 0 && negativerating == 0)
			{
				dj[j] = 1;
			}
			else
			{
				y += 2;
				dj[j] = x / y;
			}
			// cout << dj[j] << "\n";

		}

	}

}



/*******************************************DEVICE PART END************************************/


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

double broker(int target)
{

    double Fbkdj = 0; //Final output / Return variable


    double random = 0; //Only to complete function requirement of RETURN double

    double E[N]; //To store the value of Ei
    double W[N]; // To store the value of Wi;

    double sE; //Sum of Ei;

    double EiTemp; //used in the calculation of Ei


    // Calculating natural log of N;
    double ln = log(N);
    ln = -(ln);
    ln = 1/ln;


    //To make a matrix from the device to device trust values
    for(int i=0 ; i<N ; i++)
    {
        device(); //Assign values to the dj[], The trust values from a device


        for(int j=0 ; j<N ; j++)
        {
            D[i][j] = dj[j];
        }
    }


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

    for(int i=0 ; i<N ; i++)
    {
        Fbkdj = Fbkdj + (D[i][target] * W[i]);
    }

    return Fbkdj;
}

/*******************************************BROKER PART END*************************************/


/*******************************************GLOBAL TRUST START*************************************/

double calculateOmega(int negitiveR)
{
	double x=sqrt(negitiveR);
	x += 1;
	x = 1 / x;
	return x;

}

double globalTrust(double omega , double dtd , double Fbk)
{
    double Gdidj = (omega*dtd)+((1-omega)*Fbk);
    return Gdidj;
}

/*******************************************GLOBAL TRUST END*************************************/




int main()
{

    double Fbkdj = broker(targetDevice);

    double Gdidj = globalTrust(0.5 , D[requesting][targetDevice] , Fbkdj);

    cout << "\nGlobal Trust Value:" << Gdidj << "\n";


    return 0;
}
