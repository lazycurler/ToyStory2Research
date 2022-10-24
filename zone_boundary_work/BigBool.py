import math
import numpy as np

#bool isInSomeRange(int someZ,int someY,int someX,int midLefZ,int midLefY,int midLefX,int midRigZ,int midRigY,int midRigX,vec3short *scalar,int dis t?)
def isInSomeRange(someZ,
                  someY,
                  someX,
                  midLefZ,
                  midLefY,
                  midLefX,
                  midRigZ,
                  midRigY,
                  midRigX,
                  scalarZ,
                  scalarY,
                  scalarX,
                  dist):

    someZ = np.int32(someZ)
    someY = np.int32(someY)
    someX = np.int32(someX)
    midLefZ = np.int32(midLefZ)
    midLefY = np.int32(midLefY)
    midLefX = np.int32(midLefX)
    midRigZ = np.int32(midRigZ)
    midRigY = np.int32(midRigY)
    midRigX = np.int32(midRigX)
    scalarZ = np.int16(scalarZ)
    scalarY = np.int16(scalarY)
    scalarX = np.int16(scalarX)
    dist = np.int32(dist)

    # mega hacky way to replicate a goto
    def _lab_00480dbe():
        inter3 = someZ * midRigZ + someY * midRigY + someX * midRigX
        radRight = midRigZ * midRigZ + midRigY * midRigY + midRigX * midRigX
        if ((-1 < inter3) and (inter3 <= radRight)):
            if ((radRight & 0xffffff00) == 0):
                radRight = 0x100

            inter5 = (inter3 * 0x40) // (radRight >> 8)
            inter6X = someX - (inter5 * midRigX >> 0xe)
            inter6Y = someY - (inter5 * midRigY >> 0xe)
            inter6Z = someZ - (inter5 * midRigZ >> 0xe)
            radInter6 = inter6Z * inter6Z + inter6Y * inter6Y + inter6X * inter6X
            cenZ = (dist // 0x1f) * (dist // 0x1f)
            #if (sborrow4(radInter6,cenZ * 2) != radInter6 + cenZ * -2 < 0):
            if (radInter6 < (cenZ * 2)):
                return True

        inter4 = someZ * midLefZ + someY * midLefY + someX * midLefX
        radLeft = midLefZ * midLefZ + midLefY * midLefY + midLefX * midLefX
        if ((-1 < inter4) and (inter4 <= radLeft)):
            if ((radLeft & 0xffffff00) == 0):
                radLeft = 0x100

            inter7 = (inter4 * 0x40) // (radLeft >> 8)
            inter8X = someX - (inter7 * midLefX >> 0xe)
            inter8Y = someY - (inter7 * midLefY >> 0xe)
            inter8Z = someZ - (inter7 * midLefZ >> 0xe)
            inter9 = inter8Z * inter8Z + inter8Y * inter8Y + inter8X * inter8X
            inter10 = (dist // 0x1f) * (dist // 0x1f)
            #if (sborrow4(inter9 < inter10 * 2) != inter9 + inter10 * -2 < 0):
            if (inter9 < (inter10 * 2)):
                return True

        cenZ = midLefZ - midRigZ
        centY = midLefY - midRigY
        centX = midLefX - midRigX
        someRightZ = someZ - midRigZ
        someRightY = someY - midRigY
        someRightX = someX - midRigX
        radSomeRight = someRightY * centY + someRightX * centX + someRightZ * cenZ
        radCent = centX * centX + centY * centY + cenZ * cenZ
        if ((-1 < radSomeRight) and (radSomeRight <= radCent)):
            if ((radCent & 0xffffff00) == 0):
                radCent = 0x100

            iVar1 = (radSomeRight * 0x40) // (radCent >> 8)
            cenZ = (someZ - (iVar1 * cenZ >> 0xe)) - midRigZ
            sinterY = (someY - (iVar1 * centY >> 0xe)) - midRigY
            sinterX = (someX - (iVar1 * centX >> 0xe)) - midRigX
            radSinter = sinterX * sinterX + sinterY * sinterY + cenZ * cenZ
            cenZ = (dist // 0x1f) * (dist // 0x1f)
            #if ((sborrow4(radSinter, cenZ * 2) != (radSinter + cenZ * -2)) < 0):
            if (radSinter < (cenZ * 2)):
                return True

        distSquared = (dist // 0x1f) * (dist // 0x1f)
        cenZmul2 = distSquared * 2
        radSome = someZ * someZ + someY * someY + someX * someX

        #if (((1 if sborrow4(radSome,cenZmul2) == radSome else 0) + distSquared * -2) < 0):
        if (radSome >= cenZmul2):
            cenZ = (someY - midLefY) * (someY - midLefY) + (someZ - midLefZ) * (someZ - midLefZ) + (someX - midLefX) * (someX - midLefX)
            #if (((1 if sborrow4(cenZ,cenZmul2) == cenZ else 0) + distSquared * -2) < 0):
            if (cenZ >= cenZmul2):
                cenZ = someRightY * someRightY + someRightX * someRightX + someRightZ * someRightZ
                # only place false can be returned
                #return (sborrow4(cenZ,cenZmul2) != (cenZ + distSquared * -2)) < 0
                return (cenZ < cenZmul2)

        return True


    # function actually starts here
    midInter1 = midLefY
    midInter2 = midRigY
    inter1 = 0
    inter2 = 0

    absScalarX = abs(scalarX)
    absScalarY = abs(scalarY)
    absScalarZ = abs(scalarZ)

    if ((absScalarZ <= absScalarY) and absScalarX <= absScalarY):
        if (scalarY < 0):
            if (((-1 < someZ * midLefX - someX * midLefZ) and
                 (-1 < (someX - midRigX) * midRigZ - (someZ - midRigZ) * midRigX)) and
                 (-1 < (someX - midLefX) * (midLefZ - midRigZ) + (someZ - midLefZ) * (midRigX - midLefX))):
                return True
        elif (((-1 < (someX - midLefX) * midLefZ - (someZ - midLefZ) * midLefX) and
               (-1 < someZ * midRigX - someX * midRigZ)) and
               (-1 < (midRigZ - midLefZ) * (someX - midRigX) + (someZ - midRigZ) * (midLefX - midRigX))):
          return True
        else:
            return _lab_00480dbe()


    if ((absScalarZ < absScalarY) or
        (absScalarZ < absScalarX)):
        if (-1 < scalarX):
            if (((-1 < (someZ - midLefZ) * midLefY - (someY - midLefY) * midLefZ) and
                 (-1 < someY * midRigZ - someZ * midRigY)) and
                 (-1 < (someZ - midRigZ) * (midRigY - midLefY) + (someY - midRigY) * (midLefZ - midRigZ))):
                return True
            else:
                return _lab_00480dbe()

        if ((someY * midLefZ - someZ * midLefY < 0) or
            ((someZ - midRigZ) * midRigY - (someY - midRigY) * midRigZ < 0)):
            return _lab_00480dbe()

        inter1 = (someY - midLefY) * (midRigZ - midLefZ)
        inter2 = someZ - midLefZ

    elif (scalarZ < 0):
        if (((someX - midLefX) * midLefY - (someY - midLefY) * midLefX < 0) or (someY * midRigX - someX * midRigY < 0)):
            return _lab_00480dbe()
        inter1 = (midRigY - midLefY) * (someX - midRigX)
        inter2 = someY - midRigY
        midInter1 = midLefX
        midInter2 = midRigX

    else:
        if ((someY * midLefX - someX * midLefY < 0) or
            ((someX - midRigX) * midRigY - (someY - midRigY) * midRigX < 0)):
            return _lab_00480dbe()
        inter1 = (someY - midLefY) * (midRigX - midLefX)
        inter2 = someX - midLefX

    if (-1 < inter1 + inter2 * (midInter1 - midInter2)):
        return True



if __name__ == "__main__":
    someZ = 1
    someY = 1
    someX = 1
    midLefZ = 1
    midLefY = 1
    midLefX = 1
    midRigZ = 1
    midRigY = 1
    midRigX = 1
    scalarX = 1
    scalarY = 1
    scalarZ = 1
    dist = 1

    print(isInSomeRange(someZ,
                        someY,
                        someX,
                        midLefZ,
                        midLefY,
                        midLefX,
                        midRigZ,
                        midRigY,
                        midRigX,
                        scalarZ,
                        scalarY,
                        scalarX,
                        dist))