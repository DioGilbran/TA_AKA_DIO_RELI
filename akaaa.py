import time
import pandas as pd
import matplotlib.pyplot as plt

# Fungsi Content-Based Filtering Iteratif
def content_based_filtering_iterative(films, user_preferences):
    recommendations = []
    for film in films:
        match_score = 0
        for genre in film["genres"]:
            if genre in user_preferences["preferred_genres"]:
                match_score += 1
        if match_score > 0:
            recommendations.append({"film": film, "score": match_score})
    return recommendations

# Fungsi Content-Based Filtering Rekursif
def content_based_filtering_recursive(films, user_preferences, index=0, recommendations=None):
    if recommendations is None:
        recommendations = []
    if index == len(films):
        return recommendations
    match_score = sum(1 for genre in films[index]["genres"] if genre in user_preferences["preferred_genres"])
    if match_score > 0:
        recommendations.append({"film": films[index], "score": match_score})
    return content_based_filtering_recursive(films, user_preferences, index + 1, recommendations)

# Fungsi Collaborative Filtering Iteratif
def collaborative_filtering_iterative(ratings, target_user):
    similarities = []
    for user_index, user_ratings in enumerate(ratings):
        if user_index != target_user:
            similarity = sum(r1 * r2 for r1, r2 in zip(ratings[target_user], user_ratings))
            similarities.append((user_index, similarity))
    return similarities

# Fungsi Collaborative Filtering Rekursif
def collaborative_filtering_recursive(ratings, target_user, user_index=0, similarities=None):
    if similarities is None:
        similarities = []
    if user_index == len(ratings):
        return similarities
    if user_index != target_user:
        similarity = sum(r1 * r2 for r1, r2 in zip(ratings[target_user], ratings[user_index]))
        similarities.append((user_index, similarity))
    return collaborative_filtering_recursive(ratings, target_user, user_index + 1, similarities)

if __name__ == "__main__":
    # Data film dummy
    films = [
        {"id": 1, "title": "Film A", "genres": ["Action", "Thriller"]},
        {"id": 2, "title": "Film B", "genres": ["Romance", "Drama"]},
        {"id": 3, "title": "Film C", "genres": ["Sci-Fi", "Action"]},
        {"id": 4, "title": "Film D", "genres": ["Horror", "Thriller"]},
        {"id": 5, "title": "Film E", "genres": ["Comedy"]},
    ] * 100  # Gandakan data untuk analisis kompleksitas

    # Data user preferences
    user_preferences = {"preferred_genres": ["Action", "Sci-Fi"]}

    # Data rating dummy
    ratings = [
        [5, 0, 0, 3, 0],
        [0, 4, 3, 0, 5],
        [5, 3, 4, 0, 0],
        [0, 0, 4, 5, 0],
    ] * 25  # Gandakan data untuk analisis kompleksitas

    # List untuk menyimpan hasil
    results = []

    # Loop analisis sebanyak 5 kali
    for run in range(1, 6):
        print(f"\nRun {run} - Analisis Komparasi:")

        try:
            n = int(input("Masukkan jumlah data (n): "))
            if n > len(films):
                print(f"Nilai n terlalu besar! Maksimal: {len(films)}")
                continue

            sample_films = films[:n]
            sample_ratings = ratings[:n]

            # Content-Based Iterative
            start_time_iterative_cb = time.perf_counter()
            content_based_filtering_iterative(sample_films, user_preferences)
            exec_time_iterative_cb = time.perf_counter() - start_time_iterative_cb

            # Content-Based Recursive
            start_time_recursive_cb = time.perf_counter()
            content_based_filtering_recursive(sample_films, user_preferences)
            exec_time_recursive_cb = time.perf_counter() - start_time_recursive_cb

            # Collaborative Iterative
            start_time_iterative_cf = time.perf_counter()
            collaborative_filtering_iterative(sample_ratings, 0)
            exec_time_iterative_cf = time.perf_counter() - start_time_iterative_cf

            # Collaborative Recursive
            start_time_recursive_cf = time.perf_counter()
            collaborative_filtering_recursive(sample_ratings, 0)
            exec_time_recursive_cf = time.perf_counter() - start_time_recursive_cf

            # Simpan hasil untuk setiap run
            results.append((n, exec_time_recursive_cb, exec_time_iterative_cb, exec_time_recursive_cf, exec_time_iterative_cf))

            # Konversi hasil ke DataFrame
            df = pd.DataFrame(results, columns=[
                'n',
                'CB Recursive Time (s)', 'CB Iterative Time (s)',
                'CF Recursive Time (s)', 'CF Iterative Time (s)'
            ])

            # Tampilkan hasil di terminal
            print(df.to_string(index=False))

            # Buat grafik
            plt.figure(figsize=(12, 8))

            # Plot Content-Based
            plt.plot(df['n'], df['CB Recursive Time (s)'], label='CB Recursive', color='green', marker='o', linestyle='-')
            plt.plot(df['n'], df['CB Iterative Time (s)'], label='CB Iterative', color='purple', marker='o', linestyle='-')

            # Plot Collaborative Filtering
            plt.plot(df['n'], df['CF Recursive Time (s)'], label='CF Recursive', color='red', marker='o', linestyle='-')
            plt.plot(df['n'], df['CF Iterative Time (s)'], label='CF Iterative', color='blue', marker='o', linestyle='-')

            # Tambahkan label, judul, dan legenda
            plt.title('Perbandingan Waktu Eksekusi Algoritma Rekomendasi Film')
            plt.xlabel('Ukuran Input (n)')
            plt.ylabel('Waktu Eksekusi (detik)')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()

            # Tampilkan grafik
            plt.show()

        except ValueError:
            print("Masukkan angka yang valid!")

    print("\nProgram selesai!")
