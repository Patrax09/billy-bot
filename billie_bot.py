import discord
from discord.ext import commands
import random
import requests
from bs4 import BeautifulSoup
import os
import urllib.parse

# --- CONFIGURAZIONE BOT ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- LISTE STATICHE ---
quotes = [
    "I'm in love with my future, can't wait to meet her. 💜",
    "You should see me in a crown. 👑",
    "People have so much going on. You have no idea. 💭",
    "I don't know how to function without music. 🎵",
    "It's okay to be sad. 💧",
    "I never thought I’d be happy again, and here I am. 🌈",
    "If we were meant to be, we would have been by now. 🕰️",
    "I don't want to be you anymore. ❌",
    "Nothing really scares me, to be honest. 😐",
    "I like being alone. But I hate feeling alone. 🖤",
    "I’m a bad liar with a pretty mouth. 😶‍🌫️",
    "Silence speaks louder than words. 🤫",
    "Love is weird. ❤️‍🔥",
    "I think too much, that’s my problem. 💭",
    "I dress how I want. 🧥",
    "Don't smile at me. 😶",
    "Music is everything to me. 🎶",
    "You can’t fake authenticity. ✨",
    "Insecurity is a killer. 💀",
    "Being different is good. 🌟",
    "Sometimes I feel like nothing. 🫥",
    "Vulnerability is strength. 💪",
    "You should never care what people think. 🗣️",
    "Every person deserves respect. 🤝",
    "I just want to create. 🎨",
    "I don't owe anyone anything. 🚫",
    "There's beauty in sadness. 🦋",
    "I write what I feel. ✍️",
    "Pain makes great art. 🖤🎭",
    "My body is mine. 👤",
    "You can’t control everything. 🔄",
    "I grew up fast. 🧠",
    "Fame is strange. 🌍",
    "Sometimes I don’t recognize myself. 🪞",
    "Smiles can be fake. 🙂"
]

facts = [
    "Billie Eilish è la più giovane artista ad aver vinto i 4 principali Grammy nello stesso anno.",
    "Ha scritto la maggior parte delle sue canzoni con suo fratello Finneas.",
    "Billie è vegana e un'attivista per i diritti degli animali.",
    "Ha lanciato un documentario sulla sua vita: *The World's a Little Blurry*.",
    "Ha una fobia per le balene!",
    "Billie è nata il 18 dicembre 2001 a Los Angeles.",
    "Il suo vero nome è Billie Eilish Pirate Baird O’Connell.",
    "Ha scritto la sua prima canzone a 11 anni.",
        "È cresciuta con suo fratello Finneas, anche lui musicista.",
    "La sua canzone 'Ocean Eyes' l’ha resa famosa.",
    "È vegana convinta.",
    "È affetta dalla sindrome di Tourette.",
    "Ha la sinestesia: vede suoni e colori.",
    "Ha vinto due Oscar prima dei 23 anni.",
    "È la più giovane vincitrice del Grammy per l’Album dell’anno.",
    "Adora gli avocado.",
    "È una fan accanita della serie *The Office*.",
    "Ha cantato per James Bond: *No Time to Die*.",
    "Ha un ragno domestico.",
    "Il suo colore preferito è il nero.",
    "Disegna alcuni dei suoi vestiti.",
    "Ha un armadio pieno di scarpe (oltre 600 paia!).",
    "Ha iniziato a cantare a 8 anni nel coro di Los Angeles.",
    "È stata educata a casa.",
    "Il suo stile oversize è una scelta personale.",
    "Ama i cani.",
    "È molto attenta alla salute mentale.",
    "Ha una collezione di occhiali da sole.",
    "È una gamer: gioca a *Call of Duty*.",
    "Ha scritto canzoni anche per altri artisti.",
    "Ha partecipato alla colonna sonora del film *Turning Red*.",
    "È stata la più giovane a scrivere per un film di Bond.",
    "Ha convinto un famoso brand a rinunciare alla pelliccia.",
    "Usa spesso smalti e anelli molto colorati.",
    "Partecipa attivamente a campagne per il clima."
]

awards = [
    "7 Grammy Awards",
    "2 American Music Awards",
    "3 MTV Video Music Awards",
    "1 Golden Globe",
    "1 Oscar per 'No Time to Die' (Miglior canzone originale)"
]

# --- INFORMAZIONI STATICHE ---
billie_bio_text = (
    "Billie Eilish è una cantautrice americana nata il 18 dicembre 2001. "
    "È salita alla ribalta nel 2016 con il singolo 'Ocean Eyes' e da allora ha vinto numerosi premi, "
    "tra cui Grammy, American Music Awards e Billboard Music Awards. È nota per il suo stile unico e la sua voce eterea."
)

billie_albums_list = [
    "2017 - Don't Smile at Me",
    "2019 - When We All Fall Asleep, Where Do We Go?",
    "2021 - Happier Than Ever",
    "2024 - Hit Me Hard and Soft"
]

billie_songs_list = [
    "All the Good Girls Go to Hell",
    "Another Stupid Song",
    "Bad Guy",
    "Billie Bossa Nova",
    "Birds of a Feather",
    "Bored",
    "Chihiro",
    "Copycat",
    "Come Out and Play",
    "Everything I Wanted",
    "Getting Older",
    "Goldwing",
    "Halley's Comet",
    "Happier Than Ever",
    "Hostage",
    "I Didn't Change My Number",
    "I Love You",
    "Ilomilo",
    "Listen Before I Go",
    "Lost Cause",
    "Lovely (with Khalid)",
    "My Future",
    "NDA",
    "No Time to Die",
    "Ocean Eyes",
    "Oxytocin",
    "OverHeated",
    "Party Favor",
    "Six Feet Under",
    "The 30th",
    "The End of the World",
    "Therefore I Am",
    "TV",
    "What Was I Made For?",
    "When I Was Older",
    "When the Party's Over",
    "Wish You Were Gay",
    "Xanny",
    "You Should See Me in a Crown"
]

