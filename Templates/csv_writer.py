import csv

def write_pairs_to_csv(filename, rows):
    # writes pairs to a CSV 
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        
        writer.writerow(["word1", "word2", "word1_count", "word2_count", "character_difference"])
        
        for w1, w2, c1, c2, diff in rows:
            writer.writerow([w1, w2, c1, c2, diff])