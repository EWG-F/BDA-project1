#!/usr/bin/env python3
"""
TrendScope - Sample Data & Precomputed Results Generator
Generates realistic YouTube trending datasets for US, IN, GB, CA, FR
and precomputes MapReduce & Hive analytical outputs for instant demo mode.
"""

import os
import json
import csv
import random
from datetime import datetime, timedelta

def generate_category_json(filepath):
    categories = [
        {"id": "1", "snippet": {"title": "Film & Animation", "assignable": True}},
        {"id": "2", "snippet": {"title": "Autos & Vehicles", "assignable": True}},
        {"id": "10", "snippet": {"title": "Music", "assignable": True}},
        {"id": "15", "snippet": {"title": "Pets & Animals", "assignable": True}},
        {"id": "17", "snippet": {"title": "Sports", "assignable": True}},
        {"id": "19", "snippet": {"title": "Travel & Events", "assignable": True}},
        {"id": "20", "snippet": {"title": "Gaming", "assignable": True}},
        {"id": "22", "snippet": {"title": "People & Blogs", "assignable": True}},
        {"id": "23", "snippet": {"title": "Comedy", "assignable": True}},
        {"id": "24", "snippet": {"title": "Entertainment", "assignable": True}},
        {"id": "25", "snippet": {"title": "News & Politics", "assignable": True}},
        {"id": "26", "snippet": {"title": "Howto & Style", "assignable": True}},
        {"id": "27", "snippet": {"title": "Education", "assignable": True}},
        {"id": "28", "snippet": {"title": "Science & Technology", "assignable": True}},
        {"id": "29", "snippet": {"title": "Nonprofits & Activism", "assignable": True}}
    ]
    data = {"kind": "youtube#videoCategoryListResponse", "items": categories}
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def generate_country_csv(filepath, country_code, num_records=1200):
    random.seed(42 + hash(country_code) % 1000)
    
    country_channels = {
        "US": [
            ("MrBeast", 24, ["MrBeast", "Challenge", "Philanthropy", "Win", "Epic"]),
            ("Marques Brownlee", 28, ["MKBHD", "Tech Review", "Smartphone", "AI", "Apple"]),
            ("Veritasium", 27, ["Science", "Physics", "Experiment", "Truth", "Discovery"]),
            ("Taylor Swift", 10, ["Music Video", "Pop", "Eras Tour", "New Album", "Official"]),
            ("Dude Perfect", 17, ["Trick Shots", "Sports", "Challenge", "Insane", "Fun"]),
            ("PewDiePie", 20, ["Gaming", "Reaction", "Memes", "Funny", "Review"]),
            ("IGN", 20, ["Gameplay", "Game Trailer", "Review", "PS5", "Xbox"]),
            ("Tasty", 26, ["Recipe", "Food", "Quick Cooking", "Delicious", "Dinner"]),
            ("CNN", 25, ["Breaking News", "Politics", "World News", "Debate", "Analysis"]),
            ("TED", 27, ["TED Talk", "Inspiration", "Innovation", "Psychology", "Future"])
        ],
        "IN": [
            ("T-Series", 10, ["Bollywood", "Hindi Songs", "Official Music Video", "TSeries", "Hit Song"]),
            ("CarryMinati", 23, ["Roast", "Comedy", "CarryisLive", "Funny", "Hindi Roast"]),
            ("Technical Guruji", 28, ["Tech News", "Smartphone Unboxing", "Review Hindi", "Gadgets", "Hindi Tech"]),
            ("BB Ki Vines", 23, ["Bhuvan Bam", "Comedy Sketch", "Funny Drama", "Vines", "Entertainment"]),
            ("Sandeep Maheshwari", 27, ["Motivation", "Life Lessons", "Inspiration Hindi", "Success", "Mindset"]),
            ("Total Gaming", 20, ["Free Fire", "Garena", "Ajjubhai", "Gaming Live", "Clutch"]),
            ("NDTV India", 25, ["Hindi News", "Elections", "Breaking India", "Debate", "Prime Time"]),
            ("Kabita's Kitchen", 26, ["Indian Recipe", "Easy Cooking", "Quick Snacks", "Dessert", "Vegetarian"]),
            ("Cricket Country", 17, ["IPL Highlights", "Team India", "Cricket Match", "Virat Kohli", "Sixes"]),
            ("FilterCopy", 24, ["Relatable Skits", "Relationships", "Short Film", "Mini Series", "College Life"])
        ],
        "GB": [
            ("BBC News", 25, ["UK News", "Parliament", "Global Affairs", "Documentary", "Investigative"]),
            ("Sidemen", 24, ["Sidemen Sunday", "KSI", "Hide and Seek", "Tinder in Real Life", "Challenge"]),
            ("Ed Sheeran", 10, ["Acoustic", "Pop Music", "Live Performance", "Music Video", "British Pop"]),
            ("Gordon Ramsay", 26, ["Kitchen Nightmares", "MasterChef", "Cooking Guide", "Steak", "Ramsay Reacts"]),
            ("Sky Sports Premier League", 17, ["Goals Highlights", "EPL Matchday", "Football", "Arsenal", "Man City"]),
            ("DanTDM", 20, ["Minecraft", "Roblox", "Gaming Walkthrough", "Live Stream", "Funny Moments"]),
            ("Tom Scott", 27, ["Amazing Places", "Engineering", "Language", "History", "Trivia"]),
            ("Vogue UK", 26, ["Fashion Week", "Celebrity Style", "73 Questions", "Beauty Secrets", "British Vogue"]),
            ("Top Gear", 2, ["Supercars", "Drag Race", "Track Test", "Speed", "Classic Cars"]),
            ("Coldplay", 10, ["Music of the Spheres", "Concert Live", "Stadium Tour", "Rock Pop", "Official"])
        ],
        "CA": [
            ("Linus Tech Tips", 28, ["PC Build", "Graphics Card", "Hardware Review", "Tech Upgrade", "LTT"]),
            ("The Weeknd", 10, ["After Hours", "Synthwave", "R&B", "Live Concert", "Music Video"]),
            ("CBC News", 25, ["Canada Today", "Federal Policy", "National News", "Economy", "Climate"]),
            ("Hacksmith Industries", 28, ["Real Lightsaber", "Engineering Build", "Superhero Tech", "Science", "DIY"]),
            ("Drake", 10, ["OVO Sound", "Rap", "Music Video", "Certified Lover", "New Track"]),
            ("Sportsnet", 17, ["NHL Highlights", "Ice Hockey", "Stanley Cup", "Toronto Maple Leafs", "Goals"]),
            ("AsapSCIENCE", 27, ["Science Explained", "Biology", "Visual Experiment", "Psychology", "Fun Facts"]),
            ("Unbox Therapy", 28, ["Cool Tech", "Smartphone Gadgets", "Crazy Inventions", "Tech Setup", "Unboxing"]),
            ("Brave Wilderness", 15, ["Animal Encounters", "Coyote Peterson", "Wildlife", "Insect Sting", "Bite"]),
            ("Jubilee", 22, ["Middle Ground", "Spectrum", "Social Experiment", "Debate", "Empathy"])
        ],
        "FR": [
            ("Squeezie", 20, ["Gaming Fr", "Thread Horreur", "Funny", "Concept Video", "Storytelling"]),
            ("Cyprien", 23, ["Court Metrage", "Humour", "Sketch", "Animation", "Comedie"]),
            ("DavidLafargePokemon", 24, ["Pokemon Unboxing", "Booster Pack", "Collection", "Cartes", "Rare"]),
            ("France 24", 25, ["Actualite", "France News", "International", "Debat", "Politique"]),
            ("Norman", 23, ["Norman Fait Des Videos", "Stand Up", "Humour Francais", "Vlog", "Sketch"]),
            ("Mcfly et Carlito", 24, ["Concours Anecdotes", "Feat", "Defi Impossible", "Chanson", "Rigolo"]),
            ("L'Equipe", 17, ["Football", "Ligue 1", "PSG Highlights", "Mbappe", "Resume Match"]),
            ("Mister V", 23, ["Rap Francais", "Humour", "Parodie", "Skits", "Vines"]),
            ("Natoo", 22, ["Vlog", "Humour", "Mode", "Voyage", "Chienne de Vie"]),
            ("Sananas", 26, ["Tuto Maquillage", "Fashion Haul", "Beaute", "Lookbook", "Conseils"])
        ]
    }
    
    titles_pool = [
        "I Built The World's Most Insane Secret Room!",
        "Ultimate Smartphone Battle 2024: The Real Truth Revealed",
        "Official Music Video - Breaking All Global Records",
        "Can We Survive 100 Hours In Extreme Wilderness?",
        "Top 10 Mind-Blowing Scientific Discoveries of the Decade",
        "EPL / Matchday Thriller: Unbelievable Last Minute Winner Highlights",
        "Why This New Technology Changes Everything Forever!",
        "Master Chef Reveals The Absolute Secret To Perfect Steak",
        "Crazy High-Stakes Hide and Seek in Luxury Mega Mansion",
        "Breaking News Analysis: Global Economic Shift and Future Outlook",
        "We Tested The Deepest Underwater Vault!",
        "Unboxing The World's Most Expensive Gadget ($50,000 Setup)",
        "The Dark Truth Behind Modern Social Media Algorithms",
        "Live Acoustic Session & Brand New Track Announcement",
        "Speed Running The Hardest Boss Level Without Taking Damage",
        "15 Minute Quick & Delicious Dinner That Will Blow Your Mind",
        "Epic Superhero Prototype Actually Works in Real Life!",
        "Championship Final Highlights & Unseen Locker Room Drama",
        "Why Physics Might Actually Be Completely Wrong",
        "Reacting To The Funniest Fan Submissions and Memes (Try Not To Laugh)"
    ]
    
    base_date = datetime(2024, 1, 15)
    
    # We will generate a structured set of videos, some trending across 1 to 5 consecutive days
    video_templates = []
    channels = country_channels.get(country_code, country_channels["US"])
    
    for idx in range(num_records // 3):
        v_id = f"{country_code}_vid_{idx:04d}"
        ch_name, cat_id, ch_tags = random.choice(channels)
        base_title = random.choice(titles_pool)
        title = f"{base_title} [{country_code} Special #{idx+1}]"
        
        # Tags combining channel keywords and common tags
        tags_list = ch_tags + [country_code.lower(), "trending", "2024", "viral", "hd video", "youtube"]
        tags_str = "|".join([f'"{t}"' for t in tags_list])
        
        # Publish date 1-10 days before base_date
        pub_date = base_date - timedelta(days=random.randint(1, 10), hours=random.randint(0, 23))
        publish_time = pub_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        
        # Base metrics
        base_views = random.randint(25000, 15000000)
        like_ratio = random.uniform(0.02, 0.08)
        dislike_ratio = random.uniform(0.001, 0.005)
        comment_ratio = random.uniform(0.002, 0.015)
        
        sentiment_mood = random.choice(["positive", "positive", "neutral", "negative", "super_positive"])
        if sentiment_mood == "super_positive":
            desc = f"Thank you all so much for the incredible support! We love you all! Don't forget to like and subscribe for amazing future content. Best community ever!"
        elif sentiment_mood == "positive":
            desc = f"Welcome back to the channel! In today's episode we explore great new tips, awesome gameplay and fun challenges. Enjoy the video!"
        elif sentiment_mood == "negative":
            desc = f"An unfortunate issue occurred and we need to address this serious mistake. Terrible situation, warning to everyone, do not repeat this fail."
        else:
            desc = f"Official channel release for {title}. Watch the full breakdown, timestamps, and resources in the description box below."
            
        trending_days_count = random.choices([1, 2, 3, 4, 5], weights=[45, 25, 15, 10, 5])[0]
        
        for day in range(trending_days_count):
            trend_dt = base_date + timedelta(days=day + random.randint(0, 5))
            trend_date_str = trend_dt.strftime("%y.%d.%m")
            
            # Growth multiplier per trending day
            multiplier = 1.0 + (day * random.uniform(0.15, 0.45))
            views = int(base_views * multiplier)
            likes = int(views * like_ratio * random.uniform(0.95, 1.05))
            dislikes = int(views * dislike_ratio * random.uniform(0.95, 1.05))
            comment_count = int(views * comment_ratio * random.uniform(0.95, 1.05))
            
            video_templates.append({
                "video_id": v_id,
                "trending_date": trend_date_str,
                "title": title,
                "channel_title": ch_name,
                "category_id": cat_id,
                "publish_time": publish_time,
                "tags": tags_str,
                "views": views,
                "likes": likes,
                "dislikes": dislikes,
                "comment_count": comment_count,
                "thumbnail_link": f"https://i.ytimg.com/vi/{v_id}/default.jpg",
                "comments_disabled": "False",
                "ratings_disabled": "False",
                "video_error_or_removed": "False",
                "description": desc
            })
            
    # Write to CSV
    headers = [
        "video_id", "trending_date", "title", "channel_title", "category_id",
        "publish_time", "tags", "views", "likes", "dislikes", "comment_count",
        "thumbnail_link", "comments_disabled", "ratings_disabled",
        "video_error_or_removed", "description"
    ]
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in video_templates:
            writer.writerow(row)
            
    return len(video_templates)

def precompute_processed_tables(raw_dir, processed_dir):
    """
    Computes standard MapReduce & Hive aggregate files to guarantee instant
    Demo / Standalone mode loading with verified metrics.
    """
    import re
    from collections import Counter, defaultdict
    
    stop_words = {
        "the", "and", "a", "to", "of", "in", "is", "for", "that", "this", "it",
        "on", "with", "as", "at", "by", "from", "be", "or", "an", "are", "from",
        "video", "official", "new", "hd", "special", "part", "vs", "full", "2024",
        "all", "how", "what", "why", "when", "who", "which", "my", "your", "our"
    }
    
    keyword_counter = Counter()
    category_metrics = defaultdict(lambda: {"count": 0, "views": 0, "likes": 0, "comments": 0})
    video_persistence = defaultdict(lambda: {"title": "", "channel": "", "category_id": "", "days": set(), "max_views": 0, "max_likes": 0})
    channel_metrics = defaultdict(lambda: {"videos": set(), "views": 0, "likes": 0, "comments": 0})
    country_metrics = defaultdict(lambda: {"videos": 0, "views": 0, "likes": 0, "comments": 0, "unique_videos": set()})
    
    cat_names = {
        "1": "Film & Animation", "2": "Autos & Vehicles", "10": "Music", "15": "Pets & Animals",
        "17": "Sports", "19": "Travel & Events", "20": "Gaming", "22": "People & Blogs",
        "23": "Comedy", "24": "Entertainment", "25": "News & Politics", "26": "Howto & Style",
        "27": "Education", "28": "Science & Technology", "29": "Nonprofits & Activism"
    }
    
    countries = ["US", "IN", "GB", "CA", "FR"]
    
    for c in countries:
        c_path = os.path.join(raw_dir, f"{c}videos.csv")
        if not os.path.exists(c_path):
            continue
        with open(c_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                v_id = row['video_id']
                cat_id = str(row['category_id'])
                views = int(row['views'])
                likes = int(row['likes'])
                comments = int(row['comment_count'])
                t_date = row['trending_date']
                title = row['title']
                ch = row['channel_title']
                
                # Country aggregations
                country_metrics[c]["videos"] += 1
                country_metrics[c]["views"] += views
                country_metrics[c]["likes"] += likes
                country_metrics[c]["comments"] += comments
                country_metrics[c]["unique_videos"].add(v_id)
                
                # Keywords
                words = re.findall(r'[A-Za-z0-9#@]{3,}', title.lower())
                for w in words:
                    if w not in stop_words and not w.isdigit():
                        keyword_counter[w] += 1
                        
                # Category stats
                category_metrics[cat_id]["count"] += 1
                category_metrics[cat_id]["views"] += views
                category_metrics[cat_id]["likes"] += likes
                category_metrics[cat_id]["comments"] += comments
                
                # Persistence
                vp = video_persistence[v_id]
                vp["title"] = title
                vp["channel"] = ch
                vp["category_id"] = cat_id
                vp["days"].add(t_date)
                if views > vp["max_views"]:
                    vp["max_views"] = views
                    vp["max_likes"] = likes
                    
                # Channel metrics
                cm = channel_metrics[ch]
                cm["videos"].add(v_id)
                cm["views"] += views
                cm["likes"] += likes
                cm["comments"] += comments
                
    # 1. Save MapReduce Job 1 output (Keyword Frequency)
    mr1_path = os.path.join(processed_dir, "mapreduce_job1_keywords.csv")
    with open(mr1_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["keyword", "frequency", "log_scaled_impact"])
        for kw, freq in keyword_counter.most_common(150):
            writer.writerow([kw, freq, round(freq * 1.42, 2)])
            
    # 2. Save MapReduce Job 2 output (Category Stats)
    mr2_path = os.path.join(processed_dir, "mapreduce_job2_category_stats.csv")
    with open(mr2_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["category_id", "category_name", "video_count", "total_views", "total_likes", "total_comments", "avg_views", "avg_likes", "engagement_rate"])
        for cat_id, stats in category_metrics.items():
            cname = cat_names.get(cat_id, f"Category {cat_id}")
            cnt = stats["count"]
            t_views = stats["views"]
            t_likes = stats["likes"]
            t_comm = stats["comments"]
            avg_v = round(t_views / cnt, 1) if cnt else 0
            avg_l = round(t_likes / cnt, 1) if cnt else 0
            eng = round(((t_likes + t_comm) / t_views * 100), 2) if t_views else 0
            writer.writerow([cat_id, cname, cnt, t_views, t_likes, t_comm, avg_v, avg_l, eng])
            
    # 3. Save MapReduce Job 3 output (Trending Persistence)
    mr3_path = os.path.join(processed_dir, "mapreduce_job3_persistence.csv")
    with open(mr3_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["video_id", "title", "channel_title", "category_name", "consecutive_trending_days", "peak_views", "peak_likes", "persistence_score"])
        for v_id, vp in video_persistence.items():
            days_count = len(vp["days"])
            cname = cat_names.get(vp["category_id"], "General")
            p_score = round(days_count * 20.0 + (vp["max_views"] / 1000000.0) * 2.5, 2)
            writer.writerow([v_id, vp["title"], vp["channel"], cname, days_count, vp["max_views"], vp["max_likes"], p_score])
            
    # 4. Save Hive Top Channels
    hive_ch_path = os.path.join(processed_dir, "hive_top_channels.csv")
    with open(hive_ch_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["channel_title", "unique_videos", "total_views", "total_likes", "total_comments", "avg_engagement_rate"])
        sorted_channels = sorted(channel_metrics.items(), key=lambda x: x[1]["views"], reverse=True)
        for ch, cm in sorted_channels:
            u_vids = len(cm["videos"])
            v = cm["views"]
            l = cm["likes"]
            c = cm["comments"]
            eng = round(((l + c) / v * 100), 2) if v else 0
            writer.writerow([ch, u_vids, v, l, c, eng])
            
    # 5. Save Hive Regional Summary
    hive_reg_path = os.path.join(processed_dir, "hive_regional_summary.csv")
    with open(hive_reg_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["country", "total_trending_records", "unique_videos", "total_views", "total_likes", "total_comments", "avg_views_per_video", "avg_engagement_rate"])
        country_fullnames = {"US": "United States", "IN": "India", "GB": "United Kingdom", "CA": "Canada", "FR": "France"}
        for c, stats in country_metrics.items():
            t_rec = stats["videos"]
            u_vids = len(stats["unique_videos"])
            v = stats["views"]
            l = stats["likes"]
            comm = stats["comments"]
            avg_v = round(v / t_rec, 1) if t_rec else 0
            eng = round(((l + comm) / v * 100), 2) if v else 0
            writer.writerow([country_fullnames.get(c, c), t_rec, u_vids, v, l, comm, avg_v, eng])

if __name__ == "__main__":
    raw_dir = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
    processed_dir = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)
    
    countries = ["US", "IN", "GB", "CA", "FR"]
    for c in countries:
        json_file = os.path.join(raw_dir, f"{c}_category_id.json")
        csv_file = os.path.join(raw_dir, f"{c}videos.csv")
        generate_category_json(json_file)
        cnt = generate_country_csv(csv_file, c, num_records=1000)
        print(f"Generated {cnt} records for {c} -> {csv_file}")
        
    precompute_processed_tables(raw_dir, processed_dir)
    print("Precomputed Big Data MapReduce and Hive tables successfully!")
