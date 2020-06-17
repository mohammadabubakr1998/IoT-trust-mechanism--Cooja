import math
import MySQLdb


targetDevice = 2
negativeRatting = 5
requesting = 1



# N = 4

# D = [[0.95, 0.9, 0.9, 0.9], [0.95, 0.9, 0.9, 0.9], [0.95, 0.9, 0.9, 0.9], [0.95, 0.9, 0.9, 0.9]]
# D = [[0.5, 0.56, 0.68, 0.73], [0.6, 0.9, 0.53, 0.68], [0.65, 0.76, 0.74, 0.8], [0.8, 0.69, 0.55, 0.58]]
#
# D = [[0.9, 0.8, 0.95, 0.8], [0.86, 0.9, 0.76, 0.89], [0.98, 0.83, 0.94, 0.85], [0.73, 0.88, 0.8, 0.98]]
#
# # D = [[0 for x in range(N)] for y in range(N)]
#
# # D[0][0] = 0.2
# # D[0][1] = 0.3
# # D[0][2] = 0.25
# # D[0][3] = 0.4
# # D[1][0] = 0.56
# # D[1][1] = 0.3
# # D[1][2] = 0.56
# # D[1][3] = 0.29
# # D[2][0] = 0.18
# # D[2][1] = 0.33
# # D[2][2] = 0.44
# # D[2][3] = 0.25
# # D[3][0] = 0.43
# # D[3][1] = 0.38
# # D[3][2] = 0.2
# # D[3][3] = 0.58
# print(D)
# ***************************GET FROM DATABASE START************************



ldb = MySQLdb.connect(
    host="10.1.1.38",    # your host, usually localhost
    user="newuser",         # your username
    passwd="password",  # your password
    db="test2",
    port=3306)

ldb_sql = ldb.cursor()


try:
    sql = "SELECT cloudlet_name FROM cloudlets ORDER BY `cloudlets`.`id` ASC"
    ldb_sql.execute(sql)
    ldb.commit()
except MySQLdb.Error, e:
    print(e)

cloudlets_names_result = ldb_sql.fetchall()
N = ldb_sql.rowcount

cloudlets_names = [None] * N

for x in range(N):
    cloudlets_names[x] = cloudlets_names_result[x][0]

print(cloudlets_names)

D = [[0 for x in range(N)] for y in range(N)]

for i in range(N):
    for j in range(N):

        try:
            sql = "SELECT dynamic_trust FROM cloudlet_trust_40 WHERE requestor='%s' AND entertainer='%s' LIMIT 1" % (cloudlets_names[j], cloudlets_names[i])
            ldb_sql.execute(sql)
            ldb.commit()
        except MySQLdb.Error, e:
            print(e)

        trust = ldb_sql.fetchall()
        D[i][j] = float(trust[0][0])

    print(D[i])

# ***************************BGET FROM DATABASE END************************


# ***************************BROKER PART START************************


def calculatePij(i, j):

    Device = D[j][i]  # To save the value from the array D

    x = 0.0           # To use for addition

# Below calculating Ddidj(t)
    for i in range(N):

        x = float(x) + float(D[j][i])

    Pij = Device / x

    # print(Pij)
    return Pij


def calculatePijlnPij(j):

    x = 0.0
    print("=========")
    for v in range(N):
        Pij = calculatePij(v, j)
        print(Pij)

        if Pij == 0:
            PijlnPij = 0
        else:
            PijlnPij = Pij * math.log(Pij)

        x = x + PijlnPij
    return x


def calculateSumE(E):
    x = 0.0
    for v in range(N):
        x = x + E[v]
    return x


def broker(target):
    Fbkdj = 0.0

    E = [None] * N  # To store the value of Ei
    W = [None] * N  # To store the value of Wi

    # Calculating natural log of N
    ln = math.log(N)
    ln = -(ln)
    ln = 1/ln

    # Calculating Ei
    for j in range(N):
        for i in range(N):
            EiTemp = ln * calculatePijlnPij(i)
            # print(EiTemp)  # Temporary only for troubleshooting

            # if i == j:
            E[i] = EiTemp

        print("--------")

    # Below code is only to display value of E[i](Only for troubleshooting----)

    print("Values of Ei")

    for i in range(N):
        print(E[i])

    # Calculating Wi
    sE = calculateSumE(E)
    print("sE:%s" % (sE))
    for i in range(N):
        W[i] = (1-E[i])/(N-sE)

    print("W:")
    print(W)
    for i in range(N):
        Fbkdj = Fbkdj + (D[i][target-1] * W[i])

    print(Fbkdj)

    return Fbkdj


# **********************************BROKER PART END*******************************

# **********************************GLOBAL TRUST START****************************
def calculateOmega(negativeR):
    x = math.sqrt(negativeR)
    x = x + 1
    x = 1/x
    return x


def globalTrust(omega, dtd, Fbk):
    Gdidj = (omega * dtd) + ((1 - omega) * Fbk)
    return Gdidj


# **********************************GLOBAL TRUST END****************************
Fbkdj = broker(targetDevice)
omega = calculateOmega(negativeRatting)
# omega = 0.1
print("Omega:%s" % (omega))

Gdidj = globalTrust(omega, D[requesting][targetDevice], Fbkdj)

print("Gdidj")
print(Gdidj)
