// WARNING: Globals starting with '_' overlap smaller symbols at the same address
// modifies level zone?

void occasionalySetsLevelZone??(void)

{
 int iVar1;
 short sVar2;
 int smallX;
 int someDist?;
 uint xorZ;
 uint uVar3;
 int smallZ;
 int idk;
 LevelZoneInfo_t *buzzZoneInfo;
 int smallY;
 int *ptrToSomething;
 short camSom0?;
 short camSom2?;
 short camsom4?;
 byte zoneId;

 buzzZoneInfo = (LevelZoneInfo_t *)(&gLevelZoneInfoBaseAddr? + gBuzzZone * 0x20);
 zoneId = buzzZoneInfo->zoneId;
 camsom4? = gCamSom4?;
 camSom2? = gCamSom2?;
 camSom0? = gCamSom0?;
 do {
   if (zoneId == 0xff) {
     gCamSom0? = camSom0?;
     gCamSom2? = camSom2?;
     gCamSom4? = camsom4?;
     return;
   }
                  // This gets run for Al's Space Level due to the flag
   if ((buzzZoneInfo->zoneType??? != '\x0f') || (gSomeFlagLevelRelated? == 0)) {
     smallZ = gBuzzZ? >> 7;
     ptrToSomething = (int *)(&gZoneIndexedPtrTbl?)[zoneId];
     xorZ = smallZ - *(short *)(ptrToSomething + 1) >> 0x1f;
     smallX = gBuzzX? >> 7;
     smallY = gBuzzY? >> 7;
     if ((((int)((smallZ - *(short *)(ptrToSomething + 1) ^ xorZ) - xorZ) < 0x4000) &&
         ((xorZ = smallY - *(short *)((int)ptrToSomething + 6), uVar3 = (int)xorZ >> 0x1f,
         (int)((xorZ ^ uVar3) - uVar3) < 0x4000 &&
         (xorZ = smallX - *(short *)(ptrToSomething + 2) >> 0x1f,
         (int)((smallX - *(short *)(ptrToSomething + 2) ^ xorZ) - xorZ) < 0x4000)))) ||
        ((xorZ = smallZ - *(short *)(ptrToSomething + 7) >> 0x1f,
         (int)((smallZ - *(short *)(ptrToSomething + 7) ^ xorZ) - xorZ) < 0x4000 &&
         ((xorZ = smallY - *(short *)((int)ptrToSomething + 0x1e), uVar3 = (int)xorZ >> 0x1f,
         (int)((xorZ ^ uVar3) - uVar3) < 0x4000 &&
         (xorZ = smallX - *(short *)(ptrToSomething + 8) >> 0x1f,
         (int)((smallX - *(short *)(ptrToSomething + 8) ^ xorZ) - xorZ) < 0x4000)))))) {
       gCamSom0? = *(short *)((int)ptrToSomething + 10);
       _DAT_005551e0 = (int)gCamSom0?;
       gCamSom2? = *(short *)((&gZoneIndexedPtrTbl?)[buzzZoneInfo->zoneId] + 0xc);
       DAT_005551e4 = (int)gCamSom2?;
       gCamSom4? = *(short *)((&gZoneIndexedPtrTbl?)[buzzZoneInfo->zoneId] + 0xe);
       DAT_005551e8 = (int)gCamSom4?;
       iVar1 = (&gZoneIndexedPtrTbl?)[buzzZoneInfo->zoneId];
       someDist? = (smallX - *(short *)(iVar1 + 8)) * DAT_005551e8 + (smallY - *(short *)(iVar1 + 6)) * DAT_005551e4  +
                  (smallZ - *(short *)(iVar1 + 4)) * _DAT_005551e0;
       if ((someDist? < 0) &&
         (smallX = ((gOldBuzzX >> 7) - (int)*(short *)(iVar1 + 8)) * DAT_005551e8 +
                  ((gOldBuzzY? >> 7) - (int)*(short *)(iVar1 + 6)) * DAT_005551e4 +
                  ((gOldBuzzZ? >> 7) - (int)*(short *)(iVar1 + 4)) * _DAT_005551e0, -1 < smallX)) {
         idk = smallX - someDist?;
         DAT_00555368 = (((gBuzzZ? - gOldBuzzZ?) * smallX) / idk + gOldBuzzZ? >> 7) -
                      (int)*(short *)((&gZoneIndexedPtrTbl?)[buzzZoneInfo->zoneId] + 4);
         DAT_0055536c = (((gBuzzY? - gOldBuzzY?) * smallX) / idk + gOldBuzzY? >> 7) -
                      (int)*(short *)((&gZoneIndexedPtrTbl?)[buzzZoneInfo->zoneId] + 6);
         DAT_00555370 = (((gBuzzX? - gOldBuzzX) * smallX) / idk + gOldBuzzX >> 7) -
                      (int)*(short *)((&gZoneIndexedPtrTbl?)[buzzZoneInfo->zoneId] + 8);
         smallX = (&gZoneIndexedPtrTbl?)[buzzZoneInfo->zoneId];
         camsom4? = FUN_00480ae0(DAT_00555368,DAT_0055536c,DAT_00555370,
                              (int)*(short *)(smallX + 0x10) - (int)*(short *)(smallX + 4),
                              (int)*(short *)(smallX + 0x12) - (int)*(short *)(smallX + 6),
                              (int)*(short *)(smallX + 0x14) - (int)*(short *)(smallX + 8),
                              (int)*(short *)(smallX + 0x1c) - (int)*(short *)(smallX + 4),
                              (int)*(short *)(smallX + 0x1e) - (int)*(short *)(smallX + 6),
                              (int)*(short *)(smallX + 0x20) - (int)*(short *)(smallX + 8),&gCamSom0?,400);
         if (camsom4? == 0) {
          smallX = (&gZoneIndexedPtrTbl?)[buzzZoneInfo->zoneId];
          sVar2 = FUN_00480ae0(DAT_00555368,DAT_0055536c,DAT_00555370,
                             (int)*(short *)(smallX + 0x1c) - (int)*(short *)(smallX + 4),
                             (int)*(short *)(smallX + 0x1e) - (int)*(short *)(smallX + 6),
                             (int)*(short *)(smallX + 0x20) - (int)*(short *)(smallX + 8),
                             (int)*(short *)(smallX + 0x28) - (int)*(short *)(smallX + 4),
                             (int)*(short *)(smallX + 0x2a) - (int)*(short *)(smallX + 6),
                             (int)*(short *)(smallX + 0x2c) - (int)*(short *)(smallX + 8),&gCamSom0?,400);
          camSom0? = gCamSom0?;
          camSom2? = gCamSom2?;
          camsom4? = gCamSom4?;
          if (sVar2 == 0) goto LAB_0044023f;
         }
         gBuzzZone = (uint)(byte)buzzZoneInfo->zoneType???;
         camSom0? = gCamSom0?;
         camSom2? = gCamSom2?;
         camsom4? = gCamSom4?;
       }
     }
   }
LAB_0044023f:
   gCamSom4? = camsom4?;
   gCamSom2? = camSom2?;
   gCamSom0? = camSom0?;
   zoneId = buzzZoneInfo->field_0x2;
   buzzZoneInfo = (LevelZoneInfo_t *)&buzzZoneInfo->field_0x2;
   camsom4? = gCamSom4?;
   camSom2? = gCamSom2?;
   camSom0? = gCamSom0?;
 } while( true );
}
