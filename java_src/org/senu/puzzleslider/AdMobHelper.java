### 📋 පියවර 02 - ක්‍රියාත්මක කිරීමේ වාර්තාව (Execution Notes)

**මෙම පියවරෙහි අරමුණ:**
Python/PyJNIus හරහා dynamic ලෙස Android Event Listeners subclass කිරීමේදී සිදුවන Memory Corruption සහ Threading Crashing (Fatal Signals) වැළැක්වීම සඳහා static Native Java Class එකක් නිර්මාණය කිරීම.

**සිදුකරන ලද තාක්ෂණික වෙනස්කම්:**

1. **`org.senu.puzzleslider.AdMobHelper` Class එක සෑදීම:** AdMob SDK initialize කිරීම, Ad එක load කිරීම සහ පෙන්වීම (Show) සඳහා static ක්‍රමවේද (Static Methods) සැකසීම.
2. **UI Thread Isolation (`runOnUiThread`):** Android UI Thread එකට අදාළ Google AdMob Calls සියල්ලම `activityContext.runOnUiThread` මගින් isolated කොට ආරක්ෂිතව ධාවනය වන සේ සකස් කිරීම.
3. **Thread-Safe Volatile Flags:** `volatile boolean` variables (`isLoaded`, `rewardEarned`, `adFailed`) භාවිතයෙන් PyJNIus / Kivy side එකෙහි Polling loop එකට (Kivy Thread) direct memory read access ලබා දීම.

---

### 🛠️ Native Java File එක නිර්මාණය කිරීමේ විධානය (Full Code Deliverable)

ඔබගේ Project Directory එක තුළ `java_src/org/senu/puzzleslider/AdMobHelper.java` ලෙස පහත ගොනුව සම්පූර්ණයෙන්ම ස්ථාපනය කරන්න.

```java
package org.senu.puzzleslider;

import android.app.Activity;
import androidx.annotation.NonNull;
import com.google.android.gms.ads.AdRequest;
import com.google.android.gms.ads.LoadAdError;
import com.google.android.gms.ads.MobileAds;
import com.google.android.gms.ads.rewarded.RewardedAd;
import com.google.android.gms.ads.rewarded.RewardedAdLoadCallback;
import com.google.android.gms.ads.OnUserEarnedRewardListener;
import com.google.android.gms.ads.rewarded.RewardItem;
import com.google.android.gms.ads.AdError;
import com.google.android.gms.ads.FullScreenContentCallback;

public class AdMobHelper {
    private static Activity activityContext;
    private static RewardedAd mRewardedAd;
    private static volatile boolean isLoaded = false;
    private static volatile boolean rewardEarned = false;
    private static volatile boolean adFailed = false;

    // Google AdMob Rewarded Ad Unit ID (Production Unit ID හෝ Test Unit ID භාවිත කරන්න)
    private static final String AD_UNIT_ID = "ca-app-pub-3940256099942544/5224354917";

    /**
     * MobileAds SDK Initialization
     */
    public static void init(final Activity activity) {
        activityContext = activity;
        if (activityContext == null) return;

        activityContext.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                MobileAds.initialize(activityContext, initializationStatus -> {});
            }
        });
    }

    /**
     * Rewarded Ad එක Async ලෙස Load කිරීම (UI Thread Isolated)
     */
    public static void loadRewardedAd() {
        if (activityContext == null) return;

        activityContext.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                isLoaded = false;
                adFailed = false;
                AdRequest adRequest = new AdRequest.Builder().build();

                RewardedAd.load(activityContext, AD_UNIT_ID, adRequest, new RewardedAdLoadCallback() {
                    @Override
                    public void onAdFailedToLoad(@NonNull LoadAdError loadAdError) {
                        mRewardedAd = null;
                        isLoaded = false;
                        adFailed = true;
                    }

                    @Override
                    public void onAdLoaded(@NonNull RewardedAd rewardedAd) {
                        mRewardedAd = rewardedAd;
                        isLoaded = true;
                        adFailed = false;

                        mRewardedAd.setFullScreenContentCallback(new FullScreenContentCallback() {
                            @Override
                            public void onAdDismissedFullScreenContent() {
                                mRewardedAd = null;
                                isLoaded = false;
                            }

                            @Override
                            public void onAdFailedToShowFullScreenContent(AdError adError) {
                                mRewardedAd = null;
                                isLoaded = false;
                                adFailed = true;
                            }
                        });
                    }
                });
            }
        });
    }

    /**
     * Loaded Ad එක Display කිරීම (UI Thread Isolated)
     */
    public static void showRewardedAd() {
        if (activityContext == null || mRewardedAd == null) return;

        activityContext.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                rewardEarned = false;
                mRewardedAd.show(activityContext, new OnUserEarnedRewardListener() {
                    @Override
                    public void onUserEarnedReward(@NonNull RewardItem rewardItem) {
                        rewardEarned = true;
                    }
                });
            }
        });
    }

    /**
     * Ad එක Load වී ඇත්දැයි Kivy Polling Loop එකට පරීක්ෂා කිරීම සඳහා Methods
     */
    public static boolean isAdLoaded() {
        return isLoaded;
    }

    public static boolean hasEarnedReward() {
        return rewardEarned;
    }

    public static boolean isAdFailedToLoad() {
        return adFailed;
    }

    public static void resetRewardState() {
        rewardEarned = false;
        adFailed = false;
    }
}

```