# --- FUNZIONE: LYRICS ---
def get_lyrics(song_title):
    search = urllib.parse.quote(song_title + " billie eilish site:genius.com")
    url = f"https://www.google.com/search?q={search}"
    return f"🔍 Ecco i testi che ho trovato per **{song_title}**:\n{url}"

# --- FUNZIONE: IMMAGINE RANDOM  ---
def get_random_billie_image():
    immagini = [
        "https://images.unsplash.com/photo-1598387846482-6e0b8f4b8e4d",
        "https://images.unsplash.com/photo-1601234567890-abcdef123456",
        "https://images.unsplash.com/photo-1612345678901-bcdefa234567",
        "https://images.unsplash.com/photo-1623456789012-cdefab345678",
        "https://images.unsplash.com/photo-1634567890123-defabc456789",
        "https://images.unsplash.com/photo-1645678901234-efabcd567890",
        "https://images.unsplash.com/photo-1656789012345-fabcde678901",
        "https://images.unsplash.com/photo-1667890123456-abcdef789012",
        "https://images.unsplash.com/photo-1678901234567-bcdefa890123",
        "https://images.unsplash.com/photo-1689012345678-cdefab901234",
        "https://images.unsplash.com/photo-1690123456789-defabc012345",
        "https://images.unsplash.com/photo-1701234567890-efabcd123456",
        "https://images.unsplash.com/photo-1712345678901-fabcde234567",
        "https://images.unsplash.com/photo-1723456789012-abcdef345678",
        "https://images.unsplash.com/photo-1734567890123-bcdefa456789",
        "https://images.unsplash.com/photo-1745678901234-cdefab567890",
        "https://images.unsplash.com/photo-1756789012345-defabc678901",
        "https://images.unsplash.com/photo-1767890123456-efabcd789012",
        "https://images.unsplash.com/photo-1778901234567-fabcde890123",
        "https://images.unsplash.com/photo-1789012345678-abcdef901234" 
    ]
    return random.choice(immagini)

# --- COMANDI DINAMICI ---
@bot.command()
async def billie_image(ctx):
    await ctx.send("🔍 Sto cercando un'immagine di Billie per te...")
    image_url = get_random_billie_image()
    if image_url:
        await ctx.send("Ecco una bella immagine di Billie 💜")
        await ctx.send(image_url)
    else:
        await ctx.send("😢 Non sono riuscito a trovare immagini al momento.")

@bot.command()
async def billie_quote(ctx):
    quote = random.choice(quotes)
    await ctx.send(f"Billie dice: \"{quote}\"")

@bot.command()
async def billie_play(ctx, *, song_name):
    query = urllib.parse.quote(f"billie eilish {song_name}")
    url = f"https://www.youtube.com/results?search_query={query}"
    await ctx.send(f"🔎 Ecco cosa ho trovato per '{song_name}':\n{url}")

@bot.command()
async def billie_lyrics(ctx, *, song_name):
    lyrics_result = get_lyrics(song_name)
    await ctx.send(lyrics_result)

@bot.command()
async def billie_awards(ctx):
    await ctx.send("🌟 **Premi vinti da Billie Eilish:**")
    for award in awards:
        await ctx.send(f"- {award}")

@bot.command()
async def billie_facts(ctx):
    fact = random.choice(facts)
    await ctx.send(f"🤔 Curiosità su Billie: {fact}")

# --- COMANDI BASE ---
@bot.command()
async def billie_bio(ctx):
    await ctx.send(f"📜 **Biografia di Billie Eilish:**\n{billie_bio_text}")

@bot.command()
async def billie_albums(ctx):
    await ctx.send("💼 **Album di Billie Eilish:**")
    for album in billie_albums_list:
        await ctx.send(f"- {album}")

@bot.command()
async def billie_songs(ctx):
    await ctx.send("🎶 **Canzoni di Billie Eilish:**")
    for song in billie_songs_list:
        await ctx.send(f"- {song}")

# --- COMANDO HELP PERSONALIZZATO ---
@bot.command()
async def billie_help(ctx):
    help_text = (
        "📚 **Comandi disponibili del Billie Bot**\n"
        "`!billie_bio` → Biografia\n"
        "`!billie_albums` → Lista album\n"
        "`!billie_songs` → Tutte le canzoni\n"
        "`!billie_image` → Immagine casuale\n"
        "`!billie_quote` → Frase casuale\n"
        "`!billie_play <titolo>` → Cerca la canzone su YouTube\n"
        "`!billie_lyrics <titolo>` → Cerca i testi della canzone\n"
        "`!billie_awards` → Premi vinti\n"
        "`!billie_facts` → Curiosità su Billie"
    )
    await ctx.send(help_text)

# --- EVENTO: Risposte automatiche ---
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "billie eilish" in message.content.lower():
        await message.channel.send("Hai parlato di Billie? 💚 Ecco un abbraccio sonoro!")
    await bot.process_commands(message)

# --- AVVIO DEL BOT ---
TOKEN = os.getenv("DISCORD_TOKEN") or "MTM3ODM2NDkyMjEwNjIyMDU2NQ.Gaojzl.Q9OJjJSvlnf64RHiNNRrWwyVRbyU7XeyaooHOc"
bot.run(TOKEN)
