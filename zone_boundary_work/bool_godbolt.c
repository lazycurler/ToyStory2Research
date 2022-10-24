#include <cstdint>
#include <cstdio>
#include <iostream>

// for godbolt

struct vec3short {
    short z;
    short y;
    short x;
};

bool __cdecl
isInSomeRange(int someZ,
              int someY,
              int someX,
              int midLefZ,
              int midLefY,
              int midLefX,
              int midRigZ,
              int midRigY,
              int midRigX,
              vec3short *scalar,
              int dist)
{
  int absScalarZ;
  int inter3;
  int inter5;
  int inter6Z;
  int inter4;
  int inter7;
  int inter8Y;
  int inter8Z;
  int someRightZ;
  int someRightY;
  int radSomeRight;
  int iVar1;
  int distSquared;
  int cenZmul2;
  int absScalarY;
  int local_ECX_821;
  int inter6X;
  int inter6Y;
  int someSquareDist;
  int radLeft;
  int inter9;
  int cenZ;
  int centX;
  int radCent;
  int sinterY;
  int radSome;
  uint32_t signScalarY;
  uint32_t signScalarZ;
  uint32_t signScalarX;
  uint32_t signScalarX1;
  int inter1;
  int radInter6;
  int inter10;
  int centY;
  int sinterX;
  int radSinter;
  int inter2;
  int inter8X;
  int someRightX;
  int midInter1;
  int midInter2;
  short scalarY;
  short scalarZ;

  scalarY = scalar->y;
  scalarZ = scalar->z;
  signScalarY = (int)scalarY >> 0x1f;
  absScalarY = ((int)scalarY ^ signScalarY) - signScalarY;
  signScalarZ = (int)scalarZ >> 0x1f;
  absScalarZ = ((int)scalarZ ^ signScalarZ) - signScalarZ;
  if ((absScalarZ <= absScalarY) &&
     (signScalarX = (int)scalar->x >> 0x1f, (int)(((int)scalar->x ^ signScalarX) - signScalarX) <= absScalarY)) {
    if (scalarY < 0) {
      if (((-1 < someZ * midLefX - someX * midLefZ) && (-1 < (someX - midRigX) * midRigZ - (someZ - midRigZ) * midRigX)) &&
         (-1 < (someX - midLefX) * (midLefZ - midRigZ) + (someZ - midLefZ) * (midRigX - midLefX))) {
             std::cout << "a" << std::endl;
        return true;
      }
    }
    else if (((-1 < (someX - midLefX) * midLefZ - (someZ - midLefZ) * midLefX) && (-1 < someZ * midRigX - someX * midRigZ)) &&
           (-1 < (midRigZ - midLefZ) * (someX - midRigX) + (someZ - midRigZ) * (midLefX - midRigX))) {
             std::cout << "b" << std::endl;
      return true;
    }
    goto LAB_00480dbe;
  }
  midInter1 = midLefY;
  midInter2 = midRigY;
  if ((absScalarZ < absScalarY) ||
     (signScalarX1 = (int)scalar->x >> 0x1f, absScalarZ < (int)(((int)scalar->x ^ signScalarX1) - signScalarX1))) {
    if (-1 < scalar->x) {
      if (((-1 < (someZ - midLefZ) * midLefY - (someY - midLefY) * midLefZ) && (-1 < someY * midRigZ - someZ * midRigY)) &&
         (-1 < (someZ - midRigZ) * (midRigY - midLefY) + (someY - midRigY) * (midLefZ - midRigZ))) {
             std::cout << "c" << std::endl;
        return true;
      }
      goto LAB_00480dbe;
    }
    if ((someY * midLefZ - someZ * midLefY < 0) || ((someZ - midRigZ) * midRigY - (someY - midRigY) * midRigZ < 0))
    goto LAB_00480dbe;
    inter1 = (someY - midLefY) * (midRigZ - midLefZ);
    inter2 = someZ - midLefZ;
  }
  else if (scalarZ < 0) {
    if (((someX - midLefX) * midLefY - (someY - midLefY) * midLefX < 0) || (someY * midRigX - someX * midRigY < 0))
    goto LAB_00480dbe;
    inter1 = (midRigY - midLefY) * (someX - midRigX);
    inter2 = someY - midRigY;
    midInter1 = midLefX;
    midInter2 = midRigX;
  }
  else {
    if ((someY * midLefX - someX * midLefY < 0) || ((someX - midRigX) * midRigY - (someY - midRigY) * midRigX < 0))
    goto LAB_00480dbe;
    inter1 = (someY - midLefY) * (midRigX - midLefX);
    inter2 = someX - midLefX;
  }
  if (-1 < inter1 + inter2 * (midInter1 - midInter2)) {
             std::cout << "d" << std::endl;
    return true;
  }
LAB_00480dbe:
  inter3 = someZ * midRigZ + someY * midRigY + someX * midRigX;
  local_ECX_821 = midRigZ * midRigZ + midRigY * midRigY + midRigX * midRigX;
  if ((-1 < inter3) && (inter3 <= local_ECX_821)) {
    if ((local_ECX_821 & 0xffffff00U) == 0) {
      local_ECX_821 = 0x100;
    }
    inter5 = (inter3 * 0x40) / (local_ECX_821 >> 8);
    inter6X = someX - (inter5 * midRigX >> 0xe);
    inter6Y = someY - (inter5 * midRigY >> 0xe);
    inter6Z = someZ - (inter5 * midRigZ >> 0xe);
    radInter6 = inter6Z * inter6Z + inter6Y * inter6Y + inter6X * inter6X;
    someSquareDist = (dist / 0x1f) * (dist / 0x1f);
    //if (SBORROW4(radInter6,someSquareDist * 2) != radInter6 + someSquareDist * -2 < 0) {
    if (radInter6 < (someSquareDist * 2)) {
             std::cout << "e" << std::endl;
      return true;
    }
  }
  inter4 = someZ * midLefZ + someY * midLefY + someX * midLefX;
  radLeft = midLefZ * midLefZ + midLefY * midLefY + midLefX * midLefX;
  if ((-1 < inter4) && (inter4 <= radLeft)) {
    if ((radLeft & 0xffffff00U) == 0) {
      radLeft = 0x100;
    }
    inter7 = (inter4 * 0x40) / (radLeft >> 8);
    inter8X = someX - (inter7 * midLefX >> 0xe);
    inter8Y = someY - (inter7 * midLefY >> 0xe);
    inter8Z = someZ - (inter7 * midLefZ >> 0xe);
    inter9 = inter8Z * inter8Z + inter8Y * inter8Y + inter8X * inter8X;
    inter10 = (dist / 0x1f) * (dist / 0x1f);
    // if (SBORROW4(inter9,inter10 * 2) != inter9 + inter10 * -2 < 0) {
     if (inter9 < (inter10 * 2)) {
             std::cout << "f" << std::endl;
      return true;
    }
  }
  cenZ = midLefZ - midRigZ;
  centY = midLefY - midRigY;
  centX = midLefX - midRigX;
  someRightZ = someZ - midRigZ;
  someRightY = someY - midRigY;
  someRightX = someX - midRigX;
  radSomeRight = someRightY * centY + someRightX * centX + someRightZ * cenZ;
  radCent = centX * centX + centY * centY + cenZ * cenZ;
  if ((-1 < radSomeRight) && (radSomeRight <= radCent)) {
    if ((radCent & 0xffffff00U) == 0) {
      radCent = 0x100;
    }
    iVar1 = (radSomeRight * 0x40) / (radCent >> 8);
    cenZ = (someZ - (iVar1 * cenZ >> 0xe)) - midRigZ;
    sinterY = (someY - (iVar1 * centY >> 0xe)) - midRigY;
    sinterX = (someX - (iVar1 * centX >> 0xe)) - midRigX;
    radSinter = sinterX * sinterX + sinterY * sinterY + cenZ * cenZ;
    cenZ = (dist / 0x1f) * (dist / 0x1f);
    // if (SBORROW4(radSinter,cenZ * 2) != radSinter + cenZ * -2 < 0) {
    if (radSinter < (cenZ * 2)) {
             std::cout << "g" << std::endl;
      return true;
    }
  }
  distSquared = (dist / 0x1f) * (dist / 0x1f);
  cenZmul2 = distSquared * 2;
  radSome = someZ * someZ + someY * someY + someX * someX;
                   // SBOWRROW4 detects signed overflow treating both operands as int32s
  // if ((SBORROW4(radSome,cenZmul2) == radSome + distSquared * -2 < 0) &&
  if (radSome >= cenZmul2) {
      std::cout << "1" << std::endl;
    cenZ = (someY - midLefY) * (someY - midLefY) + (someZ - midLefZ) * (someZ - midLefZ) + (someX - midLefX) * (someX - midLefX);
        // , SBORROW4(cenZ,cenZmul2) == cenZ + distSquared * -2 < 0)) {
    if (cenZ >= cenZmul2) {
      std::cout << "2" << std::endl;
        cenZ = (someRightY * someRightY + someRightX * someRightX + someRightZ * someRightZ);

        // only place false can be returned
        std::cout << "h" << std::endl;
        // return SBORROW4(cenZ,cenZmul2) != cenZ + distSquared * -2 < 0;
        return (cenZ < cenZmul2);
    }
  }
  std::cout << "i" << std::endl;
  return true;
}




int main()
{
    // 0, 13000000, 0
    // vec3short sVec = { 0, 9490, 0 };
    // return isInSomeRange(1622, 101562, -2371, 0, -1790, 0, 0, -1790, 505, &sVec, 400) ||
    //        isInSomeRange(1622, 101562, -2371, 0, -1790, 505, 0, 0, 505, &sVec, 400);

    // (0, 14000000, 0)
    vec3short sVec = { 0, 9490, 0 };
    return isInSomeRange(1625, 109376, -2373, 0, -1790, 0, 0, -1790, 505, &sVec, 400) ||
           isInSomeRange(1625, 109376, -2373, 0, -1790, 505, 0, 0, 505, &sVec, 400);
}