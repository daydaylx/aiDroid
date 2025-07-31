# Kivy/KivyMD specific rules
-keep class org.kivy.** { *; }
-keep class org.kivymd.** { *; }
-dontwarn org.kivy.**
-dontwarn org.kivymd.**

# Python-for-Android
-keep class org.renpy.android.** { *; }
-keep class org.kivy.android.** { *; }

# Keep native methods
-keepclasseswithmembernames class * {
    native <methods>;
}

# Keep Samsung specific classes if needed
-keep class com.samsung.** { *; }

# General Android optimizations
-optimizationpasses 5
-dontusemixedcaseclassnames
-dontskipnonpubliclibraryclasses
-verbose
