# "Explained" style

The third toggle on the daily page. Where **Original** is Long's 1862 text and **Modern** is that same text with the archaic English updated, **Explained** says in plain, present-day English *what the passage is getting at and why it matters*. Picture a thoughtful friend who knows Stoicism well and explains it over coffee. Not a lecturer, and not a self-help guru.

## Data shape

`data/explained/book-NN.json` maps each passage id to an object:

```json
{
  "2.1": {
    "summary": "One or two short paragraphs, separated by \n\n.",
    "today": "Optional. Modern-day examples. Leave the key out when examples would be forced."
  }
}
```

## `summary` (always present)

- **40–130 words.** A one-line passage gets two or three sentences. A long passage gets two short paragraphs at most. Never longer than the passage itself unless the passage is under about 40 words.
- Open with the point, not with "In this passage, Marcus…". Lead with the idea, e.g. "Most of what upsets us is our own opinion about events, not the events themselves."
- Explain any Stoic idea the passage relies on in everyday words: the "ruling faculty" is your mind or judgement; "nature" / "the whole" is the way the universe works and our place in it; "indifferent" things are things like money, health and reputation, which aren't good or bad in themselves; "the spirit within" is your inner sense of reason and conscience; "providence or atoms" is "whether the universe is ordered by a purpose or is just chance".
- Briefly identify an obscure name or reference when it matters to the meaning, and only with facts you are sure of (e.g. "Rusticus, the Stoic teacher who introduced Marcus to Epictetus"). If you are unsure, describe the role ("one of his teachers") instead of guessing.
- Be faithful. Don't add ideas Marcus doesn't have, and don't soften hard ones (his calm about death, his indifference to fame). Where he is writing a note to himself, saying so can help ("He's reminding himself…").
- Second person ("you") is fine and often best. Use "Marcus" or "he" for the author.
- British spelling (honour, judgement, realise). Gender-neutral modern wording is fine here; this is our voice, not Long's.
- No headings, bullet points, emoji, quotation of long chunks of the passage, or exclamation marks. No "Ultimately," and no closing moral like "So remember: …".

## `today` (only when it helps)

Include it when the passage gives practical advice, a list of habits, or examples rooted in its time (the Circus factions, quail-fighting, a praetor's games, slaves, the Senate). Skip it for purely metaphysical or cosmological passages, short aphorisms that are already clear, or anywhere an example would feel bolted on. Roughly half of passages should have one.

- **25–80 words.** One to three concrete, ordinary modern situations: work, family, phones and social media, commuting, queues, group chats, hobbies, sport, news.
- Write it as plain sentences, not a list. Start straight in, e.g. "Think of the colleague who…" or "The modern version of the Greens and the Blues is…".
- Specific beats generic: "refreshing your post to see who liked it" beats "seeking validation".
- Don't name real living people, brands as villains, or political sides.

## Worked examples (this is the standard)

**1.5** (tutor: neither Green nor Blue at the Circus, endure hard work, want little, mind your own business, don't listen to slander)

```json
{
  "summary": "Marcus credits his tutor with a handful of habits that keep you steady: don't throw yourself into tribal rivalries, put up with hard work, want less, do things yourself, stay out of other people's business, and don't lend your ear to gossip.\n\nThe Greens and Blues were the rival chariot-racing teams, with fans as fierce as any today. The point isn't that sport is bad, but that picking a side and getting worked up over it is a cheap way to lose your calm.",
  "today": "The modern Greens and Blues are the football rivalry, the online pile-on or the office faction you're invited to join. Wanting little might mean not upgrading the phone that works fine; minding your own business might mean not forwarding the screenshot in the group chat."
}
```

**2.1** (begin the morning expecting difficult people)

```json
{
  "summary": "Expect difficult people, and decide in advance how you'll meet them. People behave badly because they've misunderstood what's actually good for them, not because they're monsters. And since they share the same human nature and the same capacity to reason as you, they're kin, not enemies.\n\nThey can't really harm you, because no one else can make you act badly. Getting angry or giving them the cold shoulder goes against what we're built for: working together, like two hands.",
  "today": "Before the commute or the first meeting, take a moment to expect the person who pushes into the queue, the colleague who takes the credit, the reply-all that annoys you. Having pictured it already, you're more likely to respond calmly than to snap."
}
```

**6.43** (does the sun do the work of the rain?)

```json
{
  "summary": "Everything in nature has its own job. The sun doesn't try to be rain, and the stars all differ, yet together they make one working whole. People are the same: you don't have to do everyone's part, only your own, and do it well, trusting that different roles add up to something shared."
}
```

**7.69** (live each day as if it were the last)

```json
{
  "summary": "Good character comes down to three things: living each day as though it might be your last, keeping an even keel (neither frantic nor lazy), and being genuine instead of putting on a front. Thinking about your last day isn't meant to be morbid. It's meant to clear away what doesn't matter.",
  "today": "If today were the last, you probably wouldn't spend the evening doom-scrolling or nursing a grudge from a meeting, and you'd likely say the thing you keep meaning to say to someone you love."
}
```
