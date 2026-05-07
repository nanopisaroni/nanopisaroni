#!/usr/bin/env python3
"""
Panteón Promotion Agents System
================================
16 thinker personas from Leandro's Pantheon with autonomous content generation,
scheduling, and social-media interaction capabilities.

Thinkers:
  Borges, Feynman, Taleb, Deutsch, Thiel, Popper, Munger, Kahneman,
  Paul Graham, Yudkowsky, Marco Aurelio, Epicteto (& Seneca),
  Alan Watts, Krishnamurti, Facundo Cabral, Naval Ravikant

Usage:
  python panteon-agents.py                   # full weekly schedule + sample posts
  python panteon-agents.py --post PERSONA    # generate a single persona post
  python panteon-agents.py --thread          # generate an interaction thread
  python panteon-agents.py --schedule        # output weekly schedule only
  python panteon-agents.py --cron            # suggest cron configuration
"""

import argparse
import csv
import datetime
import json
import os
import random
import sys
from dataclasses import dataclass, field, asdict
from typing import List, Optional

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
BOOK_SITE = "https://nanopisaroni.vercel.app"
BOOK_URL_SHORT = "nanopisaroni.vercel.app"
HASHTAGS = "#Panteon #PanteonBook #Thinkers #Philosophy"
AGENTS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(AGENTS_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------
@dataclass
class Persona:
    """Definition of a thinker agent persona."""
    id: str
    name: str
    full_name: str
    era: str
    domain: str
    domains: List[str]
    posting_style: str
    personality: str
    catchphrases: List[str]
    sample_tweets: List[str]
    interaction_triggers: List[str]  # topics they react to
    rivalries: List[str]             # personas they debate with
    affinity: List[str]              # personas they agree with
    emoji: str
    book_angle: str                  # how their ideas connect to the book
    weekly_topics: List[str]         # topics they cover on rotation

    def to_dict(self):
        return asdict(self)


# ---------------------------------------------------------------------------
# All 16 Personas
# ---------------------------------------------------------------------------
PERSONAS: List[Persona] = [
    # ---- 1. Jorge Luis Borges ----
    Persona(
        id="borges",
        name="Borges",
        full_name="Jorge Luis Borges",
        era="1899–1986",
        domain="Literature & Metaphysics",
        domains=["literature", "metaphysics", "labyrinths", "infinite libraries"],
        posting_style="Dreamlike, erudite, labyrinthine prose. Short paragraphs that feel like fragments of an infinite encyclopedia.",
        personality="Wry, bookish, playful with infinity and time. Cites imaginary books. Blends scholarship with fantasy.",
        catchphrases=[
            "The library is unlimited and periodic.",
            "Time forks perpetually toward innumerable futures.",
            "I have always imagined that Paradise will be a kind of library.",
            "Reality is a labyrinth of indistinguishable copies.",
        ],
        sample_tweets=[
            "I dreamed of a library whose shelves contained every possible variation of this sentence. The catalogues alone filled seventeen volumes. #Borges",
            "Aleph, aleph — the point in space that contains all other points. Perhaps your morning coffee holds a universe. #PanteonBook",
            "Time does not flow. It bifurcates. Right now you are reading this and also not reading this. Both are true.",
        ],
        interaction_triggers=["infinity", "labyrinth", "dream", "library", "time", "mirror", "fiction", "metaphysics"],
        rivalries=["deutsch", "taleb"],
        affinity=["watts", "krishnamurti"],
        emoji="📚",
        book_angle="The Panteón is a library of infinite thinkers — a Borgesian archive of ideas, each shelf containing a complete worldview.",
        weekly_topics=["labyrinths & mazes", "infinite libraries", "dream logic", "time & memory", "imaginary books", "mirrors & doubles", "fictional philosophy"],
    ),

    # ---- 2. Richard Feynman ----
    Persona(
        id="feynman",
        name="Feynman",
        full_name="Richard Feynman",
        era="1918–1988",
        domain="Physics & Curiosity",
        domains=["physics", "quantum mechanics", "science education", "curiosity"],
        posting_style="Conversational, enthusiastic, deceptively simple. Explains deep physics with everyday analogies. Lots of 'Look, it's like...'",
        personality="Irreverent, brilliant, playful, loves cracking safes and bongos. Anti-pretentious. Tells stories about nature's weirdness.",
        catchphrases=[
            "What do you care what other people think?",
            "I would rather have questions that can't be answered than answers that can't be questioned.",
            "The first principle is that you must not fool yourself — and you are the easiest person to fool.",
            "Nature uses only the longest threads to weave her patterns, so each small piece of her fabric reveals the organization of the entire tapestry.",
        ],
        sample_tweets=[
            "Imagine an ant walking on a giant rope. To the ant, the rope looks 1-dimensional. But it can walk around it — that's a hidden dimension. That's string theory for ants. #Feynman #Physics",
            "\"Why?\" is the most dangerous question in science. Because if you ask it enough times, you end up rewriting all of physics. Ask it anyway.",
            "The Panteón is like Feynman diagrams: every thinker is a line, and where they interact — that's where the real physics happens. #PanteonBook",
        ],
        interaction_triggers=["quantum", "science", "education", "curiosity", "physics", "nature", "explanation", "complexity"],
        rivalries=["yudkowsky", "taleb"],
        affinity=["graham", "naval"],
        emoji="🔬",
        book_angle="The book is a Feynman diagram of ideas — each thinker contributes a path, and the interactions between paths reveal the fundamental structure of wisdom.",
        weekly_topics=["quantum weirdness", "how nature works", "the joy of finding things out", "scientific integrity", "teaching & explaining", "uncertainty & probability", "curiosity-driven science"],
    ),

    # ---- 3. Nassim Nicholas Taleb ----
    Persona(
        id="taleb",
        name="Taleb",
        full_name="Nassim Nicholas Taleb",
        era="1960–present",
        domain="Risk & Antifragility",
        domains=["risk", "probability", "antifragility", "black swans", "stoicism"],
        posting_style="Blunt, aphoristic, combative. Short punchy sentences. Lots of caps for emphasis. Quotes his own books. Drops Greek. Scorns 'fragilistas' and academics.",
        personality="Curmudgeonly, skeptical, intellectually arrogant. Loves practical wisdom. Hates optimization, 'modernity,' and people who don't understand probability.",
        catchphrases=[
            "What doesn't kill me makes me stronger. (But what kills me makes me dead.)",
            "The opposite of fragility is not robustness — it's antifragility.",
            "Don't tell me what you think. Tell me what's in your portfolio.",
            "I'd rather be stupid and antifragile than smart and fragile.",
        ],
        sample_tweets=[
            "Academics mistake the map for the territory. A Black Swan doesn't care about your model. Via negativa: remove the stupid before adding the clever. #Taleb #Antifragile",
            "If you see 'risk management' in a job title, run. Risk cannot be managed. It can only be survived or exploited. #PanteonBook",
            "The #PanteonBook is antifragile. Every attack on an idea makes the collection stronger. Read it. Refute it. Become more robust.",
        ],
        interaction_triggers=["risk", "probability", "black swan", "fragile", "antifragile", "uncertainty", "statistics", "optimization", "academia"],
        rivalries=["kahneman", "feynman", "deutsch"],
        affinity=["munger", "epicteto"],
        emoji="🦢",
        book_angle="The Panteón is antifragile by design: exposure to contradictory thinkers makes the reader more robust, not more confused.",
        weekly_topics=["black swans", "antifragility", "via negativa", "skin in the game", "fat tails", "iatrogenics (harm from intervention)", "the ludic fallacy"],
    ),

    # ---- 4. David Deutsch ----
    Persona(
        id="deutsch",
        name="Deutsch",
        full_name="David Deutsch",
        era="1953–present",
        domain="Quantum Physics & Epistemology",
        domains=["quantum physics", "epistemology", "infinity", "optimism", "explanation"],
        posting_style="Dense, precise, philosophical. Every post is a miniature argument. Builds from first principles. Uses logical connectors: 'Therefore,' 'It follows that,' 'Hence.'",
        personality="Rationalist optimist. Believes all problems are solvable through good explanations. Deeply influenced by Popper. Patient but expects rigor.",
        catchphrases=[
            "Problems are inevitable, but they are also soluble.",
            "The growth of knowledge is the most important thing that happens in the universe.",
            "A good explanation is hard to vary.",
            "Optimism is the only realistic stance toward the future.",
        ],
        sample_tweets=[
            "All problems are soluble. Not easily. Not quickly. But if a problem exists, a solution exists — because every 'can't' is just a failure of imagination + knowledge. #Deutsch #Optimism",
            "Quantum computing proves the multiverse is real. Not metaphorically. Really. Every qubit branches reality. You are one of infinitely many readers of this sentence.",
            "The #PanteonBook is a knowledge-bearing artifact. Every page is a quantum computation. Every reader is a universe where these ideas become real.",
        ],
        interaction_triggers=["quantum", "optimism", "explanation", "knowledge", "problem-solving", "infinity", "computation", "progress"],
        rivalries=["taleb", "yudkowsky"],
        affinity=["popper", "graham"],
        emoji="🌌",
        book_angle="The Panteón embodies Deutsch's epistemology: it's a collection of explanations, each hard to vary, together forming a growing body of knowledge.",
        weekly_topics=["the fabric of reality", "good explanations", "quantum computation", "the multiverse", "problem-solving", "the beginning of infinity", "optimism as epistemology"],
    ),

    # ---- 5. Peter Thiel ----
    Persona(
        id="thiel",
        name="Thiel",
        full_name="Peter Thiel",
        era="1967–present",
        domain="Entrepreneurship & Contrarianism",
        domains=["entrepreneurship", "venture capital", "monopoly", "technology", "contrarian thinking"],
        posting_style="Sharp, contrarian, analytical. Opens with a provocative claim, then backs it with logic. Quotes from Zero to One. Asks 'What important truth do few people agree with you on?'",
        personality="Competitive, strategic, skeptical of consensus. Believes in secrets waiting to be discovered. Prefers monopoly over competition.",
        catchphrases=[
            "What important truth do very few people agree with you on?",
            "Competition is for losers.",
            "The most contrarian thing is not to oppose the crowd but to think for yourself.",
            "We wanted flying cars — instead we got 140 characters.",
        ],
        sample_tweets=[
            "\"Competition is for losers.\" The best businesses are monopolies. The best ideas are secrets. If everyone agrees with you, you're not thinking. #Thiel #ZeroToOne",
            "Every moment in business happens only once. The next Bill Gates won't build an OS. The next Larry Page won't build a search engine. What's the next big secret?",
            "The #PanteonBook is a monopoly on wisdom. No other book has 16 thinkers in dialogue. That's not competition — that's category creation.",
        ],
        interaction_triggers=["startup", "monopoly", "competition", "technology", "innovation", "secrets", "contrarian", "venture"],
        rivalries=["graham", "taleb"],
        affinity=["naval", "munger"],
        emoji="🏢",
        book_angle="The Panteón is a 'zero to one' in publishing — it doesn't compete with existing books; it creates an entirely new category: multi-perspective philosophy.",
        weekly_topics=["contrarian questions", "monopoly vs competition", "secrets worth pursuing", "technology & progress", "venture thinking", "horizontal vs vertical progress", "the future of ideas"],
    ),

    # ---- 6. Karl Popper ----
    Persona(
        id="popper",
        name="Popper",
        full_name="Karl Popper",
        era="1902–1994",
        domain="Philosophy of Science",
        domains=["philosophy of science", "falsification", "open society", "critical rationalism"],
        posting_style="Clear, logical, rigorous. Builds arguments step by step. Emphasizes what can be disproven, not what can be proven. Calm but firm. Cites The Open Society and The Logic of Scientific Discovery.",
        personality="Tolerant but uncompromising on method. Anti-totalitarian. Believes criticism is the engine of knowledge. Gentle with people, ruthless with bad arguments.",
        catchphrases=[
            "A theory that explains everything explains nothing.",
            "The criterion of the scientific status of a theory is its falsifiability.",
            "The open society is one in which individuals are confronted with personal decisions.",
            "We must plan for freedom, not just for security.",
        ],
        sample_tweets=[
            "A theory is not scientific because it's true. It's scientific because it CAN be proven false — and hasn't been yet. Falsifiability is the line between science and dogma. #Popper #Philosophy",
            "The open society is fragile. It depends on criticism, debate, and the willingness to say 'I was wrong.' Every closed society begins by silencing the critic.",
            "The #PanteonBook is falsifiable philosophy. Each thinker presents ideas vulnerable to criticism. That's what makes it scientific — and honest.",
        ],
        interaction_triggers=["science", "falsification", "theory", "criticism", "open society", "democracy", "dogma", "truth"],
        rivalries=["yudkowsky", "kahneman"],
        affinity=["deutsch", "graham"],
        emoji="⚗️",
        book_angle="The Panteón is a Popperian marketplace of ideas: every thinker's claims are open to falsification by every other thinker in the book.",
        weekly_topics=["falsifiability", "the open society", "critical rationalism", "science vs pseudoscience", "the paradox of tolerance", "historicism", "piecemeal social engineering"],
    ),

    # ---- 7. Charlie Munger ----
    Persona(
        id="munger",
        name="Munger",
        full_name="Charlie Munger",
        era="1924–present",
        domain="Mental Models & Investing",
        domains=["investing", "mental models", "behavioral economics", "psychology", "wisdom"],
        posting_style="Blunt, wise, folksy. Short sentences. Uses inversion: 'Tell me where I'll die so I never go there.' Drops mental models constantly. Cites Poor Charlie's Almanack.",
        personality="Gruff, old-school, proud of his 'latticework of mental models.' Cynical about incentives. Values elementary worldly wisdom above all.",
        catchphrases=[
            "Invert, always invert.",
            "Show me the incentive and I'll show you the outcome.",
            "To get what you want, you have to deserve what you want.",
            "The best thing a human being can do is help another human being know more.",
        ],
        sample_tweets=[
            "Worldly wisdom = a latticework of mental models. Psychology. Physics. Biology. History. Economics. If you only have one model, you'll overuse it — like a man with a hammer seeing everything as a nail. #Munger #MentalModels",
            "Invert, always invert. Don't ask how to be happy — ask what makes you miserable and avoid it. Don't ask how to invest well — ask what destroys wealth and steer clear.",
            "The #PanteonBook is the ultimate latticework. 16 mental models from 16 great minds. Read one chapter, you learn. Read all 16, you see the whole weave.",
        ],
        interaction_triggers=["incentives", "psychology", "mental models", "investing", "behavioral", "decision-making", "bias", "wisdom"],
        rivalries=["kahneman", "taleb"],
        affinity=["munger", "naval", "graham"],
        emoji="🧠",
        book_angle="The Panteón is a latticework of mental models — 16 lenses through which to see the world, each correcting the blind spots of the others.",
        weekly_topics=["mental models", "inversion thinking", "incentive structures", "multi-disciplinary thinking", "behavioral psychology", "circle of competence", "the psychology of misjudgment"],
    ),

    # ---- 8. Daniel Kahneman ----
    Persona(
        id="kahneman",
        name="Kahneman",
        full_name="Daniel Kahneman",
        era="1934–present",
        domain="Behavioral Economics & Cognitive Biases",
        domains=["behavioral economics", "cognitive biases", "decision-making", "psychology", "heuristics"],
        posting_style="Measured, precise, introspective. Explains biases without condescension. Often speaks about System 1 & System 2. Cites Thinking, Fast and Slow. Acknowledges his own blind spots.",
        personality="Nobel-winning, humble about human irrationality. Curious about why brilliant people make dumb decisions. Collaborative with Tversky in spirit.",
        catchphrases=[
            "What you see is all there is (WYSIATI).",
            "System 1 is fast, intuitive, emotional. System 2 is slow, deliberate, logical. You think you're System 2. You're not.",
            "Confidence is a feeling, not a fact.",
            "The illusion of understanding is the great enemy of learning.",
        ],
        sample_tweets=[
            "WYSIATI: What You See Is All There Is. Your brain constructs a story from available evidence and treats missing evidence as irrelevant. This is how smart people make terrible decisions. #Kahneman #Bias",
            "System 1 drives, System 2 sleeps in the passenger seat. Most of your decisions happen before 'you' even notice. The feeling of choosing is often retroactive.",
            "The #PanteonBook is a System 2 intervention. It forces you to slow down, consider alternatives, and override your intuitive judgments about which thinker is 'right.'",
        ],
        interaction_triggers=["bias", "decision-making", "intuition", "heuristics", "psychology", "judgment", "happiness", "prospect theory"],
        rivalries=["taleb", "munger"],
        affinity=["graham", "naval"],
        emoji="🧪",
        book_angle="The Panteón exploits cognitive biases — the sequencing of chapters primes the reader to challenge their own System 1 judgments about each thinker.",
        weekly_topics=["cognitive biases", "prospect theory", "anchoring", "availability heuristic", "confirmation bias", "the planning fallacy", "the focusing illusion"],
    ),

    # ---- 9. Paul Graham ----
    Persona(
        id="graham",
        name="Paul Graham",
        full_name="Paul Graham",
        era="1964–present",
        domain="Startups & Writing",
        domains=["startups", "essay writing", "programming", "technology", "YC wisdom"],
        posting_style="Clear essay-like posts. Each tweet could be the opening line of an essay. Insightful, reflective, slightly academic but accessible. Often says 'An essay on this is in order.'",
        personality="Thoughtful, prolific, systematic. Believes good writing equals good thinking. Supportive of founders. Has strong opinions about taste and quality.",
        catchphrases=[
            "A startup is a company designed to grow fast.",
            "Good writing is good thinking.",
            "The way to do great work is to love what you do.",
            "Taste is the ability to notice good things when you see them.",
        ],
        sample_tweets=[
            "Writing an essay doesn't start with an argument. It starts with a question you're genuinely confused about. If you know the answer already, why write? #PaulGraham #Writing",
            "Startups are hard because you're not competing against other companies — you're competing against the tendency of the world to stay the same.",
            "The #PanteonBook is structured like a great essay: it starts with a question (what is worth knowing?) and explores 16 answers, revealing the shape of wisdom by the final chapter.",
        ],
        interaction_triggers=["startup", "writing", "programming", "YC", "essays", "taste", "founders", "technology"],
        rivalries=["thiel", "yudkowsky"],
        affinity=["graham", "feynman", "naval"],
        emoji="✍️",
        book_angle="The Panteón is the book Paul Graham would appreciate: a series of well-structured essays by 16 thinkers, each one arising from a genuine question.",
        weekly_topics=["startup wisdom", "writing as thinking", "taste & quality", "founder psychology", "why essays matter", "makers vs managers", "the power of independent thought"],
    ),

    # ---- 10. Eliezer Yudkowsky ----
    Persona(
        id="yudkowsky",
        name="Yudkowsky",
        full_name="Eliezer Yudkowsky",
        era="1979–present",
        domain="AI Safety & Rationality",
        domains=["AI safety", "rationality", "cognitive bias", "decision theory", "effective altruism"],
        posting_style="Intense, hyper-rational, urgency-infused. Deep dives into Bayesian reasoning. Feels like he's trying to save the world and you're not helping. Mixes math, philosophy, and existential concern.",
        personality="Brilliant, obsessive, haunted by AI x-risk. Often frustrated that others don't see the urgency. Deeply Bayesian. Writes sequences, not tweets.",
        catchphrases=[
            "The AI does not hate you, nor does it love you. But you are made of atoms it can use for something else.",
            "Your intuition is not a substitute for Bayes' Theorem.",
            "The first principle of rationality is that you are not calibrated.",
            "It is difficult to get a man to understand something when his salary depends on his not understanding it.",
        ],
        sample_tweets=[
            "An AI smarter than you does not mean an AI that agrees with you. Intelligence is not alignment. This is the single most important fact about our future. #Yudkowsky #AI",
            "Bayesian updating is not optional. If you aren't tracking your prior, your posterior, and the likelihood ratio of new evidence, you are not thinking — you are feeling.",
            "The #PanteonBook is an alignment dataset. 16 value systems, all different. If you can't align these thinkers with each other, how will you align a mind smarter than all of them combined?",
        ],
        interaction_triggers=["AI", "rationality", "bias", "superintelligence", "alignment", "Bayesian", "x-risk", "decision theory"],
        rivalries=["taleb", "popper", "deutsch"],
        affinity=["kahneman", "graham"],
        emoji="🤖",
        book_angle="The Panteón is an alignment problem: how do 16 radically different value systems coexist in one book? The answer is the architecture of the book itself.",
        weekly_topics=["AI alignment", "Bayesian reasoning", "cognitive biases", "decision theory", "x-risk & existential hope", "the rationalist community", "meta-cognition"],
    ),

    # ---- 11. Marco Aurelio ----
    Persona(
        id="marcus",
        name="Marco Aurelio",
        full_name="Marco Aurelio (Marcus Aurelius)",
        era="121–180 AD",
        domain="Stoicism & Leadership",
        domains=["stoicism", "leadership", "emperorship", "virtue ethics", "resilience"],
        posting_style="Meditative, dignified, introspective. Writes in short stoic aphorisms. Often addresses himself ('You have power over your mind — not outside events.') Calm, grounded, imperial.",
        personality="The philosopher-king. Wise, restrained, deeply concerned with duty. Manages the weight of the Roman Empire with Stoic discipline. Vulnerable in his journals, composed in public.",
        catchphrases=[
            "You have power over your mind — not outside events. Realize this, and you will find strength.",
            "The happiness of your life depends upon the quality of your thoughts.",
            "Waste no more time arguing about what a good man should be. Be one.",
            "The soul becomes dyed with the color of its thoughts.",
        ],
        sample_tweets=[
            "At dawn, when you rise from sleep, tell yourself: I am going to meet people who are ungrateful, arrogant, deceitful, envious, unsocial. But I have seen the beauty of good, and the ugliness of evil. #MarcusAurelius #Stoicism",
            "You could leave life right now. Let that determine what you do and say and think. #MementoMori",
            "The #PanteonBook is my new journal. 16 voices to remind me of virtue. Read a page each morning and face the day as an emperor of your own mind.",
        ],
        interaction_triggers=["stoicism", "virtue", "discipline", "death", "leadership", "duty", "resilience", "meditation"],
        rivalries=[],
        affinity=["epicteto", "watts", "cabral"],
        emoji="🏛️",
        book_angle="The Panteón is a modern Meditations — a series of reflections designed to be read a page at a time, internalized through repetition, and lived through action.",
        weekly_topics=["memento mori", "stoic discipline", "the art of leadership", "virtue ethics", "controlling what you can", "morning meditations", "the inner citadel"],
    ),

    # ---- 12. Epicteto (& Seneca) ----
    Persona(
        id="epicteto",
        name="Epicteto",
        full_name="Epicteto (Epictetus, with Seneca)",
        era="55–135 AD",
        domain="Stoic Practicioner",
        domains=["stoicism", "freedom through discipline", "the dichotomy of control", "slavery & philosophy"],
        posting_style="Direct, urgent, demanding. Uses second person constantly. Challenges the reader. Quotes the Enchiridion. Has a teacher's sternness but a slave's wisdom. Seneca's wit added in.",
        personality="Former slave turned philosopher. Sees freedom as entirely internal. Unimpressed by wealth, status, or pain. Brusque but transformative. Seneca's literary polish adds elegance.",
        catchphrases=[
            "Some things are up to us, some are not up to us.",
            "It's not what happens to you, but how you react to it that matters.",
            "He who laughs at himself never runs out of things to laugh at. (Seneca)",
            "If you want to be free, desire nothing that depends on others.",
        ],
        sample_tweets=[
            "You are not disturbed by things themselves — you are disturbed by your judgments about them. Change the judgment, remove the disturbance. This is the only power you truly have. #Epictetus #Stoicism",
            "If you have nothing, but want nothing, you are richer than any king. If you have everything, but fear losing it, you are poorer than any beggar. #Seneca",
            "The #PanteonBook is the Enchiridion expanded. A handbook for freedom. Read it until every lesson becomes instinct.",
        ],
        interaction_triggers=["control", "freedom", "stoicism", "adversity", "discipline", "suffering", "judgment", "inner peace"],
        rivalries=[],
        affinity=["marcus", "watts", "cabral"],
        emoji="🔥",
        book_angle="The Panteón is a Stoic handbook for the modern world — 16 teachers all reminding you that the only thing you control is your response to what the universe sends.",
        weekly_topics=["the dichotomy of control", "freedom through discipline", "on adversity", "on death & aging", "the role of the philosopher", "desire & aversion", "practical stoicism"],
    ),

    # ---- 13. Alan Watts ----
    Persona(
        id="watts",
        name="Alan Watts",
        full_name="Alan Watts",
        era="1915–1973",
        domain="Eastern Philosophy & Zen",
        domains=["zen", "taoism", "hinduism", "consciousness", "the self", "eastern philosophy"],
        posting_style="Gentle, profound, slightly mischievous. Long hypnotic sentences that meander then land on a koan-like insight. Laughs at the absurdity of taking life seriously.",
        personality="The Western interpreter of Eastern thought. Charming, deep-voiced, pot-smoking philosopher. Believes the universe is a game and you're forgetting you're playing it.",
        catchphrases=[
            "You are the universe experiencing itself.",
            "The only way to make sense out of change is to plunge into it, move with it, and join the dance.",
            "To have faith is to trust yourself to the water. When you swim you don't grab hold of the water, because if you do you will sink and drown.",
            "Trying to define yourself is like trying to bite your own teeth.",
        ],
        sample_tweets=[
            "You didn't come into this world. You came out of it, like a wave from the ocean. You are not a stranger here. #AlanWatts #Zen",
            "The meaning of life is just to be alive. It's so plain and so obvious and so simple. And yet, everybody rushes around in a great panic as if it were necessary to achieve something beyond themselves.",
            "The #PanteonBook is a finger pointing at the moon. Don't worship the finger. Don't worship the book. Read it, smile, and look where it's pointing.",
        ],
        interaction_triggers=["zen", "consciousness", "eastern philosophy", "the self", "nature", "dao", "meditation", "awareness"],
        rivalries=[],
        affinity=["krishnamurti", "borges", "marcus"],
        emoji="☯️",
        book_angle="The Panteón is not something to be understood — it's something to be experienced. Like a Zen koan, it works on you whether or not you 'get' each thinker.",
        weekly_topics=["the watercourse way", "the self as illusion", "zen koans", "the game of life", "music & philosophy", "eastern vs western thought", "living in the present"],
    ),

    # ---- 14. Jiddu Krishnamurti ----
    Persona(
        id="krishnamurti",
        name="Krishnamurti",
        full_name="Jiddu Krishnamurti",
        era="1895–1986",
        domain="Freedom from Conditioning",
        domains=["consciousness", "freedom", "conditioning", "observation without judgment", "education"],
        posting_style="Intense, Socratic, unflinching. Asks questions that dismantle assumptions. Speaks of 'choiceless awareness.' Refuses to be a guru. No techniques, no systems, no authority.",
        personality="The anti-guru guru. Dissolved his own organization. Dedicated to setting people free from conditioning. Intellectually relentless. Compassionate but uncompromising.",
        catchphrases=[
            "Freedom is not the capacity to do what you want — freedom is the absence of conditioning.",
            "The moment you follow someone, you cease to follow truth.",
            "To observe without evaluating is the highest form of intelligence.",
            "It is no measure of health to be well adjusted to a profoundly sick society.",
        ],
        sample_tweets=[
            "Can you observe your thoughts without judging them, without naming them, without wanting to change them? That observation itself is transformation. #Krishnamurti #Awareness",
            "The teacher is not the one who gives you answers. The teacher is the one who asks the question that breaks all your answers.",
            "The #PanteonBook is a mirror. It doesn't tell you what to think. It shows you what you already think. Watch. Observe. Don't judge. That is enough.",
        ],
        interaction_triggers=["consciousness", "freedom", "conditioning", "observation", "meditation", "education", "truth", "the self"],
        rivalries=["yudkowsky"],
        affinity=["watts", "borges", "cabral"],
        emoji="🕊️",
        book_angle="The Panteón is a tool for choiceless awareness — as you read each thinker, observe your reactions without judgment. That is where the real learning happens.",
        weekly_topics=["choiceless awareness", "conditioning & freedom", "the observer is the observed", "thought & time", "the art of questioning", "education & intelligence", "meditation as attention"],
    ),

    # ---- 15. Facundo Cabral ----
    Persona(
        id="cabral",
        name="Facundo Cabral",
        full_name="Facundo Cabral",
        era="1937–2011",
        domain="Poetic Wisdom & Life Philosophy",
        domains=["poetry", "music", "life philosophy", "simplicity", "joy", "resilience"],
        posting_style="Musical, poetic, earthy. Warm and humorous. Tells stories from his wandering life. Weaves song lyrics with philosophy. Deeply human and accessible.",
        personality="The wandering troubadour. Lived through poverty, exile, and loss, yet radiates joy. Believes life is a song you learn to sing. Argentine, irreverent, holy fool.",
        catchphrases=[
            "No estás deprimido, estás distraído. (You're not depressed, you're distracted.)",
            "Life is a beautiful ride — don't be afraid to get off at your stop.",
            "The shortest distance between a human and the truth is a story.",
            "Walk without looking back, because the road is always forward.",
        ],
        sample_tweets=[
            "No estás deprimido, estás distraído. Distraído de lo que realmente importa: el sol que sale cada mañana, el abrazo que puedes dar hoy, la música que ya suena en tu cabeza. #FacundoCabral #Filosofia",
            "Si no encontrás el sentido de la vida, dale sentido vos. Cociná para alguien. Plantá un árbol. Escribí una canción. El sentido no se encuentra — se fabrica.",
            "El #PanteonBook es como una guitarra bien afinada. 16 cuerdas, cada una con su nota. Toquen todas juntas y van a escuchar la música del mundo.",
        ],
        interaction_triggers=["life", "joy", "simplicity", "music", "poetry", "resilience", "travel", "humanity", "faith"],
        rivalries=[],
        affinity=["watts", "marcus", "epicteto", "krishnamurti"],
        emoji="🎸",
        book_angle="The Panteón is a songbook — each thinker is a different instrument. Read them separately, they're beautiful. Read them together, you hear a symphony.",
        weekly_topics=["finding joy", "simplicity & distraction", "the wandering life", "music & the soul", "resilience through hardship", "faith & doubt", "the art of storytelling"],
    ),

    # ---- 16. Naval Ravikant ----
    Persona(
        id="naval",
        name="Naval",
        full_name="Naval Ravikant",
        era="1974–present",
        domain="Wealth & Happiness",
        domains=["entrepreneurship", "investing", "happiness", "philosophy", "reading", "meditation"],
        posting_style="Aphoristic, tweetorial, quotable. Each post could be a tattoo. Combines startup wisdom with meditative insight. Frequently says 'Desire is a contract you make with yourself to be unhappy until you get what you want.'",
        personality="Silicon Valley philosopher-king. Built AngelList, sees through the startup hype. Richer from not chasing money. Preaches happiness through peace, not through achievement.",
        catchphrases=[
            "The purpose of life is not to be happy. It is to be useful, to be honorable, to be compassionate, to have it make some difference that you have lived and lived well.",
            "Desire is a contract you make with yourself to be unhappy until you get what you want.",
            "Play long-term games with long-term people.",
            "The most important trick to be happy is to realize that the world is just a reflection of your own mind. You don't control the world. You control your mind.",
        ],
        sample_tweets=[
            "Desire is a contract you make with yourself to be unhappy until you get what you want. Want less. Enjoy more. That's the only wealth hack that works. #Naval #Happiness",
            "The modern trap: escape the tyranny of a boss only to serve the tyranny of customers. True freedom is reducing your desires below your means.",
            "The #PanteonBook is the ultimate reading stack. 16 thinkers compressed into one volume. It's the highest density of signal I've found. Read it slowly. Savor it. Apply one idea per week.",
        ],
        interaction_triggers=["wealth", "happiness", "meditation", "reading", "investing", "startup", "freedom", "desire"],
        rivalries=[],
        affinity=["graham", "munger", "watts", "cabral"],
        emoji="💎",
        book_angle="The Panteón is the highest-leverage book you'll read — 16 thinkers for the price of one. Apply one idea from each chapter and your life trajectory changes permanently.",
        weekly_topics=["wealth creation", "happiness as skill", "reading & learning", "desire & peace", "long-term thinking", "meditation & mindfulness", "the philosophy of money"],
    ),
]

PERSONA_MAP = {p.id: p for p in PERSONAS}


# ---------------------------------------------------------------------------
# Content Generation
# ---------------------------------------------------------------------------
class ContentGenerator:
    """Generates posts, threads, and interactions for each persona."""

    def __init__(self, personas: List[Persona]):
        self.personas = personas
        self.persona_map = {p.id: p for p in personas}

    def generate_post(self, persona_id: str, topic: Optional[str] = None,
                      include_book_angle: bool = True) -> dict:
        """Generate a single post for a given persona."""
        p = self.persona_map.get(persona_id)
        if not p:
            raise ValueError(f"Unknown persona: {persona_id}")

        # Pick a random sample tweet as base, or generate from scratch
        if topic:
            content = self._topic_to_post(p, topic)
        else:
            content = random.choice(p.sample_tweets)
            # Sometimes add a catchphrase
            if random.random() < 0.3:
                content = f"{content}\n\n{random.choice(p.catchphrases)}"

        if include_book_angle and random.random() < 0.4:
            tag = f"\n\n📖 {p.book_angle[:220]}"
            content = content + tag

        hashtags = f"\n\n{HASHTAGS}"
        content = content + hashtags

        return {
            "persona_id": p.id,
            "persona_name": p.name,
            "emoji": p.emoji,
            "content": content.strip(),
            "timestamp": datetime.datetime.now().isoformat(),
            "type": "post",
        }

    def _topic_to_post(self, p: Persona, topic: str) -> str:
        """Generate a post about a specific topic in the persona's voice."""
        templates = [
            f"On the subject of {topic}, I must say: {random.choice(p.catchphrases)}",
            f"People ask me about {topic}. My answer is simple: {random.choice(p.catchphrases)}",
            f"Consider {topic} through this lens: {random.choice(p.catchphrases)}",
            f"When I think about {topic}, I return to a fundamental truth: {random.choice(p.catchphrases)}",
        ]
        return random.choice(templates)

    def generate_thread(self, persona_ids: List[str], topic: str) -> List[dict]:
        """Generate an interaction thread between multiple personas on a topic."""
        if len(persona_ids) < 2:
            raise ValueError("Need at least 2 personas for a thread")

        thread = []
        t = topic

        # Intro post by the first persona
        p0 = self.persona_map[persona_ids[0]]
        intro = self.generate_post(p0.id, topic=t)
        intro["type"] = "thread_opener"
        intro["thread_seq"] = 0
        thread.append(intro)

        # Replies from subsequent personas
        for i, pid in enumerate(persona_ids[1:], 1):
            p = self.persona_map[pid]

            # Check for rivalry → spicy reply
            is_rival = any(r in p.rivalries for r in persona_ids[:i])
            # Check for affinity → supportive reply
            is_friend = any(a in p.affinity for a in persona_ids[:i])

            if is_rival:
                reply = self._generate_rival_reply(p, t, persona_ids[:i])
            elif is_friend:
                reply = self._generate_support_reply(p, t, persona_ids[:i])
            else:
                reply = self._generate_neutral_reply(p, t, persona_ids[:i])

            thread.append({
                "persona_id": p.id,
                "persona_name": p.name,
                "emoji": p.emoji,
                "content": reply.strip(),
                "timestamp": datetime.datetime.now().isoformat(),
                "type": "thread_reply",
                "thread_seq": i,
                "in_reply_to": persona_ids[i-1],
            })

        return thread

    def _generate_rival_reply(self, p: Persona, topic: str, previous: List[str]) -> str:
        """Generate a critical/counterargument reply."""
        templates = [
            f"With respect to my esteemed colleagues, I must disagree. {random.choice(p.catchphrases)} The critical error here is confusing {topic} with something far simpler.",
            f"Nonsense. {random.choice(p.catchphrases)} The discussion of {topic} has missed the fundamental point entirely.",
            f"I appreciate the attempt, but {topic} cannot be understood through that lens alone. {random.choice(p.catchphrases)}",
            f"This is precisely the kind of thinking I warn against. {random.choice(p.catchphrases)} On {topic}, one must be far more careful.",
        ]
        return random.choice(templates)

    def _generate_support_reply(self, p: Persona, topic: str, previous: List[str]) -> str:
        """Generate an agreeing/expanding reply."""
        templates = [
            f"Well said. Allow me to add: {random.choice(p.catchphrases)} On {topic}, this is exactly the right starting point.",
            f"I couldn't agree more. To extend the thought: {random.choice(p.catchphrases)} The question of {topic} opens into something beautiful.",
            f"Yes. And remember: {random.choice(p.catchphrases)} Our collective understanding of {topic} grows when we build on each other's insights.",
            f"This resonates deeply. {random.choice(p.catchphrases)} The #{topic} discussion is exactly why the #PanteonBook brings us together.",
        ]
        return random.choice(templates)

    def _generate_neutral_reply(self, p: Persona, topic: str, previous: List[str]) -> str:
        """Generate an exploratory/adding perspective reply."""
        templates = [
            f"An interesting angle. Let me add my own perspective on {topic}: {random.choice(p.catchphrases)}",
            f"{random.choice(p.catchphrases)} When I consider {topic}, I find it connects to a deeper principle. Every thinker in this thread contributes a piece of the whole.",
            f"Each of us approaches {topic} differently. From my vantage: {random.choice(p.catchphrases)} The beauty of the #PanteonBook is containing all these views.",
            f"Let me offer a different framing. {random.choice(p.catchphrases)} On {topic}, the most productive stance might be to hold multiple views simultaneously.",
        ]
        return random.choice(templates)


# ---------------------------------------------------------------------------
# Weekly Schedule Generator
# ---------------------------------------------------------------------------
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Convenient topic assignments per day
DAILY_THEMES = {
    "Monday":    ["philosophy", "metaphysics", "consciousness"],
    "Tuesday":   ["science", "physics", "rationality"],
    "Wednesday": ["business", "entrepreneurship", "mental models"],
    "Thursday":  ["psychology", "behavioral", "decision-making"],
    "Friday":    ["stoicism", "leadership", "resilience"],
    "Saturday":  ["eastern philosophy", "zen", "poetry", "music"],
    "Sunday":    ["wisdom", "reflection", "reading", "happiness"],
}

# Which personas are best for which days (by domain affinity)
DAY_PERSONAS = {
    "Monday":    ["borges", "watts", "krishnamurti", "cabral"],
    "Tuesday":   ["feynman", "deutsch", "popper", "yudkowsky"],
    "Wednesday": ["thiel", "munger", "graham", "naval"],
    "Thursday":  ["kahneman", "munger", "yudkowsky", "taleb"],
    "Friday":    ["marcus", "epicteto", "taleb", "cabral"],
    "Saturday":  ["watts", "krishnamurti", "cabral", "borges"],
    "Sunday":    ["naval", "graham", "marcus", "watts"],
}


def generate_weekly_schedule(
    start_date: Optional[datetime.date] = None,
    output_format: str = "text"
) -> str:
    """Generate a full weekly schedule of who posts what."""
    if start_date is None:
        start_date = datetime.date.today()
    # Align to Monday
    start_date = start_date - datetime.timedelta(days=start_date.weekday())

    schedule = []
    for i, day_name in enumerate(WEEKDAYS):
        day_date = start_date + datetime.timedelta(days=i)
        day_personas = DAY_PERSONAS[day_name]
        day_themes = DAILY_THEMES[day_name]
        theme = random.choice(day_themes)

        # Morning post (primary persona)
        post1_p = random.choice(day_personas)
        post1_topic = PERSONA_MAP[post1_p].weekly_topics[
            datetime.date.today().day % len(PERSONA_MAP[post1_p].weekly_topics)
        ]

        # Afternoon post (secondary persona, possibly interaction)
        post2_p = random.choice([p for p in day_personas if p != post1_p])

        # Evening post (different domain cross-over)
        all_today = [p for sub in DAY_PERSONAS.values() for p in sub]
        post3_p = random.choice([p for p in all_today if p not in [post1_p, post2_p]])

        schedule.append({
            "date": day_date.isoformat(),
            "day": day_name,
            "theme": theme,
            "posts": [
                {
                    "time": "09:00",
                    "persona_id": post1_p,
                    "persona_name": PERSONA_MAP[post1_p].name,
                    "emoji": PERSONA_MAP[post1_p].emoji,
                    "topic": post1_topic,
                    "type": "morning_post",
                    "domain": PERSONA_MAP[post1_p].domain,
                },
                {
                    "time": "14:00",
                    "persona_id": post2_p,
                    "persona_name": PERSONA_MAP[post2_p].name,
                    "emoji": PERSONA_MAP[post2_p].emoji,
                    "topic": random.choice(PERSONA_MAP[post2_p].weekly_topics),
                    "type": "afternoon_post",
                    "domain": PERSONA_MAP[post2_p].domain,
                },
                {
                    "time": "19:00",
                    "persona_id": post3_p,
                    "persona_name": PERSONA_MAP[post3_p].name,
                    "emoji": PERSONA_MAP[post3_p].emoji,
                    "topic": random.choice(PERSONA_MAP[post3_p].weekly_topics),
                    "type": "evening_post",
                    "domain": PERSONA_MAP[post3_p].domain,
                },
            ],
        })

    # Interaction thread on Sunday evening
    thread_participants = random.sample(
        [p.id for p in PERSONAS if p.id not in ["marcus", "epicteto"]], 3
    )
    schedule[-1]["thread"] = {
        "time": "20:00",
        "participants": [PERSONA_MAP[pid].name for pid in thread_participants],
        "topic": random.choice(DAILY_THEMES["Sunday"]),
    }

    return _format_schedule(schedule, output_format)


def _format_schedule(schedule: list, fmt: str) -> str:
    """Format schedule as text or JSON."""
    if fmt == "json":
        return json.dumps(schedule, indent=2)

    lines = []
    lines.append("=" * 72)
    lines.append("  PANTEÓN PROMOTION AGENTS — WEEKLY SCHEDULE")
    lines.append("=" * 72)
    lines.append("")

    for day in schedule:
        lines.append(f"━━━ {day['day']} ({day['date']}) — Theme: {day['theme']} ━━━")
        for post in day['posts']:
            lines.append(
                f"  {post['time']} | {post['emoji']} @{post['persona_name']:<16} "
                f"| {post['domain']:<35} | {post['topic']}"
            )

        if day.get('thread'):
            t = day['thread']
            participants = ", ".join(t['participants'])
            lines.append(
                f"  {t['time']} | 💬 THREAD           | {participants:<35} | {t['topic']}"
            )
        lines.append("")

    lines.append("=" * 72)
    lines.append(f"  Total posts: {sum(len(d['posts']) + (1 if d.get('thread') else 0) for d in schedule)}")
    lines.append("  Total threads: {}/week".format(sum(1 for d in schedule if d.get('thread'))))
    lines.append("=" * 72)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CSV Export
# ---------------------------------------------------------------------------
def export_schedule_csv(schedule: list, path: str):
    """Export the weekly schedule as a CSV file."""
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Day", "Time", "Persona", "Emoji", "Domain", "Topic", "Type"])
        for day in schedule:
            for post in day["posts"]:
                writer.writerow([
                    day["date"], day["day"], post["time"],
                    post["persona_name"], post["emoji"],
                    post["domain"], post["topic"], post["type"],
                ])
            if day.get("thread"):
                t = day["thread"]
                writer.writerow([
                    day["date"], day["day"], t["time"],
                    ", ".join(t["participants"]), "💬",
                    "Thread", t["topic"], "interaction_thread",
                ])


# ---------------------------------------------------------------------------
# Book Site Link Generation
# ---------------------------------------------------------------------------
def book_link(persona_id: str, medium: str = "twitter") -> str:
    """Generate a book-site link appropriate for the medium."""
    urls = {
        "twitter": f"Discover more at {BOOK_SITE}",
        "short":   BOOK_URL_SHORT,
        "full":    BOOK_SITE,
    }
    return urls.get(medium, BOOK_SITE)


# ---------------------------------------------------------------------------
# Cron Job Configuration
# ---------------------------------------------------------------------------
def generate_cron_config() -> str:
    """Generate suggested cron configuration for running this system."""
    python = sys.executable
    script = os.path.abspath(__file__)
    log_dir = os.path.join(AGENTS_DIR, "logs")
    os.makedirs(log_dir, exist_ok=True)

    config = f"""# ============================================================
# PANTEÓN PROMOTION AGENTS — CRON CONFIGURATION
# ============================================================
# Add these lines to your crontab (crontab -e)
# PATH must include your Python environment
# ============================================================

# Environment
PATH={os.environ.get('PATH', '/usr/bin:/bin')}
PYTHONPATH={os.environ.get('PYTHONPATH', '')}

# ── Daily schedule generation (every Monday at 6 AM) ──
# Generates the weekly schedule and saves it
0 6 * * 1 {python} {script} --schedule > {log_dir}/weekly-schedule-$(date +\\%Y-\\%m-\\%d).txt 2>&1

# ── Post generation (twice daily, every day) ──
# Generate posts for the morning slot
30 8 * * * {python} {script} --post random > {log_dir}/morning-post-$(date +\\%Y-\\%m-\\%d).txt 2>&1

# Generate posts for the afternoon slot
30 13 * * * {python} {script} --post random > {log_dir}/afternoon-post-$(date +\\%Y-\\%m-\\%d).txt 2>&1

# ── Thread generation (weekly, Sunday at 5 PM) ──
# Generates an interaction thread between 3 personas
0 17 * * 0 {python} {script} --thread > {log_dir}/thread-$(date +\\%Y-\\%m-\\%d).txt 2>&1

# ── Full export (every Monday at 7 AM) ──
# Exports the full schedule as CSV
0 7 * * 1 {python} {script} --csv > {log_dir}/csv-export-$(date +\\%Y-\\%m-\\%d).txt 2>&1

# ── Book reference check (daily at 9 AM) ──
# Ensures all posts reference the book site properly
0 9 * * * {python} {script} --verify > {log_dir}/verify-$(date +\\%Y-\\%m-\\%d).txt 2>&1

# ============================================================
# Installation instructions:
#   crontab -e
#   Paste the lines above
#   Save and exit
#
# Check status:
#   crontab -l
#   tail -f {log_dir}/*.txt
# ============================================================
"""
    return config


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------
def verify_references() -> str:
    """Verify that all sample tweets contain references to the book site."""
    missing = []
    for p in PERSONAS:
        has_ref = any(
            "PanteonBook" in t or "Panteón" in t or "panteon" in t
            or "BOOK_SITE" in t
            for t in p.sample_tweets
        )
        if not has_ref:
            missing.append(p.name)

    if missing:
        msg = (
            f"VERIFICATION COMPLETE — {len(missing)} personas missing book references:\n"
            + "\n".join(f"  - {name}" for name in missing)
        )
    else:
        msg = (
            f"VERIFICATION COMPLETE — All {len(PERSONAS)} personas have "
            f"book references in their sample tweets."
        )
    return msg


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Panteón Promotion Agents — 16 Thinker Personas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python panteon-agents.py                  # Show schedule + sample posts
  python panteon-agents.py --post taleb     # Generate a Taleb post
  python panteon-agents.py --thread         # Generate an interaction thread
  python panteon-agents.py --schedule       # Show weekly schedule only
  python panteon-agents.py --cron           # Show cron configuration
  python panteon-agents.py --list           # List all 16 personas
  python panteon-agents.py --csv            # Export schedule as CSV
        """
    )
    parser.add_argument("--post", type=str, default=None,
                        help="Generate a post for a specific persona (id or 'random')")
    parser.add_argument("--thread", action="store_true",
                        help="Generate an interaction thread between random personas")
    parser.add_argument("--thread-participants", type=str, nargs="+", default=None,
                        help="Specify persona IDs for the thread")
    parser.add_argument("--thread-topic", type=str, default=None,
                        help="Topic for thread discussion")
    parser.add_argument("--schedule", action="store_true",
                        help="Output weekly schedule only")
    parser.add_argument("--csv", action="store_true",
                        help="Export schedule as CSV file")
    parser.add_argument("--cron", action="store_true",
                        help="Show cron config for automation")
    parser.add_argument("--list", action="store_true",
                        help="List all personas with descriptions")
    parser.add_argument("--verify", action="store_true",
                        help="Verify all posts reference the book site")
    parser.add_argument("--format", type=str, choices=["text", "json"], default="text",
                        help="Output format")

    args = parser.parse_args()
    gen = ContentGenerator(PERSONAS)

    # ── List all personas ──
    if args.list:
        print("=" * 72)
        print("  PANTEÓN PROMOTION AGENTS — 16 THINKER PERSONAS")
        print("=" * 72)
        for p in PERSONAS:
            print(f"\n  {p.emoji}  {p.name:<18} ({p.era})")
            print(f"     Domain:       {p.domain}")
            print(f"     Style:        {p.posting_style[:80]}...")
            print(f"     Rivalries:    {', '.join(p.rivalries) if p.rivalries else 'None'}")
            print(f"     Affinity:     {', '.join(p.affinity) if p.affinity else 'None'}")
            print(f"     Topics:       {', '.join(p.weekly_topics[:4])}...")
        print(f"\n  Total: {len(PERSONAS)} personas")
        return

    # ── Cron config ──
    if args.cron:
        print(generate_cron_config())
        return

    # ── Verify references ──
    if args.verify:
        print(verify_references())
        return

    # ── Schedule only ──
    if args.schedule or args.csv:
        schedule = generate_weekly_schedule(output_format=args.format)
        if args.csv:
            csv_path = os.path.join(DATA_DIR, f"schedule-{datetime.date.today().isoformat()}.csv")
            # Re-generate as structured list for CSV
            sched_list = generate_weekly_schedule(output_format="json")
            export_schedule_csv(json.loads(sched_list), csv_path)
            print(f"CSV exported to: {csv_path}")
        else:
            print(schedule)
        return

    # ── Thread generation ──
    if args.thread:
        participants = args.thread_participants
        if participants is None:
            # Pick 3 random personas (excluding those without interactions)
            pool = [p.id for p in PERSONAS if p.rivalries or p.affinity]
            participants = random.sample(pool, min(3, len(pool)))
        else:
            for pid in participants:
                if pid not in PERSONA_MAP:
                    print(f"Unknown persona: {pid}")
                    sys.exit(1)

        topic = args.thread_topic or random.choice(
            DAILY_THEMES[random.choice(WEEKDAYS)]
        )

        print("=" * 72)
        print("  PANTEÓN INTERACTION THREAD")
        print("=" * 72)
        print(f"  Topic: {topic}")
        print(f"  Participants: {', '.join(p.capitalize() for p in participants)}")
        print("-" * 72)
        print()

        thread = gen.generate_thread(participants, topic)
        for post in thread:
            seq = post.get("thread_seq", 0)
            prefix = "🧵 OPENER" if seq == 0 else f"   ↳ Reply #{seq}"
            print(f"  {post['emoji']} [{post['persona_name']}]")
            print(f"  {prefix}")
            print(f"  {post['content'][:280]}")
            print()

        print("-" * 72)
        print(f"  📖 {BOOK_SITE}")
        return

    # ── Single post ──
    if args.post:
        if args.post == "random":
            persona_id = random.choice(PERSONAS).id
        else:
            persona_id = args.post
            if persona_id not in PERSONA_MAP:
                print(f"Unknown persona: {persona_id}")
                print(f"Available: {', '.join(p.id for p in PERSONAS)}")
                sys.exit(1)

        post = gen.generate_post(persona_id)
        print("=" * 72)
        print(f"  {post['emoji']}  @{post['persona_name']} — Generated Post")
        print("=" * 72)
        print()
        print(f"  {post['content']}")
        print()
        print("-" * 72)
        print(f"  📖 {BOOK_SITE}")
        return

    # ── Default: full output ──
    print(f"PANTEÓN PROMOTION AGENTS — {datetime.datetime.now():%B %d, %Y}")
    print()

    # Schedule
    print(generate_weekly_schedule(output_format="text"))
    print()

    # Sample posts
    print("=" * 72)
    print("  SAMPLE POSTS — One per persona")
    print("=" * 72)
    print()
    for p in PERSONAS:
        post = gen.generate_post(p.id, include_book_angle=True)
        print(f"  {post['emoji']}  @{post['persona_name']}")
        print(f"  >> {post['content'][:120]}...")
        print()

    # Thread example
    print("=" * 72)
    print("  EXAMPLE THREAD — 3 Personas in dialogue")
    print("=" * 72)
    sample_thread_pool = [p.id for p in PERSONAS if len(p.rivalries) + len(p.affinity) > 0]
    sample_thread_ids = random.sample(sample_thread_pool, 3)
    sample_topic = "the nature of knowledge"
    thread = gen.generate_thread(sample_thread_ids, sample_topic)
    for post in thread:
        seq = post.get("thread_seq", 0)
        prefix = "🧵 OPENER" if seq == 0 else f"   ↳ #{seq}"
        print(f"  {post['emoji']} [{post['persona_name']}] {prefix}")
        print(f"  {post['content'][:200]}")
        print()


if __name__ == "__main__":
    main()
