# Setting up the daily Meditation on an iPhone

This takes about 5 minutes. It uses the built-in **Shortcuts** app, so there's nothing to install. Do it on whichever phone should get the notification.

There are three parts:

1. **The shortcut** fetches today's passage and shows it as a notification.
2. **The automation** runs that shortcut every morning at 10:00.
3. **The home-screen icon** opens the full passage with one tap.

---

## 1. Build the shortcut

1. Open **Shortcuts** and go to the **Shortcuts** tab. Tap **+** (top right).
2. Tap the name at the top and call it **Daily Meditation**.
3. Add these actions in order. Tap **Search Actions** (or the search bar at the bottom), type the action's name, and tap it.

   1. **Current Date**
   2. **Format Date**
      - It should say *Format Current Date*. Tap the arrow (›) to expand it.
      - Set **Date Format** to **Custom**.
      - Set **Format String** to `yyyy-MM-dd` (capital MM).
      - Set **Time Format** to **None**.
   3. **Text**
      - Type `https://dannisteele.github.io/meditations/days/`
      - Then tap **Formatted Date** in the bar above the keyboard to insert it as a blue variable.
      - Then type `.json` straight after it, with no spaces.
      - It should read: `https://dannisteele.github.io/meditations/days/`**`Formatted Date`**`.json`
   4. **Get Contents of URL** (it should pick up *Text* automatically)
   5. **Get Dictionary Value**
      - Set it to *Get* **Value** *for* `notification` *in* **Contents of URL**.
      - For Long's original wording instead of the modern version, type `notification_original` here instead. That's the only change needed.
   6. **If**
      - Set it to *If* **Dictionary Value** **has any value**.
   7. **Show Notification**. Drag it so it sits **inside** the If, between *If* and *Otherwise*.
      - Tap the text field and replace *Hello World!* with the blue **Dictionary Value** variable (tap it in the bar above the keyboard).
      - Tap the arrow (›) and set **Title** to `Meditations`.
   8. Leave *Otherwise* empty. That way, if there's no passage or no internet, nothing happens.

4. Tap **Done**.

**Test it:** tap the shortcut once. A notification with the start of today's passage should appear. The first time, iOS may ask whether *Daily Meditation* can connect to `dannisteele.github.io`. Tap **Always Allow**.

---

## 2. Run it every morning at 10:00

1. In **Shortcuts**, go to the **Automation** tab and tap **+** (or **New Automation**).
2. Choose **Time of Day**.
   - Set the time to **10:00** and choose **Daily**.
   - Choose **Run Immediately** (not *Run After Confirmation*).
   - Turn **Notify When Run** off.
   - Tap **Next**.
3. Choose the **Daily Meditation** shortcut.

That's it. Every day at 10:00 the passage arrives as a notification.

> The date comes from the phone's clock, so on a UK phone the day changes at UK midnight, the same as the website.

---

## 3. Add the page to the home screen

Tapping the notification opens the Shortcuts app, not the full passage. *(To be confirmed on a real phone; see the test checklist below.)* For the full text, add the page as an app icon:

1. Open **Safari** and go to **https://dannisteele.github.io/meditations/**
2. Tap the **Share** button (the square with an arrow), then **Add to Home Screen**.
3. Keep the name **Meditations** and tap **Add**.

The **Meditations** icon now opens today's passage. Use the **Modern / Original** switch at the bottom to change the wording, and it'll be remembered.

> The home-screen icon remembers its own Modern/Original choice separately from Safari, so set it from the icon.

---

## Test checklist (Daniella's phone, before setting up Rach's)

- [ ] (a) Does the 10:00 automation fire on its own, with no "Run?" prompt?
- [ ] (b) What does tapping the notification open?
- [ ] (c) In Airplane Mode, does it stay silent or show an error?
- [ ] (d) Does the notification text look right, short, and end cleanly?
- [ ] Optional: add an **Open URLs** action (`https://dannisteele.github.io/meditations/`) after Show Notification, inside the If. Does opening the page every morning feel helpful or intrusive?

## Good to know

- The passages are scheduled until **8 November 2036**. After that, the shortcut quietly does nothing until the site is rebuilt.
- Every passage (487 in all) appears once before any repeats, then the order reshuffles.
