import math
import MySQLdb


targetDevice = 2
negativeRatting = 5
requesting = 1


# ***************************GET FROM DATABASE START************************



ldb = MySQLdb.connect(
    host="10.1.1.38",    # your host, usually localho st
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
            sql = "SELECT dynamic_trust FROM cloudlet_trust WHERE requestor='%s' AND entertainer='%s' LIMIT 1" % (cloudlets_names[j], cloudlets_names[i])
            ldb_sql.execute(sql)
            ldb.commit()
        except MySQLdb.Error, e:
            print(e)

        trust = ldb_sql.fetchall()
        D[j][i] = float(trust[0][0])



# for i in range(N):
#     print(D[i])

# ***************************BGET FROM DATABASE END************************


# ***************************BROKER PART START************************


def calculatePij(i, j):

    Device = D[i][j]  # To save the value from the array D

    x = 0.0           # To use for addition

# Below calculating Ddidj(t)
    for i in range(N):

        x = float(x) + float(D[i][j])

    Pij = Device / x

    # print(Pij)
    return Pij


def calculatePijlnPij(j):

    x = 0.0
    # print("=========")
    for v in range(N):
        Pij = calculatePij(v, j)
        # print(Pij)

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
    for i in range(N):
        for j in range(N):
            EiTemp = ln * calculatePijlnPij(j)
            # print(EiTemp)  # Temporary only for troubleshooting

            # if i == j:
            E[j] = EiTemp



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
