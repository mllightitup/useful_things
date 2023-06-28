# Modpack optimization
This guide describes how to improve performance in the game by changing Java arguments and adding optimization mods.
It is worth noting that everything described below can cause various problems from harmless visual bugs to crashes and in rare cases corrupted world files. 

The guide will not tell you why or what each argument affects. If you want a detailed explanation of everything, see **SOURCES**!

_**So before you use this guide, make a backup copy of your world!**_

This guide will be useful to those who use such launchers as: _**MultiMC**_, _**PolyMC**_, _**Prism**_!
# Selecting Java arguments
Arguments can be divided into several parts: Client G1GC, Server G1GC, Large Pages, GraalVM Arguments. They can be applied individually, but we recommend using them all at once.
You can copy the full line of arguments in the **Full Arguments**

Next we will try to provide all possible information, but in most cases you should just choose **Java 17**
## Client G1GC
```
-XX:+UseG1GC -XX:MaxGCPauseMillis=37 -XX:+PerfDisableSharedMem -XX:G1HeapRegionSize=16M -XX:G1NewSizePercent=23 -XX:G1ReservePercent=20 -XX:SurvivorRatio=32 -XX:G1MixedGCCountTarget=3 -XX:G1HeapWastePercent=20 -XX:InitiatingHeapOccupancyPercent=10 -XX:G1RSetUpdatingPauseTimePercent=0 -XX:MaxTenuringThreshold=1 -XX:G1SATBBufferEnqueueingThresholdPercent=30 -XX:G1ConcMarkStepDurationMillis=5.0 -XX:G1ConcRSHotCardLimit=16 -XX:G1ConcRefinementServiceIntervalMillis=150 -XX:GCTimeRatio=99
```

## Server G1GC
If you are going to use the G1GC server arguments you need to remove the client arguments
```
-XX:+UseG1GC -XX:MaxGCPauseMillis=130 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=28 -XX:G1HeapRegionSize=16M -XX:G1ReservePercent=20 -XX:G1MixedGCCountTarget=3 -XX:InitiatingHeapOccupancyPercent=10 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=0 -XX:SurvivorRatio=32 -XX:MaxTenuringThreshold=1 -XX:G1SATBBufferEnqueueingThresholdPercent=30 -XX:G1ConcMarkStepDurationMillis=5 -XX:G1ConcRSHotCardLimit=16 -XX:G1ConcRefinementServiceIntervalMillis=150
```

## Large Pages
**NOTE: Large Pages requires admin privledges on Windows**

On Windows, you must run java, and your launcher, as an administrator. 

