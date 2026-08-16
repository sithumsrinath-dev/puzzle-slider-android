package org.senu.puzzleslider;

import android.app.Activity;
import androidx.annotation.NonNull;
import com.google.android.gms.ads.AdRequest;
import com.google.android.gms.ads.LoadAdError;
import com.google.android.gms.ads.MobileAds;
import com.google.android.gms.ads.rewarded.RewardedAd;
import com.google.android.gms.ads.rewarded.RewardedAdLoadCallback;
import com.google.android.gms.ads.OnUserEarnedRewardListener;
import com.google.android.gms.ads.RewardItem;
import com.google.android.gms.ads.AdError;
import com.google.android.gms.ads.FullScreenContentCallback;

public class AdMobHelper {
    private static Activity activityContext;
    private static RewardedAd mRewardedAd;
    private static volatile boolean isLoaded = false;
    private static volatile boolean rewardEarned = false;
    private static volatile boolean adFailed = false;
    private static volatile boolean isInitialized = false;

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
                MobileAds.initialize(activityContext, initializationStatus -> {
                    isInitialized = true;
                    loadRewardedAd();
                });
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
