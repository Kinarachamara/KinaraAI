import json
import math
import re
from pathlib import Path
import difflib

# 1. දත්ත ගොනුව පූරණය කිරීම
qa_file = Path("knowledge/qa.json")

try:
    with open(qa_file, "r", encoding="utf-8") as f:
        qa = json.load(f)
except FileNotFoundError:
    print("දෝෂයකි: 'knowledge/qa.json' ගොනුව සොයාගත නොහැක!")
    print("කරුණාකර නිවැරදි ෆෝල්ඩරය තුළ JSON ගොනුව තබා නැවත උත්සාහ කරන්න.")
    qa = {}

print("=" * 45)
print("   මගේම AI (ප්‍රබල TF-IDF & Fuzzy Matching)")
print("=" * 45)
print("\nප්‍රශ්න අහන්න (ඉවත් වෙන්න 'exit', 'quit' හෝ 'bye')\n")

all_questions = list(qa.keys())

# 2. පෙළ පිරිසිදු කිරීම සහ වචන වෙන් කිරීමේ ශ්‍රිතය (Text Preprocessing)
def tokenize(text):
    text = text.lower()
    # සිංහල සහ ඉංග්‍රීසි වචන පමණක් වෙන් කර ගනී (ලකුණු ඉවත් කරයි)
    words = re.findall(r'\b\w+\b', text)
    return words

# 3. TF-IDF Cosine Similarity ගණනය කිරීමේ බුද්ධිමත් ඇල්ගොරිතමය
def get_best_tfidf_match(user_query, question_list):
    query_words = tokenize(user_query)
    if not query_words:
        return None, 0.0

    best_match = None
    max_similarity = 0.0

    # සියලුම ප්‍රශ්න සඳහා Document Frequency (DF) සෙවීම
    df = {}
    for q in question_list:
        words = set(tokenize(q))
        for word in words:
            df[word] = df.get(word, 0) + 1

    total_docs = len(question_list)

    for q in question_list:
        q_words = tokenize(q)
        if not q_words:
            continue

        # Term Frequency (TF) ගණනය කිරීම
        q_tf = {}
        for word in q_words:
            q_tf[word] = q_tf.get(word, 0) + 1

        query_tf = {}
        for word in query_words:
            query_tf[word] = query_tf.get(word, 0) + 1

        # Cosine Similarity සඳහා දෛශික (Vectors) නිර්මාණය
        unique_words = set(q_words + query_words)
        dot_product = 0.0
        q_norm_sq = 0.0
        query_norm_sq = 0.0

        for word in unique_words:
            # IDF අගය සෙවීම
            word_df = df.get(word, 1)
            idf = math.log((1 + total_docs) / (1 + word_df)) + 1

            # TF-IDF අගයන්
            q_tfidf = q_tf.get(word, 0) * idf
            query_tfidf = query_tf.get(word, 0) * idf

            dot_product += q_tfidf * query_tfidf
            q_norm_sq += q_tfidf ** 2
            query_norm_sq += query_tfidf ** 2

        q_norm = math.sqrt(q_norm_sq)
        query_norm = math.sqrt(query_norm_sq)

        if q_norm == 0.0 or query_norm == 0.0:
            similarity = 0.0
        else:
            similarity = dot_product / (q_norm * query_norm)

        if similarity > max_similarity:
            max_similarity = similarity
            best_match = q

    return best_match, max_similarity

# 4. ප්‍රධාන Chat Loop එක
while True:
    question = input("ඔබ: ").strip()

    # ඉවත් වීමේ විධානයන් පරීක්ෂාව
    if question.lower() in ["exit", "quit", "ඉවත්", "bye"]:
        print("AI: බයි! ආයුබෝවන්!")
        break

    if not question:
        continue

    answer = None
    q_lower = question.lower()

    # පියවර A: සෘජු ගැලපීම (Exact Match)
    if question in qa:
        answer = qa[question]
    elif q_lower in qa:
        answer = qa[q_lower]
    
    # පියවර B: TF-IDF Cosine Similarity (පද සහ වචන ගැලපීම)
    if not answer and all_questions:
        best_q, score = get_best_tfidf_match(question, all_questions)
        # 35% කට වඩා අර්ථයෙන් සමාන නම් පිළිතුර ලබා දෙයි
        if score > 0.35:
            answer = qa[best_q]

    # පියවර C: Fuzzy Matching (අකුරු වැරදීම්/Typos සඳහා)
    if not answer and all_questions:
        matches = difflib.get_close_matches(question, all_questions, n=1, cutoff=0.5)
        if matches:
            answer = qa[matches[0]]
        else:
            # ඉංග්‍රීසි සිම්පල් අකුරු සඳහා Fuzzy Matching
            matches_lower = difflib.get_close_matches(q_lower, [k.lower() for k in all_questions], n=1, cutoff=0.5)
            if matches_lower:
                matched_key = next((k for k in all_questions if k.lower() == matches_lower[0]), None)
                if matched_key:
                    answer = qa[matched_key]

    # පියවර D: අර්ධ ගැලපීම (Substring Match - අවසාන උත්සාහය)
    if not answer:
        for key, value in qa.items():
            if key.lower() in q_lower or q_lower in key.lower():
                answer = value
                break

    # පිළිතුර මුද්‍රණය කිරීම
    if answer:
        print(f"AI: {answer}\n")
    else:
        print("AI: මට ඒ ගැන තොරතුරු නැහැ. (වෙනත් ආකාරයකින් අසා බලන්න)\n")