That means checking the "run as administrator" compatibility checkbox for javaw.exe, java.exe and your launcher.exe, otherwise Large Pages will silently fail.
Tutorials for enabling it:
* [Windows 10 Pro](https://www.chaoticafractals.com/manual/getting-started/enabling-large-page-support-windows)
* [Windows 10 Home](https://awesomeprojectsxyz.blogspot.com/2017/11/windows-10-home-how-to-enable-lock.html?m=1)
* [Linux](https://kstefanj.github.io/2021/05/19/large-pages-and-java.html)
```
-XX:+UseLargePages -XX:LargePageSizeInBytes=2m
```

## GraalVM Enterprise Edition
### Java 17 & Java 11
<details>
  <summary>Download Links</summary>
Java 17 Links
  
- [Windows AMD64 (64-bit)](https://oca.opensource.oracle.com/gds/GRAALVM_EE_JAVA17_22_3_1/graalvm-ee-java17-windows-amd64-22.3.1.zip)
- [Linux AMD64 (64-bit)](https://oca.opensource.oracle.com/gds/GRAALVM_EE_JAVA17_22_3_1/graalvm-ee-java17-linux-amd64-22.3.1.tar.gz)
- [Linux AARCH64 (ARM 64-bit)](https://oca.opensource.oracle.com/gds/GRAALVM_EE_JAVA17_22_3_1/graalvm-ee-java17-linux-aarch64-22.3.1.tar.gz)
- [Mac AMD64 (64-bit)](https://oca.opensource.oracle.com/gds/GRAALVM_EE_JAVA17_22_3_1/graalvm-ee-java17-darwin-amd64-22.3.1.tar.gz)

Java 11 Links

* [Windows AMD64 (64-bit)](https://oca.opensource.oracle.com/gds/GRAALVM_EE_JAVA11_22_3_1/graalvm-ee-java11-windows-amd64-22.3.1.zip)
* [Linux AMD64 (64-bit)](https://oca.opensource.oracle.com/gds/GRAALVM_EE_JAVA11_22_3_1/graalvm-ee-java11-linux-amd64-22.3.1.tar.gz)
* [Linux AARCH64 (ARM 64-bit)](https://oca.opensource.oracle.com/gds/GRAALVM_EE_JAVA11_22_3_1/graalvm-ee-java11-linux-aarch64-22.3.1.tar.gz)
* [Mac AMD64 (64-bit)](https://oca.opensource.oracle.com/gds/GRAALVM_EE_JAVA11_22_3_1/graalvm-ee-java11-darwin-amd64-22.3.1.tar.gz)
</details>

#### Arguments
The arguments are the same for Java 17 and 11
```
-XX:+UnlockExperimentalVMOptions -XX:+UnlockDiagnosticVMOptions -XX:+AlwaysActAsServerClassMachine -XX:+AlwaysPreTouch -XX:+DisableExplicitGC -XX:+UseNUMA -XX:AllocatePrefetchStyle=3 -XX:NmethodSweepActivity=1 -XX:ReservedCodeCacheSize=400M -XX:NonNMethodCodeHeapSize=12M -XX:ProfiledCodeHeapSize=194M -XX:NonProfiledCodeHeapSize=194M -XX:-DontCompileHugeMethods -XX:+PerfDisableSharedMem -XX:+UseFastUnorderedTimeStamps -XX:+UseCriticalJavaThreadPriority -XX:+EagerJVMCI -Dgraal.TuneInlinerExploration=1 -Dgraal.CompilerConfiguration=enterprise
```
### Java 8
<details>
  <summary>Download Links</summary>
  
* [Windows AMD64 (64-bit)](https://oca.opensource.oracle.com/gds/GRAALVM_EE_JAVA8_21_3_5/graalvm-ee-java8-windows-amd64-21.3.5.zip)
* [Linux AMD64 (64-bit)](https://oca.opensource.oracle.com/gds/GRAALVM_EE_JAVA8_21_3_5/graalvm-ee-java8-linux-amd64-21.3.5.tar.gz)
* [Mac AMD64 (64-bit)](https://oca.opensource.oracle.com/gds/GRAALVM_EE_JAVA8_21_3_5/graalvm-ee-java8-darwin-amd64-21.3.5.tar.gz)

</details>

#### Arguments
```
-XX:+UnlockExperimentalVMOptions -XX:+UnlockDiagnosticVMOptions -XX:+AlwaysActAsServerClassMachine -XX:+ParallelRefProcEnabled -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:+PerfDisableSharedMem -XX:+AggressiveOpts -XX:+UseFastAccessorMethods -XX:MaxInlineLevel=15 -XX:MaxVectorSize=32 -XX:+UseCompressedOops -XX:ThreadPriorityPolicy=1 -XX:+UseNUMA -XX:+UseDynamicNumberOfGCThreads -XX:NmethodSweepActivity=1 -XX:ReservedCodeCacheSize=350M -XX:-DontCompileHugeMethods -XX:MaxNodeLimit=240000 -XX:NodeLimitFudgeFactor=8000 -XX:+UseFPUForSpilling -Dgraal.CompilerConfiguration=community
```
# Installing new Java
* Download the correct version of Java for your OS from **GraalVM Enterprise Edition**

* Unzip the archive to any location you like.

* For example I will create a folder **JDK** in the root of drive **C** and put there previously unpacked folder<br> `graalvm-ee-java17-22.3.2`

* So you should have the path to the `java.exe` and `javaw.exe` files as: <br>`C:\JDK\graalvm-ee-java17-22.3.2\bin`

# Using arguments

* Right-click on the modpack you want to optimize and press **Edit** You will get to the settings menu of your modpack

![image](https://github.com/mllightitup/useful_things/assets/43480503/41894862-692c-4d4b-8155-3d6ca3930609)

* Next, click on the **Settings** tab and you will get to the Java settings menu for your modpack

![image](https://github.com/mllightitup/useful_things/assets/43480503/8b4a9b30-563e-4b12-b3ad-a2db31a1fea9)

* Activate the **Java installation** checkbox and click the **Browse...** button.
* In the explorer that opens, specify the path to the **javaw.exe** file

**Example: `C:\JDK\graalvm-ee-java17-22.3.2\bin\javaw.exe`**

* Activate the checkbox **Skip Java compatibility checks**

![image](https://github.com/mllightitup/useful_things/assets/43480503/05c3668a-eb0b-40ff-9a22-2e2de9037040)

* Activate the **Memory** checkbox and specify the same minimum and maximum memory allocations. Between 6 and 8 gigabytes should be enough.

![image](https://github.com/mllightitup/useful_things/assets/43480503/c5f73851-0787-4c42-90fa-7ad6aa561055)

* Activate the **Java arguments** checkbox and insert the previously selected arguments into the empty text field

![image](https://github.com/mllightitup/useful_things/assets/43480503/60bb066f-5df8-4878-b8cf-2bc58ec5fada)

The arguments is over! If that solved your problem, you don't need to read any further. Otherwise, read **Optimization mods**

# Optimization mods
To begin with, it should be noted that the following will be recommended mods, which together with the optimization can bring both visual bugs and damage the world or crashes!

**Be sure to back up your world like we asked you before!**

Let's start with the ones that are least likely to hurt you:

* [Starlight](https://modrinth.com/mod/starlight-forge) - Reduces or eliminates freezes when passing the chunk borders, also speeds up the generation of the world, which in some cases may cause increased load on the CPU
* [EntityCulling](https://modrinth.com/mod/entityculling/versions?l=forge) - Stops drawing entities outside your field of view. Useful when using big Mob Farms
* [Rubidium](https://modrinth.com/mod/rubidium) - Sodium port for Forge. Optimizes the game in a large number of areas and therefore can cause graphical artifacts with some mods
* [Rubidium Extras](https://www.curseforge.com/minecraft/mc-mods/magnesium-extras) - Improve performance in modpacks drastically by not rendering far away tile entities.

In the video settings, go to the Extras tab and set these two values to the minimum:

Also, this mod by default for some reason includes the "True darkness" effect. You can turn it off in the same tab.

![image](https://github.com/mllightitup/useful_things/assets/43480503/be0bd84d-ebac-4063-858c-94504afecc09)

Next, we'll look at modifications that can cause harm:
* [Canary](https://www.curseforge.com/minecraft/mc-mods/magnesium-extras) - Lithium port for Forge. Optimizes the behavior of mobs, physics, block ticking. Potentially can conflict with other mods that affect the behavior of mobs and blocks
* [ModernFix](https://modrinth.com/mod/modernfix/versions?l=forge) - improves launch times, world load times, memory usage and more. By default, the mod should not do any damage, but it gives you the opportunity to apply dangerous tweeks. If you want to know more, see the [ModernFix Wiki](https://github.com/embeddedt/ModernFix/wiki/Summary-of-Patches)

Listed below are mods whose influence has not been confirmed:
* [Alternate Current](https://modrinth.com/mod/alternate-current/versions?l=forge)
* [Memory Leak Fix](https://modrinth.com/mod/memoryleakfix/versions?l=forge)
* [Pluto](https://modrinth.com/mod/pluto)
* [ImmeduatelyFastReforged](https://modrinth.com/mod/immediatelyfast-reforged)
* [Saturn](https://modrinth.com/mod/saturn)
* [EnhancedBlockEntitites Reforged](https://www.curseforge.com/minecraft/mc-mods/enhanced-block-entities-reforged-unofficial)

# Sources
* [Java arguments explanation](https://github.com/brucethemoose/Minecraft-Performance-Flags-Benchmarks)
* [Performance mods](https://github.com/TheUsefulLists/UsefulMods)
